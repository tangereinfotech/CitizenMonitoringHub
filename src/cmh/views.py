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

from cmh.common.models import CodeName

from cmh.issuemgr.constants import COMPLAINT_TYPES, STATUS_NEW, STATUS_REOPEN, STATUS_ACK, STATUS_OPEN, STATUS_RESOLVED, STATUS_CLOSED
from cmh.issuemgr.models import Complaint

def index (request):
    issue_types = []
    complaints = Complaint.objects.filter (latest = True)
    for issue_type in COMPLAINT_TYPES.order_by ('id'):
        issue_types.append ({'name' : CodeName.objects.get (code = issue_type.value).name,
                             'new_reopened' : complaints.filter ((Q (curstate = STATUS_NEW) |
                                                                  Q (curstate = STATUS_REOPEN)),
                                                                 base = issue_type).count (),
                             'acknowledged' : complaints.filter (base = issue_type,
                                                                 curstate = STATUS_ACK).count (),
                             'opened' : complaints.filter (base = issue_type,
                                                         curstate = STATUS_OPEN).count (),
                             'resolved' : complaints.filter (base = issue_type,
                                                             curstate = STATUS_RESOLVED).count (),
                             'closed' : complaints.filter (base = issue_type,
                                                           curstate = STATUS_CLOSED).count ()})
    return render_to_response ('index.html', {'menus' : get_user_menus (request.user),
                                              'user' : request.user,
                                              'map' : {'center_lat' : 23.20119,
                                                       'center_long' : 77.081795,
                                                       'zoom_level' : 13},
                                              'issue_types' : issue_types})

