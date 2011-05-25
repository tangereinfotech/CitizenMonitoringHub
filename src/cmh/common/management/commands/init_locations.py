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
from cmh.common.models import Country, State, District
from cmh.common.models import Block, GramPanchayat, Village
from cmh.common.utils import ExcelProcessor as EP

COL_STATE_NAME = 0
COL_STATE_CODE = 1
COL_DISTT_NAME = 2
COL_DISTT_CODE = 3
COL_BLOCK_NAME = 4
COL_BLOCK_CODE = 5
COL_GRAMP_NAME = 6
COL_GRAMP_CODE = 7
COL_VILLG_NAME = 8
COL_VILLG_CODE = 9
COL_VILLG_LONG = 10
COL_VILLG_LATD = 11

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
                     EP.CELL_NUMBER,
                     EP.CELL_TEXT,
                     EP.CELL_NUMBER,
                     EP.CELL_TEXT,
                     EP.CELL_NUMBER,
                     EP.CELL_TEXT,
                     EP.CELL_NUMBER,
                     EP.CELL_TEXT,
                     EP.CELL_NUMBER,
                     EP.CELL_NUMBER,
                     EP.CELL_NUMBER])

    def save_data (self, rowid, cells):
        print "Processing row number: ", rowid, ", Content: ", cells
        naton_code = 'IN'
        naton_name = 'India'
        state_name = cells [COL_STATE_NAME]
        state_code = "%03d" % int (cells [COL_STATE_CODE])
        distt_name = cells [COL_DISTT_NAME]
        distt_code = "%03d" % int (cells [COL_DISTT_CODE])
        block_name = cells [COL_BLOCK_NAME]
        block_code = "%03d" % int (cells [COL_BLOCK_CODE])
        gramp_name = cells [COL_GRAMP_NAME]
        gramp_code = "%03d" % int (cells [COL_GRAMP_CODE])
        villg_name = cells [COL_VILLG_NAME]
        villg_code = "%03d" % int (cells [COL_VILLG_CODE])
        villg_long = cells [COL_VILLG_LONG]
        villg_latd = cells [COL_VILLG_LATD]

        state_code = '.'.join ([naton_code, state_code])
        distt_code = '.'.join ([state_code, distt_code])
        block_code = '.'.join ([distt_code, block_code])
        gramp_code = '.'.join ([block_code, gramp_code])
        villg_code = '.'.join ([gramp_code, villg_code])


        try:
            country = Country.objects.get (code = naton_code, name = naton_name)
        except Country.DoesNotExist:
            country = Country.objects.create (code = naton_code, name = naton_name)

        try:
            state = State.objects.get (code = state_code,
                                       name = state_name,
                                       country = country)
        except State.DoesNotExist:
            state = State.objects.create (code = state_code,
                                          name = state_name,
                                          country = country)

        try:
            distt = District.objects.get (code = distt_code,
                                          name = distt_name,
                                          state = state)
        except District.DoesNotExist:
            distt = District.objects.create (code = distt_code,
                                             name = distt_name,
                                             state = state)

        try:
            block = Block.objects.get (code = block_code,
                                       name = block_name,
                                       district = distt)
        except Block.DoesNotExist:
            block = Block.objects.create (code = block_code,
                                          name = block_name,
                                          district = distt)

        try:
            gramp = GramPanchayat.objects.get (code = gramp_code,
                                               name = gramp_name,
                                               block = block)
        except GramPanchayat.DoesNotExist:
            gramp = GramPanchayat.objects.create (code = gramp_code,
                                                  name = gramp_name,
                                                  block = block)

        try:
            villg = Village.objects.get (code = villg_code,
                                         name = villg_name,
                                         grampanchayat = gramp)
        except Village.DoesNotExist:
            search  ="%s;%s;%s;%s;%s" % (villg_name,
                                         gramp_name,
                                         block_name,
                                         distt_name,
                                         state_name)
            villg = Village.objects.create (code = villg_code,
                                            name = villg_name,
                                            grampanchayat = gramp,
                                            lattd = villg_latd,
                                            longd = villg_long,
                                            search = search)


    def parse_complete (self):
        print "Done with import"
