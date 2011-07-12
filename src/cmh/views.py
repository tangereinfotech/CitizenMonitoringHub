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
from django.shortcuts import render_to_response
from django.db.models import Q

from cmh.usermgr.utils import get_user_menus

from cmh.common.models import ComplaintType, ComplaintDepartment

from cmh.issuemgr.models import Complaint

from cmh.issuemgr.forms import DateIndex

def index (request):
    departments = ComplaintDepartment.objects.all ()
    request.session ['blkids']  = []
    request.session ['villids'] = []
    request.session ['gpids']   = []
    request.session ['depids']  = []
    return render_to_response ('index.html', {'menus' : get_user_menus (request.user,index),
                                              'user'  : request.user,
                                              'form'  : DateIndex(),
                                              'map'   : {'center_lat' : 23.10847,
                                                       'center_long' : 76.989098},
                                              'departments' : departments})

def aboutus (request):
    return render_to_response ('aboutus.html', {'menus' : get_user_menus (request.user,index),
                                              'user' : request.user},)
