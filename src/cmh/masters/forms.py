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
from django.utils.translation import ugettext as _

from cmh.common.fields import PhoneNumberField, DefaultChoiceField, StripCharField
from cmh.common.fields import UsernameField
from cmh.common.fields import AutoCompleteOffTextInput, SpacedSelectInput
from cmh.common.fields import SpacedTextInput, SpacedROTextInput
from cmh.common.fields import SpacedTextField, SpacedROTextField
from cmh.common.fields import LatLongField, MultiNumberIdField
from cmh.common.fields import SpacedTextAreaField

from cmh.common.models import ComplaintDepartment
from cmh.common.constants import UserRoles

from cmh.usermgr.models import CmhUser, Official

from cmh.smsgateway.utils import queue_sms
from cmh.common.utils import get_random_string, debug

from cmh.common.constants import PASSWORD_LEN, PASSWORD_MSG, DeployDistrict

from cmh.common.models import ComplaintMDG, ComplaintType, State, District, Block, GramPanchayat, Village
from cmh.common.models import MilleniumDevGoal

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

        message = PASSWORD_MSG % (cmhuser.user.username, password)
        queue_sms (cmhuser.phone, message)

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

        message = PASSWORD_MSG % (cmhuser.user.username, password)
        queue_sms (cmhuser.phone, message)

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
            raise forms.ValidationError (_("Invalid DM Object"))
        except CmhUser.MultipleObjectsReturned:
            raise forms.ValidationError (_("Multiple DM Objects should not be present"))
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
        queue_sms (dm.phone, message)


class AddEditOfficial (forms.Form):
    username   = UsernameField (widget=AutoCompleteOffTextInput ())
    name       = StripCharField (widget=AutoCompleteOffTextInput ())
    phone      = PhoneNumberField (widget=AutoCompleteOffTextInput ())
    department = DefaultChoiceField (widget = SpacedSelectInput ())
    supervisor = DefaultChoiceField (widget = SpacedSelectInput (), required = False)

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
            raise forms.ValidationError (_("Department is mandatory"))
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

        message = PASSWORD_MSG % (cmhuser.user.username, password)
        queue_sms (cmhuser.phone, message)

        official = Official.objects.create (user = user, supervisor = supervisor)

        official.department = department
        official.save()
        return official



class EditOfficial (forms.Form):
    objid       = forms.CharField (widget = forms.HiddenInput ())
    depid       = forms.CharField (widget = forms.HiddenInput ())
    username    = SpacedROTextField (label = _("UserName"))
    name        = SpacedTextField (widget=AutoCompleteOffTextInput (), label = _("Name"))
    phone       = PhoneNumberField (widget=AutoCompleteOffTextInput (), label =_("Phone Number"))
    department  = forms.ModelChoiceField (queryset = ComplaintDepartment.objects.all(), empty_label = "------", label=_("Department"))
    def __init__(self, offobj, *args, **kwargs) :
        super(EditOfficial, self).__init__(*args,**kwargs)
        if offobj != None:
            self.fields ['objid'].initial        = offobj.id
            self.fields ['username'].initial     = offobj.user.username
            self.fields ['name'].initial         = offobj.user.first_name
            self.fields ['phone'].initial        = offobj.phone_number
            self.fields ['department'].initial   = ComplaintDepartment.objects.get(id = offobj.department.id)
            self.fields ['depid'].initial        = offobj.department.id


    def save (self):
        dept            = ComplaintDepartment.objects.get (id = self.cleaned_data['department'].id)
        cmhuser         = CmhUser.objects.get(id = self.cleaned_data['objid'])
        official        = Official.objects.get(user__cmhuser__id = self.cleaned_data['objid'])

        user             = User.objects.get(username = self.cleaned_data['username'])
        user.first_name  = self.cleaned_data['name']
        password = get_random_string (PASSWORD_LEN)
        user.set_password (password)
        user.save ()

        cmhuser.user    = user
        cmhuser.phone   = self.cleaned_data ['phone']

        official.user   = user
        official.department = dept

        official.save()
        cmhuser.save ()

        message = PASSWORD_MSG % (cmhuser.user.username, password)
        queue_sms (cmhuser.phone, message)

        return official


class EditCso (forms.Form):
    objid    = forms.CharField (widget = forms.HiddenInput ())
    username =  SpacedROTextField (widget = AutoCompleteOffTextInput ())
    name     = StripCharField (widget = AutoCompleteOffTextInput ())
    phone    = PhoneNumberField (widget = AutoCompleteOffTextInput ())

    def __init__(self, csoobj, *args, **kwargs) :
        super(EditCso, self).__init__(*args,**kwargs)
        if csoobj != None:
            self.fields ['objid'].initial        = csoobj.id
            self.fields ['username'].initial     = csoobj.user.username
            self.fields ['name'].initial         = csoobj.user.first_name
            self.fields ['phone'].initial        = csoobj.phone_number


    def save (self):
        user             = User.objects.get(username = self.cleaned_data['username'])

        cmhuser          = CmhUser.objects.get(id = self.cleaned_data['objid'])
        user.first_name  = self.cleaned_data['name']
        password = get_random_string (PASSWORD_LEN)
        user.set_password (password)
        user.save()

        cmhuser.user    = user
        cmhuser.phone   = self.cleaned_data ['phone']

        cmhuser.save ()

        message = PASSWORD_MSG % (cmhuser.user.username, password)
        queue_sms (cmhuser.phone, message)

        return cmhuser

class DepartmentSelected (forms.Form):
    department = forms.IntegerField ()

class AddState (forms.Form):
    sname       = SpacedROTextField (label = _("State Name"), initial = DeployDistrict.DISTRICT.state.name)
    scode       = SpacedROTextField (label = _("State Code"), initial = DeployDistrict.DISTRICT.state.get_code())
    lattd       = LatLongField (label  = _("Latitude"), initial = DeployDistrict.DISTRICT.state.lattd)
    longd       = LatLongField (label  = _("Longitude"), initial = DeployDistrict.DISTRICT.state.longd)

    def save (self):
        state = DeployDistrict.DISTRICT.state
        state.lattd = self.cleaned_data['lattd']
        state.longd = self.cleaned_data['longd']
        state.save()

class AddDistrict (forms.Form):
    sname       = SpacedROTextField (label = _("State Name"), initial = DeployDistrict.DISTRICT.state.name)
    scode       = SpacedROTextField (label = _("State Code"), initial = DeployDistrict.DISTRICT.state.get_code())
    dname       = SpacedROTextField (label = _("District Name"), initial = DeployDistrict.DISTRICT.name)
    dcode       = SpacedROTextField (label = _("District Code"), initial = DeployDistrict.DISTRICT.get_code())
    lattd       = LatLongField (label  = _("District Latitude"), initial = DeployDistrict.DISTRICT.lattd)
    longd       = LatLongField (label  = _("District Longitude"), initial = DeployDistrict.DISTRICT.longd)
    def save (self):
        dist = DeployDistrict.DISTRICT
        dist.lattd = self.cleaned_data['lattd']
        dist.longd = self.cleaned_data['longd']
        dist.save()



class AddDep (forms.Form):
    depname       = SpacedTextField (label = _("Department Name"))
    depcode       = SpacedTextField (label = _("Department Code"))

    def clean_depcode(self) :
        dcode = self.cleaned_data ['depcode']
        if ComplaintDepartment.objects.filter (code = dcode).count () != 0:
            raise forms.ValidationError (_("Department code already exists"))

        if dcode.isupper() == False:
            raise forms.ValidationError (_("Department code must be a string with all CAPTIAL LETTERS"))
        return dcode

    def save (self):
        dep = ComplaintDepartment.objects.create(code     = self.cleaned_data['depcode'],
                                                 name     = self.cleaned_data['depname'],
                                                 district = DeployDistrict.DISTRICT)
        dep.save()

class AddBlock (forms.Form):
    sname       = SpacedROTextField (label = _("State Name"), initial = DeployDistrict.DISTRICT.state.name)
    scode       = SpacedROTextField (label = _("State Code"), initial = DeployDistrict.DISTRICT.state.get_code ())
    dname       = SpacedROTextField (label = _("District Name"), initial = DeployDistrict.DISTRICT.name)
    dcode       = SpacedROTextField (label = _("District Code"), initial = DeployDistrict.DISTRICT.get_code ())
    bname       = SpacedTextField (label=_("Block Name"))
    bcode       = SpacedTextField (label=_("Block Code"))
    lattd       = LatLongField (label  = _("Block Latitude"))
    longd       = LatLongField (label  = _("Block Longitude"))

    def clean_bcode(self) :
        try:
            bcode = int (self.cleaned_data ['bcode'])
        except ValueError:
            raise forms.ValidationError (_("Block code must be a number"))

        comp_bcode = "%s.%03d" % (DeployDistrict.DISTRICT.code, bcode)
        if Block.objects.filter (code = comp_bcode).count () != 0:
            raise forms.ValidationError (_("Block code already exists"))
        return comp_bcode

    def save (self):
        blk = Block.objects.create(code     = self.cleaned_data['bcode'],
                                   name     = self.cleaned_data['bname'],
                                   lattd    = self.cleaned_data['lattd'],
                                   longd    = self.cleaned_data['longd'],
                                   district = DeployDistrict.DISTRICT)


class AddGramPanchayat (forms.Form):
    sname       = SpacedROTextField (label = _("State Name"), initial = DeployDistrict.DISTRICT.state.name)
    scode       = SpacedROTextField (label = _("State Code"), initial = DeployDistrict.DISTRICT.state.get_code ())
    dname       = SpacedROTextField (label = _("District Name"), initial = DeployDistrict.DISTRICT.name)
    dcode       = SpacedROTextField (label = _("District Code"), initial = DeployDistrict.DISTRICT.get_code ())
    lattd       = LatLongField (label  = _("Gram Panchayat Latitude"))
    longd       = LatLongField (label  = _("Gram Panchayat Longitude"))

    block       = forms.ModelChoiceField (queryset = Block.objects.filter(district=DeployDistrict.DISTRICT), empty_label = "------", label=_("Block"))
    gpname      = SpacedTextField (label=_("Gram Panchayat Name"))
    gpcode      = SpacedTextField (label=_("Gram Panchayat Code"))

    def clean (self) :
        super (AddGramPanchayat, self).clean ()

        if 'gpcode' in self.cleaned_data and 'block' in self.cleaned_data:
            try:
                gpcode = int (self.cleaned_data['gpcode'])
            except ValueError:
                raise forms.ValidationError (_("Gram Panchayat code must be a number"))

            comp_gpcode = "%s.%03d" % (self.cleaned_data['block'].code, gpcode)
            if GramPanchayat.objects.filter (code = comp_gpcode).count () != 0:
                raise forms.ValidationError (_("Gram Panchayat code already exists"))

            self.cleaned_data ['gpcode'] = comp_gpcode
        return self.cleaned_data

    def save (self):
        return GramPanchayat.objects.create(code       = self.cleaned_data['gpcode'],
                                            name       = self.cleaned_data['gpname'],
                                            lattd      = self.cleaned_data['lattd'],
                                            longd      = self.cleaned_data['longd'],
                                            block      = self.cleaned_data['block'])


class AddVillage (forms.Form):
    sname       = SpacedROTextField (label = _("State Name"), initial = DeployDistrict.DISTRICT.state.name)
    scode       = SpacedROTextField (label = _("State Code"), initial = DeployDistrict.DISTRICT.state.get_code ())
    dname       = SpacedROTextField (label = _("District Name"), initial = DeployDistrict.DISTRICT.name)
    dcode       = SpacedROTextField (label = _("District Code"), initial = DeployDistrict.DISTRICT.get_code ())
    vname       = SpacedTextField (label   = _("Village Name"))
    vcode       = SpacedTextField (label   = _("Village Code"))
    lattd       = LatLongField (label  = _("Village Latitude"))
    longd       = LatLongField (label  = _("Village Longitude"))
    blockdata   = forms.ModelChoiceField (queryset = Block.objects.filter(district=DeployDistrict.DISTRICT), empty_label = "------", label=_("Block"))
    gp          = forms.ModelChoiceField (queryset = GramPanchayat.objects.none (), empty_label = '------', label=_("Gram Panchayat"))

    def __init__ (self, *args, **kwargs):
        super (AddVillage, self).__init__ (*args, **kwargs)

        for arg in args:
            if 'blockdata' in arg:
                try:
                    block = Block.objects.get (id = arg ['blockdata'])
                    self.fields ['gp'].queryset = block.grampanchayat_set.all ()
                except Block.DoesNotExist:
                    pass


    def clean (self) :
        super (AddVillage, self).clean ()
        if 'vcode' in self.cleaned_data and 'gp' in self.cleaned_data:
            try:
                vcode = int (self.cleaned_data['vcode'])
            except ValueError:
                raise forms.ValidationError (_("Village code must be a number"))

            comp_vcode = "%s.%03d" % (self.cleaned_data['gp'].code, vcode)
            if Village.objects.filter (code = comp_vcode).count () != 0:
                raise forms.ValidationError (_("Village code already exists"))

            self.cleaned_data ['vcode'] = comp_vcode
        return self.cleaned_data

    def save (self):
        vill = Village.objects.create(code                = self.cleaned_data['vcode'],
                                      name                = self.cleaned_data['vname'],
                                      lattd               = self.cleaned_data['lattd'],
                                      longd               = self.cleaned_data['longd'],
                                      grampanchayat       = self.cleaned_data['gp'],
                                      )


class AddComplaint (forms.Form):
    code        = SpacedTextField (label=_("Complaint Code"))
    summary     = SpacedTextField (max_length = 2000, label = _("Summary"))
    cclass      = SpacedTextField (max_length = 500, label = _("Classification"))
    defsmsnew   = SpacedTextAreaField (max_length = 2000, label = _("Default SMS New"), required = False)
    defsmsack   = SpacedTextAreaField (max_length = 2000, label = _("Default SMS Acknowledge"), required = False)
    defsmsopen  = SpacedTextAreaField (max_length = 2000, label = _("Default SMS Open"), required = False)
    defsmsres   = SpacedTextAreaField (max_length = 2000, label = _("Default SMS Resolved"), required = False)
    defsmsclo   = SpacedTextAreaField (max_length = 2000, label = _("Default SMS Closed"), required = False)
    mdg         = MultiNumberIdField (max_length = 20,   label = _("MDG Goals"), required = False)
    department  = forms.ModelChoiceField (label = _("Department"),
                                          queryset = ComplaintDepartment.objects.all(),
                                          empty_label = "------",
                                          widget=forms.Select (attrs = {'style' : 'width:100%'}))

    def clean_mdg (self):
        for goalnum in self.cleaned_data ['mdg']:
            if int (goalnum) < 1 or int (goalnum) > 8:
                raise forms.ValidationError (_("MDG goal must be between 1 and 8"))
        return self.cleaned_data ['mdg']


    def clean (self) :
        if 'code' in self.cleaned_data and 'department' in self.cleaned_data:
            compcode = "%s.%s" % (self.cleaned_data['department'].code, self.cleaned_data ['code'])
            if ComplaintType.objects.filter (code = compcode).count () != 0:
                raise forms.ValidationError (_("Complaint code already exists"))

            self.cleaned_data ['code'] = compcode
        return self.cleaned_data

    def save (self):
        comp = ComplaintType.objects.create(code         = self.cleaned_data['code'],
                                            summary      = self.cleaned_data['summary'],
                                            cclass       = self.cleaned_data['cclass'],
                                            defsmsnew    = self.cleaned_data['defsmsnew'],
                                            defsmsack    = self.cleaned_data['defsmsack'],
                                            defsmsres    = self.cleaned_data['defsmsres'],
                                            defsmsclo    = self.cleaned_data['defsmsclo'],
                                            department   = self.cleaned_data['department'])

        for goalnum in self.cleaned_data ['mdg']:
            mdg = MilleniumDevGoal.objects.get (goalnum = goalnum)
            ComplaintMDG.objects.create (complainttype = comp, mdg = mdg)


class EditBlk (forms.Form):
    objid  = forms.CharField (widget = forms.HiddenInput ())
    sname  = SpacedROTextField (label = _("State Name"), initial = DeployDistrict.DISTRICT.state.name)
    scode  = SpacedROTextField (label = _("State Code"), initial = DeployDistrict.DISTRICT.state.get_code ())
    dname  = SpacedROTextField (label = _("District Name"), initial = DeployDistrict.DISTRICT.name)
    dcode  = SpacedROTextField (label = _("District Code"), initial = DeployDistrict.DISTRICT.get_code ())
    lattd  = forms.DecimalField (label  = _("Gram Panchayat Latitude"), max_value = 180, min_value = -180)
    longd  = forms.DecimalField (label  = _("Gram Panchayat Longitude"), max_value = 180, min_value = -180)

    bname  = SpacedTextField (label=_("Block Name"))
    bcode  = SpacedTextField (label=_("Block Code"))

    def __init__(self, blkobj, *args, **kwargs) :
        super(EditBlk, self).__init__(*args,**kwargs)
        if blkobj != None:
            self.fields ['objid'].initial = blkobj.id
            self.fields ['bname'].initial = blkobj.name
            self.fields ['bcode'].initial = blkobj.get_code ()
            self.fields ['lattd'].initial = blkobj.lattd
            self.fields ['longd'].initial = blkobj.longd

    def clean (self):
        if 'objid' in self.cleaned_data and 'bcode' in self.cleaned_data:
            try:
                orgblkobj = Block.objects.get (id = self.cleaned_data['objid'])
                real_blkcode = "%s.%03s" % (DeployDistrict.DISTRICT.code, self.cleaned_data ['bcode'])
                if real_blkcode != orgblkobj.code:
                    blkobj = Block.objects.get (code = real_blkcode)
                    raise forms.ValidationError (_("This code can't be used. Block with this code already exists"))
            except Block.DoesNotExist:
                pass
            except Block.MultipleObjectsReturned:
                raise forms.ValidationError (_("This code can't be used. Block with this code already exists"))
        return self.cleaned_data


    def save (self):
        blk         = Block.objects.get(id = self.cleaned_data['objid'])

        oldcode = blk.code

        blk.code    = "%s.%03s" % (DeployDistrict.DISTRICT.code,
                                       self.cleaned_data ['bcode'])
        blk.name    = self.cleaned_data['bname']
        blk.lattd   = self.cleaned_data['lattd']
        blk.longd   = self.cleaned_data['longd']
        blk.save()

        if oldcode != blk.code:
            for gp in blk.grampanchayat_set.all ():
                gp.code = "%s.%03s.%03s" % (DeployDistrict.DISTRICT.code,
                                            self.cleaned_data ['bcode'],
                                            gp.get_code ())
                gp.save()
                for village in gp.village_set.all ():
                    village.code = "%s.%03s.%03s.%03s" % (DeployDistrict.DISTRICT.code,
                                                          self.cleaned_data ['bcode'],
                                                          village.get_gpcode(),
                                                          village.get_code ())
                    village.save()



class EditGp (forms.Form):
    objid  = forms.CharField (widget = forms.HiddenInput ())
    sname  = SpacedROTextField (label = _("State Name"), initial = DeployDistrict.DISTRICT.state.name)
    scode  = SpacedROTextField (label = _("State Code"), initial = DeployDistrict.DISTRICT.state.get_code ())
    dname  = SpacedROTextField (label = _("District Name"), initial = DeployDistrict.DISTRICT.name)
    dcode  = SpacedROTextField (label = _("District Code"), initial = DeployDistrict.DISTRICT.get_code ())
    lattd  = forms.DecimalField (label  = _("Gram Panchayat Latitude"), max_value = 180, min_value = -180)
    longd  = forms.DecimalField (label  = _("Gram Panchayat Longitude"), max_value = 180, min_value = -180)

    bname  = SpacedROTextField (label=_("Block Name"))
    bcode  = SpacedROTextField (label=_("Block Code"))
    gpname = SpacedTextField (label=_("Gram Panchayat Name"))
    gpcode = SpacedTextField (label=_("Gram Panchayat Code"))

    def __init__(self, gpobj, *args, **kwargs) :
        super(EditGp, self).__init__(*args,**kwargs)
        if gpobj != None:
            self.fields ['objid'].initial = gpobj.id
            self.fields ['bname'].initial = gpobj.block.name
            self.fields ['bcode'].initial = gpobj.block.get_code ()
            self.fields ['gpname'].initial = gpobj.name
            self.fields ['gpcode'].initial = gpobj.get_code ()
            self.fields ['lattd'].initial = gpobj.lattd
            self.fields ['longd'].initial = gpobj.longd

    def clean (self):
        if 'objid' in self.cleaned_data and 'bcode' in self.cleaned_data and 'gpcode' in self.cleaned_data:
            try:
                orggpobj = GramPanchayat.objects.get (id = self.cleaned_data['objid'])
                real_gpcode = "%s.%03s.%03s" % (DeployDistrict.DISTRICT.code, self.cleaned_data ['bcode'], self.cleaned_data ['gpcode'])
                if real_gpcode != orggpobj.code:
                    gpobj = GramPanchayat.objects.get (code = real_gpcode)
                    raise forms.ValidationError (_("This code can't be used. Gram Panchayat with this code exists within block"))
            except GramPanchayat.DoesNotExist:
                pass
            except GramPanchayat.MultipleObjectsReturned:
                raise forms.ValidationError (_("This code can't be used. Gram Panchayat with this code exists within block"))
        return self.cleaned_data


    def save (self):
        gp         = GramPanchayat.objects.get(id = self.cleaned_data['objid'])

        oldcode    = gp.code
        gp.code    = "%s.%03s.%03s" % (DeployDistrict.DISTRICT.code,
                                       self.cleaned_data ['bcode'],
                                       self.cleaned_data ['gpcode'])
        gp.name    = self.cleaned_data['gpname']
        gp.lattd   = self.cleaned_data['lattd']
        gp.longd   = self.cleaned_data['longd']
        gp.save()

        if oldcode != gp.code:
            for village in gp.village_set.all ():
                village.code = "%s.%03s.%03s.%03s" % (DeployDistrict.DISTRICT.code,
                                                      self.cleaned_data ['bcode'],
                                                      self.cleaned_data ['gpcode'],
                                                      village.get_code ())
                village.save()


class EditVillage (forms.Form):
    objid  = forms.CharField (widget  = forms.HiddenInput ())
    sname  = SpacedROTextField (label = _("State Name"), initial = DeployDistrict.DISTRICT.state.name)
    scode  = SpacedROTextField (label = _("State Code"), initial = DeployDistrict.DISTRICT.state.get_code ())
    dname  = SpacedROTextField (label = _("District Name"), initial = DeployDistrict.DISTRICT.name)
    dcode  = SpacedROTextField (label = _("District Code"), initial = DeployDistrict.DISTRICT.get_code ())
    bname  = SpacedROTextField (label =_("Block Name"))
    bcode  = SpacedROTextField (label =_("Block Code"))
    gpname = SpacedROTextField (label =_("Gram Panchayat Name"))
    gpcode = SpacedROTextField (label =_("Gram Panchayat Code"))

    vname  = SpacedTextField (label   = _("Village Name"))
    vcode  = SpacedTextField (label   = _("Village Code"))
    lattd  = forms.DecimalField (label= _("Village Latitude"), max_value = 180, min_value = -180)
    longd  = forms.DecimalField (label= _("Village Longitude"), max_value = 180, min_value = -180)


    def __init__(self, villobj, *args, **kwargs) :
        super(EditVillage, self).__init__(*args,**kwargs)
        if villobj != None:
            self.fields ['objid'].initial = villobj.id
            self.fields ['bname'].initial = villobj.grampanchayat.block.name
            self.fields ['bcode'].initial = villobj.grampanchayat.block.get_code ()
            self.fields ['gpname'].initial = villobj.grampanchayat.name
            self.fields ['gpcode'].initial = villobj.grampanchayat.get_code ()
            self.fields ['vname'].initial = villobj.name
            self.fields ['vcode'].initial = villobj.get_code ()
            self.fields ['lattd'].initial = villobj.lattd
            self.fields ['longd'].initial = villobj.longd

    def clean (self):
        if 'vcode' in self.cleaned_data and 'objid' in self.cleaned_data and 'bcode' in self.cleaned_data and 'gpcode' in self.cleaned_data:
            try:
                orgvillobj = Village.objects.get (id = self.cleaned_data['objid'])
                real_vcode = "%s.%03s.%03s.%03s" % (DeployDistrict.DISTRICT.code, self.cleaned_data ['bcode'], self.cleaned_data ['gpcode'],self.cleaned_data['vcode'])
                if real_vcode != orgvillobj.code:
                    villobj = Village.objects.get (code = real_vcode)
                    raise forms.ValidationError (_("This code can't be used. Village with this code exists within Gram Panchayat"))
            except Village.DoesNotExist:
                pass
            except Village.MultipleObjectsReturned:
                raise forms.ValidationError (_("This code can't be used. Village with this code exists within Gram Panchayat"))

        return self.cleaned_data


    def save (self):
        vil         = Village.objects.get(id = self.cleaned_data['objid'])
        vil.code    = "%s.%03s.%03s.%03s" % (DeployDistrict.DISTRICT.code,
                                             self.cleaned_data ['bcode'],
                                             self.cleaned_data ['gpcode'],
                                             self.cleaned_data ['vcode'])
        vil.name    = self.cleaned_data['vname']
        vil.lattd   = self.cleaned_data['lattd']
        vil.longd   = self.cleaned_data['longd']
        vil.save()




class EditDep (forms.Form):
    dname  = SpacedTextField (label = _("Department Name"))
    dcode  = SpacedTextField (label = _("Department Code"))
    objid  = forms.CharField (widget = forms.HiddenInput ())

    def __init__(self, depobj, *args, **kwargs) :
        super(EditDep, self).__init__(*args,**kwargs)
        if depobj != None:
            self.fields ['objid'].initial = depobj.id
            self.fields ['dname'].initial = depobj.name
            self.fields ['dcode'].initial = depobj.code

    def clean (self):
        if 'objid' in self.cleaned_data and 'dcode' in self.cleaned_data:
            try:
                orgdepobj = ComplaintDepartment.objects.get (id = self.cleaned_data['objid'])
                real_depcode =  self.cleaned_data ['dcode']
                if real_depcode != orgdepobj.code:
                    depobj = ComplaintDepartment.objects.get (code = real_depcode)
                    raise forms.ValidationError (_("Department code already exists please enter non-existing department code"))
            except ComplaintDepartment.DoesNotExist:
                pass
            except ComplaintDepartment.MultipleObjectsReturned:
                raise forms.ValidationError (_("Department code already exists please enter non-existing department code"))
        return self.cleaned_data


    def save (self):
        dep         = ComplaintDepartment.objects.get(id = self.cleaned_data['objid'])
        dep.code     = self.cleaned_data ['dcode']
        dep.name     = self.cleaned_data['dname']
        dep.save()

        for comp in dep.complainttype_set.all():
            comp.code = "%s.%03s" % (self.cleaned_data ['dcode'],
                                                  comp.get_code ())
            comp.save()


    code        = SpacedTextField (label=_("Complaint Code"))
    summary     = SpacedTextField (max_length = 2000, label = _("Summary"))
    cclass      = SpacedTextField (max_length = 500, label = _("Classification"))
    defsmsnew   = SpacedTextField (max_length = 2000, label = _("Default SMS New"), required = False)
    defsmsack   = SpacedTextField (max_length = 2000, label = _("Default SMS Acknowledge"), required = False)
    defsmsopen  = SpacedTextField (max_length = 2000, label = _("Default SMS Open"), required = False)
    defsmsres   = SpacedTextField (max_length = 2000, label = _("Default SMS Resolved"), required = False)
    defsmsclo   = SpacedTextField (max_length = 2000, label = _("Default SMS Closed"), required = False)
    mdg         = MultiNumberIdField (max_length = 20,   label = _("MDG Goals"), required = False)
    department  = forms.ModelChoiceField (label = _("Department"),
                                          queryset = ComplaintDepartment.objects.all(),
                                          empty_label = "------",
                                          widget=forms.Select (attrs = {'style' : 'width:100%'}))


class EditComp (forms.Form):
    dname       = SpacedROTextField (label = _("Department"))
    objid       = forms.CharField (widget = forms.HiddenInput ())
    hcode       = forms.CharField (widget = forms.HiddenInput ())
    code        = SpacedTextField (label=_("Complaint Code"))
    summary     = SpacedTextField (max_length = 2000, label = _("Summary"))
    cclass      = SpacedTextField (max_length = 500, label = _("Classification"))
    defsmsnew   = SpacedTextAreaField (max_length = 2000, label = _("Default SMS New"), required = False)
    defsmsack   = SpacedTextAreaField (max_length = 2000, label = _("Default SMS Acknowledge"), required = False)
    defsmsopen  = SpacedTextAreaField (max_length = 2000, label = _("Default SMS Open"), required = False)
    defsmsres   = SpacedTextAreaField (max_length = 2000, label = _("Default SMS Resolved"), required = False)
    defsmsclo   = SpacedTextAreaField (max_length = 2000, label = _("Default SMS Closed"), required = False)
    mdg         = MultiNumberIdField (max_length = 20,   label = _("MDG Goals"), required = False)

    def __init__(self, compobj, *args, **kwargs) :
        super(EditComp, self).__init__(*args,**kwargs)
        if compobj != None:
            self.fields ['objid'].initial       = compobj.id
            self.fields ['code'].initial        = compobj.get_code()
            self.fields ['hcode'].initial       = compobj.get_department()
            self.fields ['dname'].initial       = compobj.department.name
            self.fields ['summary'].initial     = compobj.summary
            self.fields ['cclass'].initial      = compobj.cclass
            self.fields ['defsmsnew'].initial   = compobj.defsmsnew
            self.fields ['defsmsack'].initial   = compobj.defsmsack
            self.fields ['defsmsopen'].initial  = compobj.defsmsopen
            self.fields ['defsmsres'].initial   = compobj.defsmsres
            self.fields ['defsmsclo'].initial   = compobj.defsmsclo
            self.fields ['mdg'].initial         = ', '.join (sorted ([str (m.mdg.goalnum) for m in compobj.complaintmdg_set.all ()]))


    def clean_mdg (self):
        for goalnum in self.cleaned_data ['mdg']:
            if int (goalnum) < 1 or int (goalnum) > 8:
                raise forms.ValidationError (_("MDG goal must be between 1 and 8"))
        return self.cleaned_data ['mdg']


    def clean (self):
        if 'objid' in self.cleaned_data and 'hcode' in self.cleaned_data and 'code' in self.cleaned_data:
            try:
                orgcompobj = ComplaintType.objects.get (id = self.cleaned_data['objid'])
                real_compcode =  "%s.%03s" % (self.cleaned_data['hcode'],self.cleaned_data ['code'])
                if real_compcode != orgcompobj.code:
                    compobj = ComplaintType.objects.get (code = real_compcode)
                    raise forms.ValidationError (_("Complaint code already exists please enter non-existing complaint code"))
            except ComplaintType.DoesNotExist:
                pass
            except ComplaintType.MultipleObjectsReturned:
                raise forms.ValidationError (_("Complaint code already exists please enter non-existing complaint code"))
        return self.cleaned_data


    def save (self):
        comp              = ComplaintType.objects.get(id = self.cleaned_data['objid'])
        comp.code         = "%s.%s" % (self.cleaned_data['hcode'],self.cleaned_data ['code'])
        comp.summary      = self.cleaned_data['summary']
        comp.cclass       = self.cleaned_data['cclass']
        comp.defsmsnew    = self.cleaned_data['defsmsnew']
        comp.defsmsack    = self.cleaned_data['defsmsack']
        comp.defsmsres    = self.cleaned_data['defsmsres']
        comp.defsmsclo    = self.cleaned_data['defsmsclo']
        comp.save()

        compmdg_ids = [m.id for m in comp.complaintmdg_set.all ()]
        foundmdgs = []
        for goalnum in self.cleaned_data ['mdg']:
            mdg = MilleniumDevGoal.objects.get (goalnum = goalnum)
            try:
                mdgobj = comp.complaintmdg_set.get (mdg__goalnum = goalnum)
                foundmdgs.append (mdgobj.id)
            except ComplaintMDG.DoesNotExist:
                mdgobj = ComplaintMDG.objects.create (complainttype = comp, mdg = mdg)

        for objid in compmdg_ids:
            if objid in foundmdgs:
                pass
            else:
                comp.complaintmdg_set.get (id = objid).delete ()

        return comp

