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

from datetime import datetime
from django.conf import settings


def update_complaint_sequence (complaint):
    from cmh.issuemgr.models import Complaint

    todays_complaints = Complaint.objects.filter (created__year  = complaint.created.year,
                                                  created__month = complaint.created.month,
                                                  created__day   = complaint.created.day,
                                                  original = None)
    todays_complaints = todays_complaints.order_by ('created')

    first_complaint = todays_complaints [0]
    complaint.complaintno = '%s.%06d' % (complaint.created.strftime ('%Y%m%d'),
                                         (complaint.id - first_complaint.id + 1))
    complaint.save ()



def get_location_attr (block_no, gp_no, vill_no):
    loc_code = "%s.%03d.%03d.%03d" % (settings.DEPLOY_DISTT_CODE,
                                      int (block_no),
                                      int (gp_no),
                                      int (vill_no))

    return Village.objects.get (code = loc_code)
