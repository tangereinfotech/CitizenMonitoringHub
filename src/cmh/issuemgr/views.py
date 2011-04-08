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

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render_to_response

from cmh.issuemgr.models import State, District, Block, GramPanchayat, Village
from cmh.issuemgr.models import Department, ComplaintItem


def index (request):
    return render_to_response ('complaint.html', {'states' : State.objects.all ()} )

def select_region (request):
    state_code = request.POST ['code']
    ds = District.objects.filter (state__code = state_code)
    return HttpResponse (serializers.serialize ('json', ds, fields = ['code', 'name']))

def submit (request):
    print request.POST
    return render_to_response ('complaint_submitted.html')
