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

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from cmh.smsgateway.utils import queue_complaint_update_sms

from cmh.common.utils import debug
from cmh.common.models import Village
from cmh.common.constants import DeployDistrict
from cmh.issuemgr.models import Complaint

from cmh.issuemgr.constants import STATUS_RESOLVED, STATUS_CLOSED

def update_complaint_sequence (complaint):
    from cmh.issuemgr.models import Complaint

    todays_complaints = Complaint.objects.filter (created__year  = complaint.created.year,
                                                  created__month = complaint.created.month,
                                                  created__day   = complaint.created.day,
                                                  original = None)
    todays_complaints = todays_complaints.order_by ('created')

    first_complaint = todays_complaints [0]
    complaint.complaintno = '%s.%03d' % (complaint.created.strftime ('%Y%m%d'),
                                         (complaint.id - first_complaint.id + 1))
    complaint.save ()



def get_location_attr (block_no, gp_no, vill_no):
    loc_code = "%s.%03d.%03d.%03d" % (DeployDistrict.DISTRICT.code,
                                      int (block_no.strip ()),
                                      int (gp_no.strip ()),
                                      int (vill_no.strip ()))

    return Village.objects.get (code = loc_code)


def close_resolved ():
    now_day = datetime.today ().date ()
    seven_ago = now_day - timedelta (days = 7)

    resolved = Complaint.objects.filter (latest = True,
                                         curstate = STATUS_RESOLVED,
                                         createdate__lte = seven_ago)

    for oldver in resolved:
        debug ("Closing through time lapse : " + oldver.complaintno)
        newver = oldver.clone (AnonymousUser ())
        newver.curstate = STATUS_CLOSED
        newver.save ()

        if newver.complainttype.defsmsclo != None:
            queue_complaint_update_sms (newver.filedby.mobile,
                                        newver.complainttype.defsmsclo,
                                        newver)
        else:
            debug ("[%s]{%s}: " % (newver.complaintno, str (newver.curstate)) +
                   "Message is empty -- not queueing >> from forms.py: issuemgr")

