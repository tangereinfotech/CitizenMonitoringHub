
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

from django.core.management.base import NoArgsCommand

from cmh.issuemgr.views import get_vital_stats
import settings
from datetime import date
from django.template import loader
from django.template.loader import Context, get_template
from cmh.common.models import ComplaintDepartment
from django.core.mail import EmailMessage

class Command (NoArgsCommand):
    def handle (self, *args, **kwargs):
        cds = ComplaintDepartment.objects.all()
        stdate = settings.LIVEDATE
        enddate = date.today()
        summary_stats = {}
        for cd in cds:
            vital_stats = get_vital_stats([cd], stdate, enddate)
            summary_stats[cd.name] = vital_stats
        c = Context({"dep_stats": summary_stats, "stdate": stdate, "enddate": enddate})
        t = get_template('vital_stats_dept_wise_breakup.html')
        html = t.render(c)
        msg = EmailMessage('Summary Grievance Statistics for Kalahandi as on %s'%(enddate.strftime("%d %b, %Y")), html, settings.EMAIL_HOST_USER, settings.EMAIL_NOTIFICATION_LIST)
        msg.content_subtype = "html"
        msg.send()

