# encoding: utf-8
#
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

import sys
import xlrd

from django.conf import settings

class InvalidDataException (Exception):
    pass

class ExcelProcessor ():
    CELL_EMPTY  = xlrd.XL_CELL_EMPTY  # 0
    CELL_TEXT   = xlrd.XL_CELL_TEXT   # 1
    CELL_NUMBER = xlrd.XL_CELL_NUMBER # 2
    CELL_DATE   = xlrd.XL_CELL_DATE   # 3

    def __init__ (self, rowdatacallback, parsedonecallback):
        self.rowdatacallback = rowdatacallback
        self.parsedonecallback = parsedonecallback

    def process (self, excel, sheet_name, has_header, cell_types = []):
        book = xlrd.open_workbook (excel)
        sheet = book.sheet_by_name (sheet_name)

        if has_header:
            rowno = 1
        else:
            rowno = 0

        if len (cell_types) == 0:
            for rowid in range (rowno, sheet.nrows):
                cells = {}
                for cellid in range (sheet.ncols):
                    cells.update ({cellid : (sheet.cell_type (rowid, cellid), sheet.cell_value (rowid, cellid))})

                self.rowdatacallback (rowid, cells)
        else:
            for rowid in range (rowno, sheet.nrows):
                cellvalues = []
                for cellid in range (len (cell_types)):
                    ct = sheet.cell_type (rowid, cellid)
                    if ct != ExcelProcessor.CELL_EMPTY:
                        value = self.convert_type (ct,
                                                   cell_types [cellid],
                                                   sheet.cell_value (rowid, cellid))
                        cellvalues.append (value)
                    else:
                        cellvalues.append (None)
                self.rowdatacallback (rowid, cellvalues)

        self.parsedonecallback ()

    def convert_type (self, curtype, newtype, data):
        if curtype == ExcelProcessor.CELL_TEXT:
            if newtype == ExcelProcessor.CELL_TEXT:
                return data.strip ()
            elif newtype == ExcelProcessor.CELL_NUMBER:
                return float (data.strip ())
            elif newtype == ExcelProcessor.CELL_DATE:
                raise InvalidDataException ("Conversion to Date Type not supported")
            else:
                raise InvalidDataException ("Invalid target datatype:"+str(newtype))

        elif curtype == ExcelProcessor.CELL_NUMBER:
            if newtype == ExcelProcessor.CELL_TEXT:
                return str (data)
            elif newtype == ExcelProcessor.CELL_NUMBER:
                return data
            elif newtype == ExcelProcessor.CELL_DATE:
                raise InvalidDataException ("Conversion to Date Type not supported")
            else:
                raise InvalidDataException ("Invalid target datatype : " +
                                            str (newtype))
        elif curtype == ExcelProcessor.CELL_DATE:
            raise InvalidDataException ("Conversion from Date Type not supported")
        else:
            raise InvalidDataException ("Invalid source datatype : " + str (curtype))



import re, random, string
from datetime import datetime, date, timedelta
from django.db.models import Q

def check_email (email):
    at_count = re.findall ('@', email)
    at_idx  = email.rfind ('@')
    dot_idx = email.rfind ('.')

    if (len (at_count) != 1 or at_idx == -1 or \
        dot_idx == (len (email) - 1) or dot_idx < at_idx):
        return False
    else:
        return True

def check_mobile(ph):
    if len (ph) != 10:
        return False
    else:
        try:
            iph = int (ph)
            return True
        except ValueError:
            return False

def check_phone(ph):
    if len (ph) != 8:
        return False
    else:
        try:
            iph = int (ph)
            return True
        except ValueError:
            return False



def get_random_string (length, special_chars = False):
    CHARSET = 'abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789'
    if special_chars == True:
        CHARSET +="""~!@#$%^&*()_+{}[];:,./<>\t\t"""
    ret_str = ""
    for x in range (length):
        ret_str = ret_str + random.choice(CHARSET)
    return ret_str

def value_or_random(data, length, special_chars = False):
    """if data in None, returns a random string otherwise returns data"""
    if data == None:
        return get_random_string(length, special_chars)
    return data

def parse_string (string, tokens = []):
    parsed_tokens = {}
    m = re.search (ur'(?P<text>[\w\s,]*)\s+(?P<rest>\w+:.*)|(?P<matchers>\w+:.[\u0000-\uffff]*)|(?P<all>.*)', string, flags = re.UNICODE)
    if m != None:
        if m.group ('all') != None:
            parsed_tokens ['text'] = m.group ('all')
        else:
            parsed_tokens ['text'] = m.group ('text')
            if m.group ('rest') != None:
                rest = m.group ('rest') # in rest you get key: value pair to search for (in 1st cond)
            elif m.group ('matchers') != None:
                rest = m.group ('matchers') # in rest you get key: value pair to search for (in 2nd cond)

            if rest != None:
                for token in tokens:
                    token_str = ur'\b%s\b:(?P<first>[\u0000-\uFFFF]*[\s\w/@\.,-]+)\s\w+:|\b%s\b:(?P<second>[\u0000-\uFFFF]*[\s\w/@\.,-]+)$' % (token, token)
                    m2 = re.search (token_str, rest, flags = re.UNICODE)
                    if m2 != None:
                        if m2.group ('first') != None:
                            parsed_tokens [token] = m2.group ('first').strip ()
                        if m2.group ('second') != None:
                            parsed_tokens [token] = m2.group ('second').strip ()

    return parsed_tokens

def parse_string2 (string, tokens = []):
    token_results = parse_string (string, tokens)
    if token_results.has_key ('text') and token_results ['text'] != None:
        token_results ['text'] = token_results ['text'].split ()
    return token_results

def ddmmyyyy2date (str):
    try:
        if str.split('/') != -1:
           (m, d, y) = str.split ('/')
        elif str.split('-') != -1:
           (m, d, y) = str.split ('-')

        mm = int (m)
        dd = int (d)
        yyyy = int (y)
    except:
        return None

    if mm == None or dd == None or yyyy == None or mm > 12 or dd > 31 or (mm == 2 and dd > 28):
        return None
    else:
        return date (year = yyyy, month = mm, day = dd)



def debug (message):
    if settings.DEBUG:
        sys.stderr.write (str (message) + "\n")

def daterange (start_date, end_date):
    for n in range((end_date - start_date).days):
        yield start_date + timedelta (days = n)

