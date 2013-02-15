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

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from datetime import datetime
from common.reports import Report
from cmh.issuemgr.constants import STATUS_ACK, STATUS_CLOSED, STATUS_NEW, STATUS_OPEN, STATUS_REOPEN, STATUS_RESOLVED
from cmh.issuemgr.models import Complaint
from cmh.common.models import ComplaintDepartment
from dateutil import rrule
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from django.db.models import Count
import os

WFSTATE = {
    'new': STATUS_NEW,
    'ack': STATUS_ACK,
    'open': STATUS_RESOLVED,
    'resolved': STATUS_RESOLVED,
    'closed': STATUS_CLOSED,
    'reopen': STATUS_REOPEN
}

class Command(BaseCommand):
    help = "This utility provides various aggregations on the data"

    option_list = BaseCommand.option_list + (
        make_option('-w', '--workflow-state', dest='wstate', type='string', help='Engagement of Departments on system on a month on month basis'),
        make_option('-s', '--start-date', dest='sdate', type='string', help='Engagement of Departments on system on a month on month basis'),
        make_option('-e', '--end-date', dest='edate', type='string', help='Engagement of Departments on system on a month on month basis'),
    )

    def handle(self, *args, **options):

        try:
            sdate = options['sdate']
        except KeyError:
            raise OptionValueError("option %s: invalid start date value: %r. Should have a format like 'YYYY/MM/DD'" % ('-s', options['sdate']))
        try:
            edate = options['edate']
        except KeyError:
            raise OptionValueError("option %s: invalid end date value: %r. Should have a format like 'YYYY/MM/DD'" % ('-s', options['edate']))

        try:
            wstate = options['wstate']
            state = WFSTATE[wstate]
        except KeyError:
            raise OptionValueError("option %s: invalid Workflow state. Valid state valies are new, ack, open, resolved, closed, reopen'" % ('-s', options['edate']))

        from datetime import date
        from time import mktime, strptime

        sdate = datetime.fromtimestamp(mktime(strptime(sdate, "%Y/%m/%d")))
        edate = datetime.fromtimestamp(mktime(strptime(edate, "%Y/%m/%d")))

        month_ranges = [(dt, dt + relativedelta(months= +1) + relativedelta(days=-1)) for dt in rrule.rrule(rrule.MONTHLY, sdate, until=edate)]
        for month in month_ranges:
            deps = Complaint.objects.filter(created__range = month).filter(curstate = state).values('department').annotate(n=Count('pk'))
            for dep in deps:
                d = ComplaintDepartment.objects.get(pk = dep['department'])
                from django.utils.encoding import smart_str
                print month[0].strftime("%Y-%m-%d"), ",", smart_str(d.name), ",", dep['n']

