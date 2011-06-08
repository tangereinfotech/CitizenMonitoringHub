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
from cmh.common.models import ComplaintDepartment, ComplaintType, ComplaintMDG
from cmh.common.utils import ExcelProcessor as EP
from cmh.common.utils import InvalidDataException
from cmh.common.constants import DeployDistrict
from cmh.common.remingtrans import translate
from cmh.issuemgr.models import Complaint

COL_REFR_NUMB = 0
COL_DEPT_CODE = 1
COL_COMP_CODE = 2
COL_BLOK_CODE = 3
COL_GRAM_CODE = 4
COL_CITI_NAME = 5
COL_COMP_DESC = 6
COL_COMP_REMK = 7

class Command (BaseCommand):
    help = """This utility parses an Excel file for JanSruti complaints. The spreadsheet must comply to the format agreed upon earlier
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
                     EP.CELL_INT,
                     EP.CELL_INT,
                     EP.CELL_INT,
                     EP.CELL_TEXT,
                     EP.CELL_TEXT,
                     EP.CELL_TEXT])

    def save_data (self, rowid, cells):
        print "Registering complaint: %d [%s]" % (rowid, str (cells))
        name = cells [COL_CITI_NAME]
        text = cells [COL_COMP_DESC]

        print "--> name: " + translate (name)
        print "--> text: " + translate (text)

    def parse_complete (self):
        print "Done"
