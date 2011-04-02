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

from django.shortcuts import render_to_response
from cmh.common.utils import get_complaint_types

def index (request):
    # complaint_types = get_complaint_types ()
    complaint_types = []
    return render_to_response ('complaint.html', {'complaint_types' : complaint_types} )

def submit (request):
    print request.POST
    return render_to_response ('complaint_submitted.html')
