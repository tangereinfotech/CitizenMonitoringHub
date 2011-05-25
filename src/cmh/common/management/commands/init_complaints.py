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
from cmh.issuemgr.models import ComplaintDepartment, ComplaintType
from cmh.common.utils import ExcelProcessor as EP
from cmh.common.utils import InvalidDataException

COL_DEPT_NAME = 0
COL_DEPT_CODE = 1
COL_COMP_CODE = 2
COL_COMP_SUMM = 3
COL_COMP_CLSS = 4
COL_COMP_SMSACK = 5
COL_COMP_SMSOPN = 6
COL_COMP_SMSRSL = 7
COL_COMP_SMSCLO = 8

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
                    [EP.CELL_TEXT for i in range (9)])

    def save_data (self, rowid, cells):
        print "Processing row number: ", rowid, ", Content: ", cells
        dept_code = cells [COL_DEPT_CODE]
        comp_code = cells [COL_COMP_CODE]
        comp_summ = cells [COL_COMP_SUMM]
        comp_clss = cells [COL_COMP_CLSS]
        comp_smsack = cells [COL_COMP_SMSACK]
        comp_smsopn = cells [COL_COMP_SMSOPN]
        comp_smsrsl = cells [COL_COMP_SMSRSL]
        comp_smsclo = cells [COL_COMP_SMSCLO]

        try:
            department = ComplaintDepartment.objects.get (code__iexact = dept_code)
        except ComplaintDepartment.DoesNotExist:
            raise InvalidDataException ("Department does not exist: "+ dept_code)

        comp_code = "%s.%03d" % (dept_code, int (float (comp_code)))
        try:
            complaint = ComplaintType.objects.get (code = comp_code)
        except ComplaintType.DoesNotExist:
            complaint = ComplaintType.objects.create (code = comp_code,
                                                      summary = comp_summ,
                                                      department = department,
                                                      cclass = comp_clss,
                                                      defsmsack = comp_smsack,
                                                      defsmsopen = comp_smsopn,
                                                      defsmsres = comp_smsrsl,
                                                      defsmsclo = comp_smsclo)

    def parse_complete (self):
        pass
