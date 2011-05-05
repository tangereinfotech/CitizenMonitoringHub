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

from django import forms

LOCATION_REGEX = r'^ *(?P<village>\w+) *\[(?P<gp>\w+), *(?P<block>\w+)\] *$|^ *(?P<full>\w+) *$'

from datetime import datetime

from cmh.issuemgr.constants import VILLAGES, COMPLAINT_TYPES, STATUS_NEW, STATUS_ACK
from cmh.issuemgr.constants import STATUSES, DEPARTMENTS
from cmh.issuemgr.models import Complaint, ComplaintItem, StatusTransition
from cmh.issuemgr.utils import update_complaint_sequence
from cmh.usermgr.utils import get_or_create_citizen
from cmh.common.models import Category, Attribute

class ComplaintForm (forms.Form):
    logdate     = forms.DateField (input_formats = ('%d/%m/%Y',))
    description = forms.CharField (widget=forms.Textarea ( attrs = {'style' :
                                                                    "width:348px;border-style:inset;",
                                                                    "rows" : "6"}))
    locationid  = forms.IntegerField (widget = forms.HiddenInput ())
    locationdesc = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px'}))
    yourname    = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                      'maxlength' : '100'}))
    yourmobile  = forms.IntegerField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                         'maxlenght' : '15'}))
    categoryid  = forms.IntegerField (required = False, widget = forms.HiddenInput ())
    categorydesc = forms.CharField (required = False,
                                    widget = forms.TextInput (attrs = {'style' : 'width:348px'}))

    def clean_locationid (self):
        try:
            village = VILLAGES.get (id = self.cleaned_data ['locationid'])
        except:
            raise forms.ValidationError ("Location code is not correct")
        return self.cleaned_data ['locationid']

    def clean_categoryid (self):
        if self.cleaned_data ['categoryid'] != None:
            try:
                category = COMPLAINT_TYPES.get (id = self.cleaned_data ['categoryid'])
            except:
                raise forms.ValidationError ("Complaint Type is not correct")
        return self.cleaned_data ['categoryid']

    def save (self, need_category = False):
        location = VILLAGES.get (id = self.cleaned_data ['locationid'])
        citizen = get_or_create_citizen (self.cleaned_data ['yourmobile'],
                                         self.cleaned_data ['yourname'])

        if self.cleaned_data ['categoryid'] != None:
            complaint_base = COMPLAINT_TYPES.get (id = self.cleaned_data ['categoryid'])
            department = complaint_base.parent
        else:
            complaint_base = None
            department = None

        cpl = Complaint.objects.create (base = complaint_base,
                                        complaintno = None,
                                        description = self.cleaned_data ['description'],
                                        department  = department,
                                        curstate = STATUS_NEW,
                                        filedby = citizen,
                                        logdate = self.cleaned_data ['logdate'],
                                        location = location,
                                        original = None)
        update_complaint_sequence (cpl)
        return cpl

class AcceptComplaintForm (forms.Form):
    logdate     = forms.DateField (input_formats = ('%d/%m/%Y',))
    description = forms.CharField (widget=forms.Textarea ( attrs = {'style' :
                                                                    "width:348px;border-style:inset;",
                                                                    "rows" : "6"}))
    locationid  = forms.IntegerField (widget = forms.HiddenInput ())
    locationdesc = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px'}))
    yourname    = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                      'maxlength' : '100'}))
    yourmobile  = forms.IntegerField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                         'maxlenght' : '15'}))
    categoryid  = forms.IntegerField (widget = forms.HiddenInput ())
    categorydesc = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px'}))

    def clean_locationid (self):
        try:
            village = VILLAGES.get (id = self.cleaned_data ['locationid'])
        except:
            raise forms.ValidationError ("Location code is not correct")
        return self.cleaned_data ['locationid']

    def clean_categoryid (self):
        try:
            category = COMPLAINT_TYPES.get (id = self.cleaned_data ['categoryid'])
        except:
            raise forms.ValidationError ("Complaint Type is not correct")
        return self.cleaned_data ['categoryid']

    def save (self, need_category = False):
        location       = VILLAGES.get (id = self.cleaned_data ['locationid'])
        citizen = get_or_create_citizen (self.cleaned_data ['yourmobile'],
                                         self.cleaned_data ['yourname'])

        complaint_base = COMPLAINT_TYPES.get (id = self.cleaned_data ['categoryid'])
        department = complaint_base.parent

        cpl = Complaint.objects.create (base = complaint_base,
                                        complaintno = None,
                                        description = self.cleaned_data ['description'],
                                        department  = department,
                                        curstate = STATUS_NEW,
                                        filedby = citizen,
                                        logdate = self.cleaned_data ['logdate'],
                                        location = location,
                                        original = None)
        update_complaint_sequence (cpl)

        accept_cpl = cpl.clone ()
        accept_cpl.curstate = STATUS_ACK
        accept_cpl.save ()

        return accept_cpl


class ComplaintLocationBox (forms.Form):
    term = forms.RegexField (regex = LOCATION_REGEX)


class ComplaintTypeBox (forms.Form):
    term = forms.CharField ()


class ComplaintDepartmentBox (forms.Form):
    term = forms.CharField ()


class ComplaintUpdateForm (forms.Form):
    complaintno = forms.CharField (required = True)
    newstatus = forms.ChoiceField (required = True)
    revlocationid = forms.IntegerField (widget = forms.HiddenInput (), required = False)
    revlocationdesc = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:100%'}),
                                   required = False)
    revdepartmentid = forms.IntegerField (widget = forms.HiddenInput (), required = False)
    revdepartmentdesc = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:100%'}),
                                     required = False)
    comment = forms.CharField (widget = forms.Textarea (attrs = {'style' : 'width:100%',
                                                                 'cols' : '40',
                                                                 'rows' : '6'}),
                               required = True)

    def __init__ (self, complaint, *args, **kwargs):
        super (ComplaintUpdateForm, self).__init__ (*args, **kwargs)
        st = StatusTransition.objects.get (curstate = complaint.curstate)
        newstates = st.newstates.all ()

        self.fields ['newstatus'] = \
                    forms.ChoiceField (required = True,
                                       choices = ([(-1, '----')] +
                                                  [(status.id, status.get_value ())
                                                   for status in newstates]),
                                       widget = forms.Select (attrs = {'style': 'width:100%'}))

    def clean_revlocationid (self):
        if self.cleaned_data ['revlocationid'] != None:
            try:
                village = VILLAGES.get (id = self.cleaned_data ['revlocationid'])
            except:
                raise forms.ValidationError ("Location code is not correct")
            return self.cleaned_data ['revlocationid']
        else:
            return None

    def clean_revdepartmentid (self):
        if self.cleaned_data ['revdepartmentid'] != None:
            try:
                department = DEPARTMENTS.get (id = self.cleaned_data ['revdepartmentid'])
            except:
                raise forms.ValidationError ('Department id is not correct')
            return self.cleaned_data ['revdepartmentid']
        else:
            return None

    def clean_comment (self):
        if len (self.cleaned_data ['comment']) == 0:
            raise forms.ValidationError ("Comment is mandatory")
        return self.cleaned_data ['comment']

    def clean_newstatus (self):
        try:
            complaint = Complaint.objects.get (complaintno = self.cleaned_data ['complaintno'],
                                               latest = True)
        except:
            raise forms.ValidationError ('Complaint number is invalid')

        if self.cleaned_data ['newstatus'] != "-1":
            try:
                checkstatus = STATUSES.get (id = self.cleaned_data ['newstatus'])
                st = StatusTransition.objects.get (curstate = complaint.curstate)
                is_valid = st.newstates.get (id = checkstatus.id)
            except Attribute.DoesNotExist:
                raise forms.ValidationError ("New status is not a valid status code")
            except StatusTransition.DoesNotExist:
                raise forms.ValidationError ("That status transition is not allowed")
        else:
             raise forms.ValidationError ("Please select a valid next status")
        return self.cleaned_data ['newstatus']

    def save (self):
        complaint = Complaint.objects.get (complaintno = self.cleaned_data ['complaintno'],
                                           latest = True)
        newver = complaint.clone ()

        newver.curstate = STATUSES.get (id = self.cleaned_data ['newstatus'])
        newver.description = self.cleaned_data ['comment']

        if self.cleaned_data ['revlocationid'] != None:
            newver.location = VILLAGES.get (id = self.cleaned_data ['revlocationid'])

        if self.cleaned_data ['revdepartmentid'] != None:
            newver.department = DEPARTMENTS.get (id = self.cleaned_data ['revdepartmentid'])

        newver.save ()
        return newver



