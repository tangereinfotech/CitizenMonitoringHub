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

import xlrd
import sys
import os
import re

from optparse import make_option, OptionParser
from django.core.management.base import BaseCommand, CommandError
from cmh.issuemgr.models import ComplaintDepartment
from cmh.common.models import District
from cmh.common.utils import ExcelProcessor as EP
from cmh.common.utils import InvalidDataException

COL_DEPT_CODE = 0
COL_DEPT_NAME = 1
COL_DISTT_NAME = 2

class Command (BaseCommand):
    help = """This utility parses an Excel file for location database. The spreadsheet must comply to the format agreed upon earlier
"""
    option_list = BaseCommand.option_list + (
        make_option ('-f', '--file', action='store', dest='file', type='string',
                     help='Spreadsheet file complying to the template as agreed'
                     ),
        make_option ('-s', '--sheet', action='store', dest='sheet', type='string',
                     help='Worksheet name'),
        )

    def handle (self, *args, **options):
        bookname  = options ['file']
        sheetname = options ['sheet']

        if bookname == None:
            print self.help
            sys.exit (0)
        if os.path.exists (bookname) == False:
            print self.help
            sys.exit (0)

        ep = EP (self.save_data, self.parse_complete)
        ep.process (bookname, sheetname, True,
                    [EP.CELL_TEXT,
                     EP.CELL_TEXT,
                     EP.CELL_TEXT])

    def save_data (self, rowid, cells):
        print "Processing row number: ", rowid, ", Content: ", cells
        dept_code = cells [COL_DEPT_CODE]
        dept_name = cells [COL_DEPT_NAME]
        distt_name = cells [COL_DISTT_NAME].strip ()

        try:
            distt = District.objects.get (name__icontains = distt_name)
        except:
            raise InvalidDataException ("Invalid District Name specified")

        try:
            dept = ComplaintDepartment.objects.get (code = dept_code, name = dept_name, district = distt)
        except ComplaintDepartment.DoesNotExist:
            dept = ComplaintDepartment.objects.create (code = dept_code, name = dept_name, district = distt)


    def parse_complete (self):
        pass
