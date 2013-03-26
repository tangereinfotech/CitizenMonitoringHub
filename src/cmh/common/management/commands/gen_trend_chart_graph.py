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

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User

from cmh.common.constants import UserRoles
from cmh.common.utils import daterange
from optparse import make_option
from cmh.issuemgr.constants import STATUS_OPEN, STATUS_RESOLVED, STATUS_CLOSED, STATUS_REOPEN, STATUS_ACK, STATUS_NEW
from cmh.issuemgr.models import Complaint, TrendChartSummary
from datetime import date
from django.db.models import Q
def update_trend_chart(sdate = date(2013,01,01), edate=date(2013,01,03)):

    edate = edate
    #Assume resolved state is also a closed state, unless reopened. If reopened, the state would show on latest. so not a worry
    CLOSED_STATES= [STATUS_CLOSED, STATUS_RESOLVED]

    # Remove all closed complaints before the sdate. They are definitely closed and so need not be indexed
    cnos = Complaint.objects.filter(createdate__lte = edate).values_list('complaintno').distinct()

    #Get day increment for the period
    all_dates = [d for d in daterange(sdate, edate)]

    for d in all_dates:
        for c in cnos:
            cs = Complaint.objects.filter(complaintno = c[0], createdate__lte = d).exclude(curstate = STATUS_NEW).order_by('-created')
            if cs.count() > 0 and cs[0].department != None:
                curstate = cs[0].curstate
                trend_dep = cs[0].department
            else:
                curstate = None
                trend_dep = None
            if trend_dep != None:
                try:
                    TrendChartSummary.objects.get(complaint = c[0], date = d)
                except TrendChartSummary.DoesNotExist:
                    if curstate in CLOSED_STATES:
                        pass
                    else:
                        complaint_log_date = Complaint.objects.filter(complaintno = c[0]).order_by('created')[0].logdate
                        TrendChartSummary.objects.create(complaint = c[0], date = d, status = True, department = trend_dep, filed_on = complaint_log_date)

class Command (BaseCommand):
    help = "This utility updates the status of complaints on a per day basis as being open or being closed"

    option_list = BaseCommand.option_list + (
        make_option('-s', '--start_date', dest = 'sdate', type='string', help = 'start date of the range period in YYYY/MM/DD format'),
        make_option('-e', '--end_date', dest = 'sdate', type='string', help = 'end date of the range period in YYYY/MM/DD format')
    )
    def handle (self, *args, **options):
        try:
            sdate = datetime.strptime(options['sdate'],"%Y/%m/%d")
        except:
            raise OptionValueError("option %s: invalid end date value: %r. Should have a format like 'YYYY/MM/DD'" % ('-s', options['sdate']))
        try:
            edate = datetime.strptime(options['edate'],"%Y/%m/%d")
        except:
            raise OptionValueError("option %s: invalid end date value: %r. Should have a format like 'YYYY/MM/DD'" % ('-e', options['edate']))
        update_trend_chart(sdate, edate)
