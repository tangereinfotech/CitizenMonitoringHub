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
import os

class Command(BaseCommand):
    help = "This utility exports data of all complaints filed between a given start date and end date"

    option_list = BaseCommand.option_list + (
        make_option('-s', '--start_date', dest='sdate', type='string', help='start date of the range period in YYYY/MM/DD format'),
        make_option('-e', '--end_date', dest='edate', type='string',help = 'end date of the range period in YYYY/MM/DD format'),
        make_option('-f', '--file', dest='export_file', type='string',help = 'file name for exporting the data'),
    )


    def handle(self, *args, **options):
        try:
            sdate = datetime.strptime(options['sdate'],"%Y/%m/%d")
        except ValueError:
            raise OptionValueError("option %s: invalid start date value: %r. Should have a format like 'YYYY/MM/DD'" % ('-s', options['sdate']))
        try:
            edate = datetime.strptime(options['edate'],"%Y/%m/%d")
        except ValueError:
            raise OptionValueError("option %s: invalid end date value: %r. Should have a format like 'YYYY/MM/DD'" % ('-e', options['edate']))

        export_dir = os.path.dirname(options['export_file'])

        if os.path.exists(export_dir):
            pass
        else:
            raise OptionValueError("option %s: Directory %r does not exist" % ('-f', export_dir))
        try:
            ofile = open (options['export_file'], "w")
        except IOError:
            raise OptionValueError("option %s: Could not open file %r for writing" % ('-f', options['export_file']))

        report = Report(sdate, edate,ofile)
        report.export_data()
