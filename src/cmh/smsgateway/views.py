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

import sys
from datetime import datetime

from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseForbidden

from cmh.smsgateway.forms import SMSTransferReqFormat, SMSReceivedFormat

from cmh.issuemgr.utils import update_complaint_sequence
from cmh.issuemgr.utils import get_location_attr
from cmh.issuemgr.models import Complaint
from cmh.issuemgr.constants import STATUS_NEW

from cmh.usermgr.utils import get_or_create_citizen


def gateway (request):
    if request.method == 'GET':
        transferreq = SMSTransferReqFormat (request.GET)
        if transferreq.is_valid () == True:
            # Find any pending SMSes to be transferred
            # Send them as show in the payload section below
            return HttpResponse (json.dumps ({"payload":
                                              {"task": "send",
                                               "secret": "0123456789",
                                               "messages": [{"to": "0000000000", # 10-dig phone number
                                                             "message": "the message goes here" },]
                                               }
                                              }))
        else:
            return HttpResponse (json.dumps ({}))
    elif request.method == 'POST':
        try:
            receivedform = SMSReceivedFormat (request.POST)
            if receivedform.is_valid ():
                sender_phone = receivedform.cleaned_data ['from']
                message      = receivedform.cleaned_data ['message']
                message_fields = message.split ()
                location = message_fields [0]
                sender_name = message_fields [1]
                issue_desc = ' '.join (message_fields [2:])
                (block_no, gp_no, vill_no) = location.split ('-')

                citizen = get_or_create_citizen (sender_phone, sender_name)

                location = get_location_attr (block_no, gp_no, vill_no)

                compl = Complaint.objects.create (base = None,
                                                  complaintno = None,
                                                  description = issue_desc,
                                                  department = None,
                                                  curstate = STATUS_NEW,
                                                  filedby = citizen,
                                                  logdate = datetime.today ().date (),
                                                  location = location,
                                                  original = None,
                                                  creator = None)
                update_complaint_sequence (compl)
                return HttpResponse (json.dumps ({'payload' : {'success' : 'true'}}))
            else:
                return HttpResponse (json.dumps ({'payload' : {'success' : 'false'}}))
        except:
            import traceback
            traceback.print_exc ()
    else:
        return HttpResponseForbidden

