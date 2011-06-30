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

from cmh.smsgateway.models import TextMessage

from cmh.common.models import Country, State, District
from cmh.common.models import Block, GramPanchayat, Village
from cmh.common.models import ComplaintType, ComplaintDepartment, ComplaintType
from cmh.common.models import ComplaintStatus, StatusTransition

from cmh.issuemgr.constants import STATUS_NEW, STATUS_ACK, STATUS_OPEN, STATUS_RESOLVED, STATUS_CLOSED, STATUS_REOPEN

from cmh.issuemgr.models import Complaint
from cmh.issuemgr.utils import update_complaint_sequence

from cmh.usermgr.utils import get_or_create_citizen

from cmh.common.constants import UserRoles

from cmh.common.fields import MultiNumberIdField, FormattedDateField

from cmh.common.utils import debug
from cmh.issuemgr.constants import GENDER_CHOICES, COMMUNITY_CHOICES

class ComplaintForm (forms.Form):
    logdate     = forms.DateField (input_formats = ('%d/%m/%Y',),
                                   widget = forms.TextInput (attrs = {'autocomplete' : 'off'}))
    description = forms.CharField (widget=forms.Textarea ( attrs = {'style' :
                                                                    "width:348px;border-style:inset;",
                                                                    "rows" : "6"}))
    locationid  = forms.IntegerField (widget = forms.HiddenInput ())
    locationdesc = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                       'autocomplete' : 'off'}))
    yourname    = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                      'maxlength' : '100'}))
    yourmobile  = forms.IntegerField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                         'maxlenght' : '15'}))
    categoryid  = forms.IntegerField (required = False, widget = forms.HiddenInput ())
    categorydesc = forms.CharField (required = False,
                                    widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                       'autocomplete' : 'off'}))

    def clean_locationid (self):
        try:
            village = Village.objects.get (id = self.cleaned_data ['locationid'])
        except:
            raise forms.ValidationError ("Location code is not correct")
        return self.cleaned_data ['locationid']

    def clean_categoryid (self):
        if self.cleaned_data ['categoryid'] != None:
            try:
                category = ComplaintType.objects.get (id = self.cleaned_data ['categoryid'])
            except:
                raise forms.ValidationError ("Complaint Type is not correct")
        return self.cleaned_data ['categoryid']

    def save (self, user):
        location = Village.objects.get (id = self.cleaned_data ['locationid'])
        citizen = get_or_create_citizen (self.cleaned_data ['yourmobile'],
                                         self.cleaned_data ['yourname'])

        assignto = None
        if self.cleaned_data ['categoryid'] != None:
            complaint_base = ComplaintType.objects.get (id = self.cleaned_data ['categoryid'])
            department = complaint_base.department
            officials = department.official_set.all ()
            if officials.count () > 0:
                assignto = officials [0]
        else:
            complaint_base = None
            department = None

        cpl = Complaint.objects.create (complainttype = complaint_base,
                                        complaintno = None,
                                        description = self.cleaned_data ['description'],
                                        department  = department,
                                        curstate = STATUS_NEW,
                                        filedby = citizen,
                                        logdate = self.cleaned_data ['logdate'],
                                        location = location,
                                        original = None,
                                        creator = user,
                                        assignto = assignto)
        update_complaint_sequence (cpl)
        return cpl

class AcceptComplaintForm (forms.Form):
    logdate         = forms.DateField (input_formats = ('%d/%m/%Y',),
                                   widget = forms.TextInput (attrs = {'autocomplete' : 'off'}))
    description     = forms.CharField (widget=forms.Textarea ( attrs = {'style' :
                                                                    "width:348px;border-style:inset;",
                                                                    "rows" : "6"}))
    locationid      = forms.IntegerField (widget = forms.HiddenInput ())
    locationdesc    = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                       'autocomplete' : 'off'}))
    yourname        = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                      'maxlength' : '100'}))
    yourmobile      = forms.IntegerField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                         'maxlenght' : '15'}))
    categoryid      = forms.IntegerField (widget = forms.HiddenInput ())
    categorydesc    = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:348px',
                                                                       'autocomplete' : 'off'}))
    gender          = forms.CharField (widget = forms.RadioSelect (choices = GENDER_CHOICES), required = False, initial = 'Unspecified')

    community       = forms.CharField (widget = forms.RadioSelect (choices = COMMUNITY_CHOICES), required = False, initial = 'Unspecified')

    def clean_locationid (self):
        try:
            village = Village.objects.get (id = self.cleaned_data ['locationid'])
        except:
            raise forms.ValidationError ("Location code is not correct")
        return self.cleaned_data ['locationid']

    def clean_categoryid (self):
        try:
            category = ComplaintType.objects.get (id = self.cleaned_data ['categoryid'])
        except:
            raise forms.ValidationError ("Complaint Type is not correct")
        return self.cleaned_data ['categoryid']

    def save (self, user):
        location = Village.objects.get (id = self.cleaned_data ['locationid'])
        citizen = get_or_create_citizen (self.cleaned_data ['yourmobile'],
                                         self.cleaned_data ['yourname'])

        complaint_base = ComplaintType.objects.get (id = self.cleaned_data ['categoryid'])
        department = complaint_base.department
        officials = department.official_set.all ()
        if officials.count () > 0:
            assignto = officials [0]
        else:
            assignto = None

        cpl = Complaint.objects.create (complainttype = complaint_base,
                                        complaintno = None,
                                        description = self.cleaned_data ['description'],
                                        department  = department,
                                        curstate = STATUS_NEW,
                                        filedby = citizen,
                                        logdate = self.cleaned_data ['logdate'],
                                        location = location,
                                        original = None,
                                        creator = user,
                                        assignto = assignto)
        update_complaint_sequence (cpl)

        accept_cpl = cpl.clone (user)
        accept_cpl.curstate = STATUS_ACK
        accept_cpl.save ()

        message = cpl.complainttype.defsmsack.replace ('____', cpl.filedby.mobile)
        TextMessage.objects.queue_text_message (cpl.filedby.mobile, message)

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
    revcategoryid = forms.IntegerField (widget = forms.HiddenInput (), required = False)
    revcategorydesc = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:100%'}),
                                       required = False)
    comment = forms.CharField (widget = forms.Textarea (attrs = {'style' : 'width:100%',
                                                                 'cols' : '40',
                                                                 'rows' : '6'}),
                               required = True)
    gender          = forms.CharField (widget = forms.RadioSelect (choices = (('Male', 'Male'),
                                                                              ('Female', 'Female'),
                                                                              ('Unspecified','Unspecified'))),
                                       required = False,
                                       initial = 'Unspecified')

    community       = forms.CharField (widget = forms.RadioSelect (choices = (('SC/ST', 'SC / ST'),
                                                                              ('Others', 'Others'),
                                                                              ('Unspecified','Unspecified'))),
                                       required = False,
                                       initial = 'Unspecified')


    def __init__ (self, complaint, newstates, *args, **kwargs):
        super (ComplaintUpdateForm, self).__init__ (*args, **kwargs)

        self.newstates = newstates

        self.fields ['newstatus'] = \
                    forms.ChoiceField (required = True,
                                       choices = ([(-1, '----')] +
                                                  [(status.id, status.name)
                                                   for status in newstates]),
                                       widget = forms.Select (attrs = {'style': 'width:100%'}))

        if complaint.location != None:
            self.fields ['revlocationid'] = forms.IntegerField (widget = forms.HiddenInput (), required = False, initial = complaint.location.id)
            self.fields ['revlocationdesc'] = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:100%'}),
                                                               required = False,
                                                               initial = complaint.location.name)
        if complaint.complainttype != None:
            self.fields ['revcategoryid'] = forms.IntegerField (widget = forms.HiddenInput (), required = False, initial = complaint.complainttype.id)
            self.fields ['revcategorydesc'] = forms.CharField (widget = forms.TextInput (attrs = {'style' : 'width:100%'}),
                                                               required = False,
                                                               initial = complaint.complainttype.summary)
        self.fields ['comment'] = forms.CharField (widget = forms.Textarea (attrs = {'style' : 'width:100%',
                                                                 'cols' : '40',
                                                                 'rows' : '6'}),
                                                   required = True,
                                                   initial = complaint.description)


    def clean_revlocationid (self):
        if self.cleaned_data ['revlocationid'] != None:
            try:
                village = Village.objects.get (id = self.cleaned_data ['revlocationid'])
            except:
                raise forms.ValidationError ("Location code is not correct")
            return self.cleaned_data ['revlocationid']
        else:
            return None

    def clean_revcategoryid (self):
        if self.cleaned_data ['revcategoryid'] != None:
            try:
                ct = ComplaintType.objects.get (id = self.cleaned_data ['revcategoryid'])
            except:
                raise forms.ValidationError ('Complaint Category is not correct')
            return self.cleaned_data ['revcategoryid']
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
                checkstatus = ComplaintStatus.objects.get (id = self.cleaned_data ['newstatus'])
                is_valid = self.newstates.get (id = checkstatus.id)
            except ComplaintStatus.DoesNotExist:
                raise forms.ValidationError ("New status is not a valid status code")
            except StatusTransition.DoesNotExist:
                raise forms.ValidationError ("That status transition is not allowed")
        else:
             raise forms.ValidationError ("Please select a valid next status")
        return self.cleaned_data ['newstatus']

    def save (self, user):
        complaint = Complaint.objects.get (complaintno = self.cleaned_data ['complaintno'], latest = True)

        newver = complaint.clone (user)

        newver.curstate = ComplaintStatus.objects.get (id = self.cleaned_data ['newstatus'])
        newver.description = self.cleaned_data ['comment']

        if self.cleaned_data ['revlocationid'] != None:
            newver.location = Village.objects.get (id = self.cleaned_data ['revlocationid'])

        if self.cleaned_data ['revcategoryid'] != None:
            assignto = None
            complaint_base = ComplaintType.objects.get (id = self.cleaned_data ['revcategoryid'])
            department = complaint_base.department
            officials = department.official_set.all ()
            if officials.count () > 0:
                assignto = officials [0]
            else:
                assignto = None

            newver.complainttype = ComplaintType.objects.get (id = self.cleaned_data ['revcategoryid'])
            newver.department = newver.complainttype.department
            newver.assignto = assignto
            newver.gender = self.cleaned_data ['gender']
            newver.community = self.cleaned_data ['community']
        newver.save ()

        # Update the "original" issue if the new status is ACK state since the
        # issue has been made actionable
        if complaint.curstate == STATUS_NEW and newver.curstate == STATUS_ACK:
            original = newver.original
            original.complainttype = newver.complainttype
            original.location = newver.location
            original.department = newver.complainttype.department
            original.assignto = newver.assignto
            original.gender = newver.gender
            original.community = newver.community
            original.save ()

        if newver.curstate == STATUS_ACK:
            message = newver.complainttype.defsmsack.replace ('____', newver.complaintno)
        elif newver.curstate == STATUS_OPEN:
            message = newver.complainttype.defsmsopen.replace ('____', newver.complaintno)
        elif newver.curstate == STATUS_RESOLVED:
            message = newver.complainttype.defsmsres.replace ('____', newver.complaintno)
        elif newver.curstate == STATUS_CLOSED:
            message = newver.complainttype.defsmsclo.replace ('____', newver.complaintno)
        elif newver.curstate == STATUS_REOPEN:
            message = newver.complainttype.defsmsnew.replace ('____', newver.complaintno)
        else:
            message = None

        if message != None:
            debug ("Queuing message on change of status")
            TextMessage.objects.queue_text_message (newver.filedby.mobile, message)

        return newver


class HotComplaintForm (forms.Form):
    departments = MultiNumberIdField ()
    stdate      = FormattedDateField ()
    endate      = FormattedDateField ()


class ComplaintTrackForm (forms.Form):
    complaintno = forms.CharField (label="Complaint No.",
                                   widget = forms.TextInput (attrs = {'size': '50',
                                                                      'autocomplete' : 'off'}))


class ComplaintDisplayParams (forms.Form):
    departments = MultiNumberIdField ()
    datalevel   = forms.ChoiceField (choices = (("villg", "villg"),
                                                ("gramp", "gramp"),
                                                ("block", "block"),
                                                ("distt", "distt"),
                                                ("state", "state")))
    stdate      = FormattedDateField ();
    endate      = FormattedDateField ();

class Report (forms.Form):
    strtdate     = forms.DateField (input_formats = ('%d/%m/%Y',),
                                    widget = forms.TextInput (attrs = {'autocomplete' : 'off'}),
                                    required = False)
    enddate      = forms.DateField (input_formats = ('%d/%m/%Y',),
                                    widget = forms.TextInput (attrs = {'autocomplete' : 'off'}),
                                    required = False)
    departments  = forms.ModelMultipleChoiceField(queryset = ComplaintDepartment.objects.all(),
                                                  label    = "Available Departments",
                                                  widget   = forms.Select (attrs = {'style' : 'width:300px;height:150px;',
                                                                                  'multiple' : 'multiple',}),
                                                  required = False)
    selecteddep  = forms.ModelMultipleChoiceField(queryset = ComplaintDepartment.objects.none(),
                                                  label    = "Selected Departments",
                                                  widget   = forms.Select (attrs = {'style' : 'width:300px;height:150px;',
                                                                                  'multiple' : 'multiple',}),
                                                  required = False)
    sel_loc      = forms.MultipleChoiceField( widget = forms.Select (attrs = {'style' : 'width:300px;height:150px;',
                                                                                  'multiple' : 'multiple',}),
                                              required = False)
    block        = forms.ModelChoiceField(queryset = Block.objects.all(), empty_label = "------",
                                          widget   = forms.Select (attrs = { 'style' : 'width:100%'}),
                                          required = False)
    gp           = forms.ModelChoiceField (queryset = GramPanchayat.objects.none (),
                                           empty_label = '------',
                                           widget   = forms.Select (attrs = { 'style' : 'width:100%'}),
                                           required = False)
    village      = forms.ModelChoiceField (queryset = Village.objects.none (),empty_label = '------',
                                           widget   = forms.Select (attrs = { 'style' : 'width:100%'}),
                                           required = False)
    def __init__ (self, repdata, *args, **kwargs):
        super (Report, self).__init__ (*args, **kwargs)
        if repdata != None:
            self.fields['departments'].queryset = ComplaintDepartment.objects.exclude(id__in = [d.id for d in repdata.department.all ()])
            self.fields['selecteddep'].queryset = repdata.department.all ()
            self.fields['gp'].queryset          = repdata.gp.all()
            self.fields['village'].queryset     = repdata.village.all()




class LocationStatsForm (ComplaintDisplayParams):
    locid = forms.IntegerField ()

class ReportForm(forms.Form):
    strtdate     = forms.DateField (input_formats = ('%d/%m/%Y',),
                                    widget = forms.TextInput (attrs = {'autocomplete' : 'off'}))
    enddate      = forms.DateField (input_formats = ('%d/%m/%Y',),
                                    widget = forms.TextInput (attrs = {'autocomplete' : 'off'}))
