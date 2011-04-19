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

from cmh.issuemgr.constants import VILLAGES, COMPLAINT_TYPES, STATUS_NEW
from cmh.issuemgr.models import Complaint, ComplaintItem
from cmh.issuemgr.utils import update_complaint_sequence
from cmh.usermgr.utils import get_or_create_citizen

class ComplaintForm (forms.Form):
    logdate       = forms.DateField (input_formats = ('%d/%m/%Y',))
    description   = forms.CharField ()
    locationid    = forms.IntegerField ()
    yourname      = forms.CharField ()
    yourmobile    = forms.IntegerField ()
    categoryid    = forms.IntegerField ()

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

    def save (self):
        location       = VILLAGES.get (id = self.cleaned_data ['locationid'])
        complaint_base = COMPLAINT_TYPES.get (id = self.cleaned_data ['categoryid'])

        citizen = get_or_create_citizen (self.cleaned_data ['yourmobile'],
                                         self.cleaned_data ['yourname'])

        cpl = Complaint.objects.create (base = complaint_base,
                                        complaintno = None,
                                        description = self.cleaned_data ['description'],
                                        department  = complaint_base.parent,
                                        curstate = STATUS_NEW,
                                        filedby = citizen,
                                        logdate = self.cleaned_data ['logdate'],
                                        location = location,
                                        original = None)
        update_complaint_sequence (cpl)
        return cpl

class ComplaintLocationBox (forms.Form):
    term = forms.RegexField (regex = LOCATION_REGEX)


class ComplaintTypeBox (forms.Form):
    term = forms.CharField ()
