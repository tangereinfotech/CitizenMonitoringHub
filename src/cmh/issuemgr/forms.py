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

class ComplaintForm (forms.Form):
    complaint_state       = forms.CharField ()
    complaint_distt       = forms.CharField ()
    complaint_block       = forms.CharField ()
    complaint_gp          = forms.CharField ()
    complaint_village     = forms.CharField ()
    complaint_date        = forms.DateField ()
    complaint_department  = forms.CharField ()
    complaint_summary     = forms.CharField ()
    complaint_description = forms.CharField ()
    your_name             = forms.CharField ()
    your_mobile           = forms.CharField ()


class ComplaintLocationBox (forms.Form):
    term = forms.CharField ()
