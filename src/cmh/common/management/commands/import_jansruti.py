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
from datetime import datetime

from optparse import make_option, OptionParser
from django.core.management.base import BaseCommand, CommandError

from cmh.common.remingtrans import translate
from cmh.common.constants import DeployDistrict

from cmh.common.utils import ExcelProcessor as EP
from cmh.common.utils import InvalidDataException

from cmh.common.models import ComplaintDepartment, ComplaintType, ComplaintMDG
from cmh.common.models import GramPanchayat, Village

from cmh.usermgr.utils import get_or_create_citizen

from cmh.issuemgr.constants import STATUS_NEW
from cmh.issuemgr.models import Complaint
from cmh.issuemgr.utils import update_complaint_sequence

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

        ep = EP (self.save_data, self.parse_complete, self.exception_handler)
        ep.process (bookname, sheetname, True,
                    [EP.CELL_TEXT,
                     EP.CELL_TEXT,
                     EP.CELL_INT,
                     EP.CELL_INT,
                     EP.CELL_INT,
                     EP.CELL_TEXT,
                     EP.CELL_TEXT,
                     EP.CELL_TEXT])

    def exception_handler (self, rowid, e):
        print "Skipping row %d since exception occured while importing this row:" % (rowid + 1), e

    def save_data (self, rowid, cells):
        skiprow = False
        reason = ""

        if cells [-1] != None and cells [-1].lower () == 'reject':
            skiprow = True
            reason = "Row is marked for skipping"

        if skiprow == False:
            if None in cells [:-1]:
                skiprow = True
                reason = "Empty cells in row"

        if skiprow == False:
            try:
                dept = ComplaintDepartment.objects.get (code = cells [COL_DEPT_CODE])
            except ComplaintDepartment.DoesNotExist:
                skiprow = True
                reason = "Department with code [%s] not found" % (cells [COL_DEPT_CODE])
            except ComplaintDepartment.MultipleObjectsReturned:
                skiprow = True
                reason = "Multiple departments found with code: " + cells [COL_DEPT_CODE]

        if skiprow == False:
            try:
                ct = ComplaintType.objects.get (code = "%s.%03d" % (dept.code, cells [COL_COMP_CODE]))
            except ComplaintType.DoesNotExist:
                skiprow = True
                reason = "Complaint Type not found with department code [%s] and complaint code [%d]" % (dept.code, cells [COL_COMP_CODE])
            except ComplaintType.MultipleObjectsReturned:
                skiprow = True
                reason = "Multiple Complaint Types found with department code [%s] and complaint code [%d]" % (dept.code, cells [COL_COMP_CODE])

        if skiprow == False:
            try:
                gp = GramPanchayat.objects.get (code = DeployDistrict.DISTRICT.code + ".%03d.%03d" % (cells [COL_BLOK_CODE], cells [COL_GRAM_CODE]))
            except GramPanchayat.DoesNotExist:
                skiprow = True
                reason = "Gram Panchayat not found with Block code [%d] and Gram Panchayat code [%d]" % (cells [COL_BLOK_CODE], cells [COL_GRAM_CODE])
            except GramPanchayat.MultipleObjectsReturned:
                skiprow = True
                reason = "Multiple Gram Panchayat found with Block code [%d] and Gram Panchayat code [%d]" % (cells [COL_BLOK_CODE], cells [COL_GRAM_CODE])

        if skiprow == False:
            village_codes = sorted ([v.code for v in gp.village_set.all ()])
            if len (village_codes) == 0:
                skiprow = True
                reason  = "No villages are present in Gram Panchayat with Block code [%d] and Gram Panchayat code [%d]" % (cells [COL_BLOK_CODE], cells [COL_GRAM_CODE])
            else:
                village = gp.village_set.all ().get (code = village_codes [0])

        if skiprow:
            print "Skipping row [%d], reason: %s" % ((rowid + 1), reason)
        else:
            c = Complaint.objects.create (complainttype = ct,
                                          description = translate (cells [COL_COMP_DESC]),
                                          department = dept,
                                          curstate = STATUS_NEW,
                                          filedby = get_or_create_citizen ('9977001872', translate (cells [COL_CITI_NAME])),
                                          location = village,
                                          logdate = datetime.today ())
            update_complaint_sequence (c)

    def parse_complete (self):
        print "Done"
