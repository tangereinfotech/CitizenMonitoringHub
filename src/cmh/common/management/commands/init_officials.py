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
from django.contrib.auth.models import User
from cmh.issuemgr.models import ComplaintDepartment
from cmh.common.models import District
from cmh.usermgr.constants import UserRoles
from cmh.usermgr.models import Official, CmhUser
from cmh.common.utils import ExcelProcessor as EP
from cmh.common.utils import InvalidDataException

COL_DEPT_NAME = 0
COL_DEPT_CODE = 1
COL_OFFI_TITL = 2
COL_OFFI_NAME = 3
COL_OFFI_DESG = 4
COL_OFFI_MOBL = 5
COL_OFFI_DIST = 6

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
                    [EP.CELL_TEXT for i in range (7)])

    def save_data (self, rowid, cells):
        print "Processing row number: ", rowid, ", Content: ", cells
        dept_code = cells [COL_DEPT_CODE]
        title     = cells [COL_OFFI_TITL]
        name      = cells [COL_OFFI_NAME]
        desg      = cells [COL_OFFI_DESG]
        mobile    = cells [COL_OFFI_MOBL]
        district  = cells [COL_OFFI_DIST]

        try:
            department = ComplaintDepartment.objects.get (code = dept_code)
        except ComplaintDepartment.DoesNotExist:
            raise InvalidDataException ("Department does not exist : " + dept_code)

        try:
            district = District.objects.get (name__iexact = district)
        except District.DoesNotExist:
            raise InvalidDataException ("District does not exist: " + district)

        try:
            username = name.replace (" ", "")
            username = username.lower ()
            user = User.objects.get (username = username)
        except User.DoesNotExist:
            user = User.objects.create (username = username, first_name = name)
            user.set_password ('123') # FIXME: SMS Point
            user.save ()

        try:
            cmhuser = CmhUser.objects.get (user = user)
            cmhuser.phone = mobile
            cmhuser.save ()
        except CmhUser.DoesNotExist:
            cmhuser = CmhUser.objects.create (user = user, phone = mobile)

        cmhuser.set_user_role (UserRoles.OFFICIAL)

        try:
            official = Official.objects.get (user = user)
        except Official.DoesNotExist:
            official = Official.objects.create (user = user)

        official.departments.add (department)
        official.title = title
        official.designation = desg
        official.save ()



    def parse_complete (self):
        pass
