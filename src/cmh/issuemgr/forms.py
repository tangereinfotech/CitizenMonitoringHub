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
from django.utils.translation import ugettext as _

from cmh.smsgateway.utils import queue_complaint_update_sms

from cmh.common.models import Country, State, District
from cmh.common.models import Block, GramPanchayat, Village
from cmh.common.models import ComplaintType, ComplaintDepartment, ComplaintType
from cmh.common.models import ComplaintStatus, StatusTransition

from cmh.issuemgr.constants import STATUS_NEW, STATUS_ACK, STATUS_OPEN, STATUS_RESOLVED, STATUS_CLOSED, STATUS_REOPEN

from cmh.issuemgr.models import Complaint, ComplaintClosureMetric
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
                                    widget = forms.HiddenInput (attrs = {'style' : 'width:348px',
                                                                       'autocomplete' : 'off'}))
    filename    = forms.FileField (label = _("Upload Evidence:"), required = False)

    def clean_locationid (self):
        try:
            village = Village.objects.get (id = self.cleaned_data ['locationid'])
        except:
            raise forms.ValidationError (_("Location code is not correct"))
        return self.cleaned_data ['locationid']

    def clean_categoryid (self):
        if self.cleaned_data ['categoryid'] != None:
            try:
                category = ComplaintType.objects.get (id = self.cleaned_data ['categoryid'])
            except:
                raise forms.ValidationError (_("Complaint Type is not correct"))
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

        ComplaintClosureMetric.objects.create (complaintno = cpl.complaintno)

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

    filename        = forms.FileField (label = _("Upload Evidence:"), required = False)

    def clean_locationid (self):
        try:
            village = Village.objects.get (id = self.cleaned_data ['locationid'])
        except:
            raise forms.ValidationError (_("Location code is not correct"))
        return self.cleaned_data ['locationid']

    def clean_categoryid (self):
        try:
            category = ComplaintType.objects.get (id = self.cleaned_data ['categoryid'])
        except:
            raise forms.ValidationError (_("Complaint Type is not correct"))
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
                                        assignto = assignto,
                                        gender = self.cleaned_data ['gender'],
                                        community = self.cleaned_data ['community'])
        update_complaint_sequence (cpl)

        ComplaintClosureMetric.objects.create (complaintno = cpl.complaintno)

        accept_cpl = cpl.clone (user)
        accept_cpl.curstate = STATUS_ACK
        accept_cpl.save ()


        message = None
        ct = cpl.complainttype
        if ct.defsmsack != None and len (ct.defsmsack.strip ()) != 0:
            message = ct.defsmsnew

        if message == None:
            if ct.defsmsnew != None and len (ct.defsmsnew.strip ()) != 0:
                message = ct.defsmsnew

        if message != None:
            queue_complaint_update_sms (cpl.filedby.mobile, message, cpl)

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
    gender          = forms.CharField (widget = forms.RadioSelect (choices = ((_('Male'), _('Male')),
                                                                              (_('Female'), _('Female')),
                                                                              (_('Unspecified'),_('Unspecified')))),
                                       required = False,
                                       initial = _('Unspecified'))

    community       = forms.CharField (widget = forms.RadioSelect (choices = ((_('SC/ST'), _('SC / ST')),
                                                                              (_('Others'), _('Others')),
                                                                              (_('Unspecified'),_('Unspecified')))),
                                       required = False,
                                       initial = _('Unspecified'))

    filename        = forms.FileField (label = _("Upload Evidence:"), required = False)

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


    def clean_revlocationid (self):
        if self.cleaned_data ['revlocationid'] != None:
            try:
                village = Village.objects.get (id = self.cleaned_data ['revlocationid'])
            except:
                raise forms.ValidationError (_("Location code is not correct"))
        return self.cleaned_data ['revlocationid']

    def clean_revcategoryid (self):
        if self.cleaned_data ['revcategoryid'] != None:
            try:
                ct = ComplaintType.objects.get (id = self.cleaned_data ['revcategoryid'])
            except:
                raise forms.ValidationError (_('Complaint Category is not correct'))
        return self.cleaned_data ['revcategoryid']

    def clean_comment (self):
        if len (self.cleaned_data ['comment']) == 0:
            raise forms.ValidationError (_("Comment is mandatory"))
        return self.cleaned_data ['comment']

    def clean_newstatus (self):
        try:
            complaint = Complaint.objects.get (complaintno = self.cleaned_data ['complaintno'],
                                               latest = True)
        except:
            raise forms.ValidationError (_('Complaint number is invalid'))

        if self.cleaned_data ['newstatus'] != "-1":
            try:
                checkstatus = ComplaintStatus.objects.get (id = self.cleaned_data ['newstatus'])
                is_valid = self.newstates.get (id = checkstatus.id)
            except ComplaintStatus.DoesNotExist:
                raise forms.ValidationError (_("New status is not a valid status code"))
            except StatusTransition.DoesNotExist:
                raise forms.ValidationError (_("That status transition is not allowed"))
        else:
             raise forms.ValidationError (_("Please select a valid next status"))
        return self.cleaned_data ['newstatus']

    def clean (self):
        try:
            complaint = Complaint.objects.get (complaintno = self.cleaned_data ['complaintno'], latest = True)
        except:
            raise forms.ValidationError (_('Complaint number is invalid'))

        if self.cleaned_data ['revcategoryid'] == None:
            if ((complaint.original != None and complaint.original.complainttype == None) or
                (complaint.complainttype == None)):
                raise forms.ValidationError (_("Complaint Type is mandatory"))
        return self.cleaned_data


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

        if newver.curstate == STATUS_CLOSED:
            now_time = datetime.now ()
            ccms = ComplaintClosureMetric.objects.filter (complaintno = newver.complaintno)
            origs = Complaint.objects.filter (complaintno = newver.complaintno, curstate = STATUS_NEW).order_by ('created')
            if ccms.count () == 1:
                if origs.count () == 1:
                    orig = origs [0]
                    ccm = ccms [0]
                    ccm.closed = now_time
                    period = now_time - orig.created
                    ccm.period = period.days + ((period.seconds * 1.0) / (3600 * 24))
                    ccm.save ()
                else:
                    debug ("Multiple complaint objects with status_new for complaint : " + newver.complaintno)
                    debug ("... Doing nothing")
            else:
                debug ("Multiple complaint closure metrics exist for this complaint : " + newver.complaintno)
                debug ("... Doing nothing")


        if newver.curstate == STATUS_ACK:
            message = newver.complainttype.defsmsack
        elif newver.curstate == STATUS_OPEN:
            message = newver.complainttype.defsmsopen
        elif newver.curstate == STATUS_RESOLVED:
            message = newver.complainttype.defsmsres
        elif newver.curstate == STATUS_CLOSED:
            message = newver.complainttype.defsmsclo
        elif newver.curstate == STATUS_REOPEN:
            message = newver.complainttype.defsmsnew
        else:
            message = None

        if message != None:
            queue_complaint_update_sms (newver.filedby.mobile, message, newver)
        else:
            debug ("[%s]{%s}: " % (newver.complaintno, str (newver.curstate)) +
                   "Message is empty -- not queueing >> from forms.py: issuemgr")

        return newver


class HotComplaintForm (forms.Form):
    departments = MultiNumberIdField ()
    stdate      = FormattedDateField ()
    endate      = FormattedDateField ()


class ComplaintTrackForm (forms.Form):
    complaintno = forms.CharField (label=_("Complaint No."),
                                   widget = forms.TextInput (attrs = {'size': '50',
                                                                      'autocomplete' : 'off'}))

class DateIndex (forms.Form):
    stdate = forms.DateField (input_formats = ('%d/%m/%Y',),
                              widget = forms.TextInput (attrs = {'autocomplete': 'off',
                                                                 'style' : 'width:80px'}))
    endate = forms.DateField (input_formats = ('%d/%m/%Y',),
                              widget = forms.TextInput (attrs = {'autocomplete': 'off',
                                                                 'style' : 'width:80px'}))

class ComplaintDisplayParams (forms.Form):
    departments = MultiNumberIdField ()
    datalevel   = forms.ChoiceField (choices = (("villg", "villg"),
                                                ("gramp", "gramp"),
                                                ("block", "block"),
                                                ("distt", "distt"),
                                                ("state", "state")))
    stdate      = FormattedDateField ()
    endate      = FormattedDateField ()

class Report (forms.Form):
    stdate = FormattedDateField ()
    endate = FormattedDateField ()
    departments  = forms.ModelMultipleChoiceField (queryset = ComplaintDepartment.objects.all(),
                                                   label    = _("Available Departments"),
                                                   widget   = forms.Select (attrs = {'style' : 'width:300px;height:150px;',
                                                                                     'multiple' : 'multiple',}),
                                                   required = False)

    selecteddep  = forms.ModelMultipleChoiceField (queryset = ComplaintDepartment.objects.none(),
                                                   label    = _("Selected Departments"),
                                                   widget   = forms.Select (attrs = {'style' : 'width:300px;height:150px;',
                                                                                     'multiple' : 'multiple',}),
                                                   required = False)

    block        = forms.ModelChoiceField (queryset = Block.objects.all(),
                                           empty_label = "------",
                                           widget   = forms.Select (attrs = { 'style' : 'width:100%'}),
                                           required = False)
    gp           = forms.ModelChoiceField (queryset = GramPanchayat.objects.none (),
                                           empty_label = '------',
                                           widget   = forms.Select (attrs = { 'style' : 'width:100%'}),
                                           required = False)
    village      = forms.ModelChoiceField (queryset = Village.objects.none (),
                                           empty_label = '------',
                                           widget   = forms.Select (attrs = { 'style' : 'width:100%'}),
                                           required = False)

    def __init__ (self, stdate, endate, deptids, blockids, *args, **kwargs):
        super (Report, self).__init__ (*args, **kwargs)

        self.fields ['stdate'].initial = stdate
        self.fields ['endate'].initial = endate
        self.fields ['departments'].queryset = ComplaintDepartment.objects.exclude (id__in = deptids)
        self.fields ['selecteddep'].queryset = ComplaintDepartment.objects.filter (id__in = deptids)
        self.fields ['block'].queryset       = Block.objects.all().exclude (id__in = blockids)



class LocationStatsForm (ComplaintDisplayParams):
    locid = forms.IntegerField ()

class ReportForm(forms.Form):
    stdate = forms.DateField (input_formats = ('%d/%m/%Y',),
                              widget = forms.TextInput (attrs = {'autocomplete' : 'off'}))
    endate = forms.DateField (input_formats = ('%d/%m/%Y',),
                              widget = forms.TextInput (attrs = {'autocomplete' : 'off'}))
    deptids = MultiNumberIdField (required = False)
    stateids = MultiNumberIdField (required = False)
    disttids = MultiNumberIdField (required = False)
    blockids = MultiNumberIdField (required = False)
    grampids = MultiNumberIdField (required = False)
    villgids = MultiNumberIdField (required = False)
    mdgindicators = forms.CharField (required = False)
    suggestions   = forms.CharField (required = False)


class ReportDataValid(forms.Form):
    deptids = MultiNumberIdField ()
    blkid   = MultiNumberIdField (required=False)
    gpid    = MultiNumberIdField (required=False)
    villid  = MultiNumberIdField (required=False)


class SetComplaintReminder (forms.Form):
    complaintno = forms.CharField (widget = forms.HiddenInput())
    reminderon  = forms.DateField (input_formats = ('%d/%m/%Y',),
                                   widget = forms.TextInput (attrs = {'autocomplete' : 'off',
                                                                      'size' : '10'}),
                                   label = _("On:"))

    def __init__ (self, complaint, *args, **kwargs):
        super (SetComplaintReminder, self).__init__ (*args, **kwargs)
        self.fields ['complaintno'].initial = complaint.complaintno

