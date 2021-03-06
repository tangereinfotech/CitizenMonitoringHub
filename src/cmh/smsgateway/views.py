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

import sys, re
from datetime import datetime

from django.utils import simplejson as json
from django.http import HttpResponse, HttpResponseForbidden
from django.utils.translation import ugettext as _

from cmh.smsgateway.forms import SMSTransferReqFormat, SMSReceivedFormat
from cmh.smsgateway.models import TextMessage, ReceivedTextMessage, SenderBlacklist, IgnoredTextMessage
from cmh.smsgateway.utils import queue_complaint_update_sms, queue_sms

from cmh.issuemgr.utils import update_complaint_sequence
from cmh.issuemgr.utils import get_location_attr
from cmh.issuemgr.models import Complaint, ComplaintClosureMetric
from cmh.issuemgr.constants import STATUS_NEW

from cmh.common.models import ComplaintType

from cmh.usermgr.utils import get_or_create_citizen
from cmh.common.utils import debug
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.utils.http import http_date
import time
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _

REGEX_SEP = r"[\. ,;\-_:]+"

FORMAT = r"^(?P<block>\d+)" + REGEX_SEP + r"(?P<gramp>\d+)" + REGEX_SEP + r"(?P<villg>\d+)" + REGEX_SEP + r"(?P<name>\w+)" + REGEX_SEP + r"(?P<complaint>.+$)"

class InvalidMessageException (Exception):
    pass

@never_cache
def gateway (request):
    print "came in gateway"
    if request.method == 'GET':
        transferreq = SMSTransferReqFormat (request.GET)
        if transferreq.is_valid () == True:
            messages = []
            for tm in TextMessage.objects.filter (processed = False):
                messages.append ({'to' : tm.phone, 'message' : tm.message})
                tm.processed = True
                tm.processed_time = datetime.now()
                tm.save ()
            return HttpResponse (json.dumps ({"payload":
                                              {"task": "send",
                                               "secret": "0123456789",
                                               "messages": messages}}))
        else:
            #non user generated request, just ignore this
            return HttpResponse (json.dumps ({"payload":
                                          {"success": "true",
                                           }}))
    elif request.method == 'POST':
        receivedform = SMSReceivedFormat (request.POST)
        #debug ("Received from: " + str (receivedform))
        if receivedform.is_valid ():
            try:
                #debug ("Form is valid")
                sender_phone = receivedform.cleaned_data ['from']
                message      = receivedform.cleaned_data ['message']
                rtm = ReceivedTextMessage.objects.create (sender = sender_phone,
                                                          valid = False,
                                                          message = message)

                matches = re.match (FORMAT, message, re.S)
                if matches != None:
                    block = str (int (matches.group ('block')))
                    gramp = str (int (matches.group ('gramp')))
                    villg = str (int (matches.group ('villg')))
                    sender_name  = matches.group ('name')
                    issue_desc = matches.group ('complaint')
                    citizen = get_or_create_citizen (sender_phone, sender_name)
                    location = get_location_attr (block, gramp, villg)
                    compl = Complaint.objects.create (complainttype = None,
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
                    ComplaintClosureMetric.objects.create (complaintno = compl.complaintno)

                    # If we reach this point, the message was properly formatted
                    rtm.valid = True
                    rtm.complaint = compl
                    rtm.save ()

                    # Remove the user from blacklist in case he is there
                    for sbl in SenderBlacklist.objects.filter (sender = rtm.sender):
                        #debug ("Removing sender from blacklist: " + str (rtm.sender))
                        sbl.delete ()

                    text_message = _("Your Grievance number is %s. We would revert in 36 hours to seek more details" % (compl.complaintno))
                    queue_sms (sender_phone, text_message)
                    return HttpResponse (json.dumps ({'payload' : {'success' : 'true'}}))
                else:
                    itm = IgnoredTextMessage.objects.create(sender = sender_phone,
                                                            valid = False,
                                                            message = message)
                    raise InvalidMessageException
            except (InvalidMessageException, ObjectDoesNotExist) as e:
                # Improperly formatted
                # check if the user is black listed, keep the sender black listed and don't respond
                if not is_blacklisted (rtm.sender):
                    if not new_blacklist (rtm.sender):
                        text_message = "Call center would respond in next 36 hrs after looking into your issue"
                        queue_sms (sender_phone, text_message)
                else:
                    #debug ("Sender is blacklisted. Not sending ack: " + str (rtm.sender))
                    pass
                return HttpResponse (json.dumps ({'payload' : {'success' : 'true'}}))
        else:
            # In this case, we can safely assume that the message is not coming from
            # SMSSync so silently ignore.
            return HttpResponse (json.dumps ({'payload' : {'success' : 'true'}}))
    else:
        return HttpResponseForbidden


def is_blacklisted (sender):
    if SenderBlacklist.objects.filter (sender__contains = sender).count () == 0:
        return False
    else:
        return True

def remove_from_blacklist(sender):
    SenderBlacklist.objects.filter(sender__contains = sender).delete()



def new_blacklist (sender):
    def get_message_valid (msglist, index):
        try:
            msg = msglist [index]
            valid = msg.valid
        except:
            valid = True
        return valid

    sender_messages = ReceivedTextMessage.objects.filter (sender = sender)

    all_count = sender_messages.count ()
    if all_count > 3:
        beg_index = all_count - 3
    else:
        beg_index = 0

    sender_messages = sender_messages [beg_index:]

    msg0valid = get_message_valid (sender_messages, 0)
    msg1valid = get_message_valid (sender_messages, 1)
    msg2valid = get_message_valid (sender_messages, 2)

    if (msg0valid == False and msg1valid == False and msg2valid == False):
        # Blacklist the user in case he is not blacklisted yet
        if SenderBlacklist.objects.filter (sender = sender).count () == 0:
            #debug ("Blacklisting sender : " + str (sender))
            SenderBlacklist.objects.create (sender = sender)
        return True
    else:
        return False
