# encoding: utf-8
# Copyright 2011, Tangere Infotech Pvt Ltd [http://tangere.in]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

from django import forms
from django.contrib.auth.models import User

from cmh.common.fields import PhoneNumberField, DefaultChoiceField, StripCharField
from cmh.common.fields import UsernameField
from cmh.common.fields import AutoCompleteOffTextInput, SpacedSelectInput
from cmh.common.fields import SpacedTextInput

from cmh.common.models import ComplaintDepartment
from cmh.common.constants import UserRoles

from cmh.usermgr.models import CmhUser, Official

from cmh.smsgateway.models import TextMessage
from cmh.common.utils import get_random_string, debug

from cmh.common.constants import PASSWORD_LEN, PASSWORD_MSG

class AddCSOMember (forms.Form):
    username = UsernameField (widget = AutoCompleteOffTextInput ())
    name     = StripCharField (widget = AutoCompleteOffTextInput ())
    phone    = PhoneNumberField (widget = AutoCompleteOffTextInput ())

    def save (self):
        user = User.objects.create (username = self.cleaned_data ['username'],
                                    first_name = self.cleaned_data ['name'])
        password = get_random_string (PASSWORD_LEN)
        user.set_password (password)
        user.save ()

        cmhuser = CmhUser.objects.create (user = user,
                                          phone = self.cleaned_data ['phone'])

        cmhuser.set_user_role (UserRoles.CSO)

        message = PASSWORD_MSG % (cmhuser.phone, password)
        debug (message)
        TextMessage.objects.queue_text_message (cmhuser.phone, message)

        return cmhuser


class RegisterDM (forms.Form):
    username = UsernameField (widget = SpacedTextInput (attrs={"readonly":
                                                               "readonly"}),
                              initial="dm", check=False)
    name     = StripCharField (widget = AutoCompleteOffTextInput ())
    phone    = PhoneNumberField (widget = AutoCompleteOffTextInput ())

    def save (self):
        user = User.objects.create (username = 'dm',
                                    first_name = self.cleaned_data ['name'])

        password = get_random_string (PASSWORD_LEN)

        user.set_password (password)
        user.save ()

        cmhuser = CmhUser.objects.create (user = user,
                                             phone = self.cleaned_data ['phone'])
        cmhuser.set_user_role (UserRoles.DM)

        message = PASSWORD_MSG % (cmhuser.phone, password)
        debug (message)
        TextMessage.objects.queue_text_message (cmhuser.phone, message)

        return cmhuser


class DmId (forms.Form):
    dmid = forms.IntegerField (widget = forms.HiddenInput ())


class EditDM (forms.Form):
    dmid     = forms.CharField (widget = forms.HiddenInput ())
    username = UsernameField (widget = SpacedTextInput (attrs = {"readonly" :
                                                                 "readonly"}),
                              initial="dm", check = False)
    name     = StripCharField (widget = AutoCompleteOffTextInput ())
    phone    = PhoneNumberField (widget = AutoCompleteOffTextInput ())


    def clean_dmid (self):
        try:
            dm = CmhUser.objects.get (user__approle__role = UserRoles.DM, id = self.cleaned_data ['dmid'])
        except CmhUser.DoesNotExist:
            raise forms.ValidationError ("Invalid DM Object")
        except CmhUser.MultipleObjectsReturned:
            raise forms.ValidationError ("Multiple DM Objects should not be present")
        return self.cleaned_data ['dmid']


    def clean_name (self):
        if self.cleaned_data ['name'] != None:
            return self.cleaned_data ['name'].strip ()
        else:
            return ''

    def save (self):
        dmid = self.cleaned_data ['dmid']
        dm = CmhUser.objects.get (user__approle__role = UserRoles.DM, id = dmid)

        user = dm.user
        user.first_name = self.cleaned_data ['name']

        password = get_random_string (PASSWORD_LEN)
        user.set_password (password)
        user.save ()

        dm.phone = self.cleaned_data ['phone']
        dm.save ()

        message = PASSWORD_MSG % (dm.phone, password)
        debug (message)
        TextMessage.objects.queue_text_message (dm.phone, message)


class AddEditOfficial (forms.Form):
    username   = UsernameField (widget=AutoCompleteOffTextInput ())
    name       = StripCharField (widget=AutoCompleteOffTextInput ())
    phone      = PhoneNumberField (widget=AutoCompleteOffTextInput ())
    department = DefaultChoiceField (widget = SpacedSelectInput ())
    supervisor = DefaultChoiceField (widget = SpacedSelectInput ())

    def __init__ (self, *args, **kwargs):
        if 'departments' in kwargs:
            departments = kwargs ['departments']
            del kwargs ['departments']
        else:
            departments = None

        if 'supervisors' in kwargs:
            supervisors = kwargs ['supervisors']
            del kwargs ['supervisors']
        else:
            supervisors = None

        super (AddEditOfficial, self).__init__ (*args, **kwargs)

        if departments != None:
            choices = [("%d" % department.id, department.name)
                       for department in departments]
            choices.insert (0, ('-1', '----'))
            self.fields ['department'].choices = choices

        if supervisors != None:
            choices = [(sup [0], sup [1]) for sup in supervisors]
            choices.insert (0, ('-1', '----'))
            self.fields ['supervisor'].choices = choices


    def clean_department (self):
        if self.cleaned_data ['department'] == -1:
            raise forms.ValidationError ("Department is mandatory")
        return self.cleaned_data ['department']

    def save (self):
        if self.cleaned_data ['supervisor'] == "-1":
            supervisor = None
            role = UserRoles.OFFICIAL
        else:
            supervisor = Official.objects.get (id = self.cleaned_data ['supervisor'])
            role = UserRoles.DELEGATE

        department = ComplaintDepartment.objects.get (id = self.cleaned_data ['department'])

        user = User.objects.create (username = self.cleaned_data ['username'],
                                    first_name = self.cleaned_data ['name'])
        password = get_random_string (PASSWORD_LEN)
        user.set_password (password)
        user.save ()

        cmhuser = CmhUser.objects.create (user = user,
                                          phone = self.cleaned_data ['phone'])
        cmhuser.set_user_role (role)
        cmhuser.save ()

        message = PASSWORD_MSG % (cmhuser.phone, password)
        debug (message)
        TextMessage.objects.queue_text_message (cmhuser.phone, message)

        official = Official.objects.create (user = user, supervisor = supervisor)

        official.departments.add (department)
        return official


class DepartmentSelected (forms.Form):
    department = forms.IntegerField ()
