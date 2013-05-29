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
from cmh.reports.models import IssuesDataReport
from cmh.issuemgr.models import TrendChartSummary, Complaint
from cmh.common.models import ComplaintDepartment
from optparse import make_option, OptionValueError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class Command (BaseCommand):
    help = "Change Department for a specified complaint no"

    option_list = BaseCommand.option_list + (
        make_option('-c', '--complaintno', dest = 'complaintno', type='string', help = 'Complaint No for which the department needs to be changed'),
        make_option('-d', '--department', dest = 'departmentname', type='string', help = 'Department Name -- Some unique part of the department name would do. Raise error if multiple departments exist with same name')
    )

    def handle (self, *args, **options):

        complaintno = options['complaintno']
        if complaintno == None:
            raise OptionValueError("option %s is mandatory. Please provide the Complaint No" % ('-s'))

        departmentname = options['departmentname']
        if departmentname == None:
            raise OptionValueError("option %s is mandatory. Please provide the Department Name" % ('-d'))

        complaints = Complaint.objects.filter(complaintno = complaintno)

        if complaints.count() == 0:
            raise OptionValueError("No Complaints with this Complaint Number:%s" % (options['complaintno']))
        try:
            department = ComplaintDepartment.objects.get(name__contains = departmentname)
        except MultipleObjectsReturned:
            raise OptionValueError("Multiple Departments contain this name. Please qualify the name further")
        except ObjectDoesNotExist:
            raise OptionValueError("No Departments found with this name.")
        complaints.update(department = department)
        IssuesDataReport.objects.filter(complaintno = complaintno).update(department = department)
        IssuesDataReport.objects.filter(complaintno = complaintno).update(department_name = department.code)
        TrendChartSummary.objects.filter(complaint = complaintno).update(department = department)

