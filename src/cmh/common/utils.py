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
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.cache import add_never_cache_headers
from django.utils import simplejson

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
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta (days = n)


def get_datatables_records(request, querySet, columnIndexNameMap, jsonTemplatePath = None, *args):
    """
    Usage:
        querySet: query set to draw data from.
        columnIndexNameMap: field names in order to be displayed.
        jsonTemplatePath: optional template file to generate custom json from.  If not provided it will generate the data directly from the model.

    """

    cols = int(request.GET.get('iColumns',0)) # Get the number of columns
    iDisplayLength =  min(int(request.GET.get('iDisplayLength',10)),100)     #Safety measure. If someone messes with iDisplayLength manually, we clip it to the max value of 100.
    startRecord = int(request.GET.get('iDisplayStart',0)) # Where the data starts from (page)
    endRecord = startRecord + iDisplayLength  # where the data ends (end of page)

    # Pass sColumns
    keys = columnIndexNameMap.keys()
    keys.sort()
    colitems = [columnIndexNameMap[key] for key in keys]
    sColumns = ",".join(map(str,colitems))

    # Ordering data
    iSortingCols =  int(request.GET.get('iSortingCols',0))
    asortingCols = []

    if iSortingCols:
        for sortedColIndex in range(0, iSortingCols):
            sortedColID = int(request.GET.get('iSortCol_'+str(sortedColIndex),0))
            if request.GET.get('bSortable_{0}'.format(sortedColID), 'false')  == 'true':  # make sure the column is sortable first
                sortedColName = columnIndexNameMap[sortedColID]
                sortingDirection = request.GET.get('sSortDir_'+str(sortedColIndex), 'asc')
                if sortingDirection == 'desc':
                    sortedColName = '-'+sortedColName
                asortingCols.append(sortedColName)
        querySet = querySet.order_by(*asortingCols)

    # Determine which columns are searchable
    searchableColumns = []
    for col in range(0,cols):
        if request.GET.get('bSearchable_{0}'.format(col), False) == 'true': searchableColumns.append(columnIndexNameMap[col])

    # Apply filtering by value sent by user
    customSearch = request.GET.get('sSearch', '').encode('utf-8');
    if customSearch != '':
        outputQ = None
        first = True
        for searchableColumn in searchableColumns:
            kwargz = {searchableColumn+"__icontains" : customSearch}
            outputQ = outputQ | Q(**kwargz) if outputQ else Q(**kwargz)
        querySet = querySet.filter(outputQ)

    # Individual column search
    outputQ = None
    for col in range(0,cols):
        if request.GET.get('sSearch_{0}'.format(col), False) > '' and request.GET.get('bSearchable_{0}'.format(col), False) == 'true':
            kwargz = {columnIndexNameMap[col]+"__icontains" : request.GET['sSearch_{0}'.format(col)]}
            outputQ = outputQ & Q(**kwargz) if outputQ else Q(**kwargz)
    if outputQ: querySet = querySet.filter(outputQ)

    iTotalRecords = iTotalDisplayRecords = querySet.count() #count how many records match the final criteria
    querySet = querySet[startRecord:endRecord] #get the slice
    sEcho = int(request.GET.get('sEcho',0)) # required echo response

    if jsonTemplatePath:
        jstonString = render_to_string(jsonTemplatePath, locals()) #prepare the JSON with the response, consider using : from django.template.defaultfilters import escapejs
        response = HttpResponse(jstonString, mimetype="application/javascript")
    else:
        aaData = []
        a = querySet.values()
        for row in a:
            rowkeys = row.keys()
            rowvalues = row.values()
            rowlist = []
            for col in range(0,len(colitems)):
                for idx, val in enumerate(rowkeys):
                    if val == colitems[col]:
                        rowlist.append(str(rowvalues[idx]))
            aaData.append(rowlist)
        response_dict = {}
        response_dict.update({'aaData':aaData})
        response_dict.update({'sEcho': sEcho, 'iTotalRecords': iTotalRecords, 'iTotalDisplayRecords':iTotalDisplayRecords, 'sColumns':sColumns})
        response =  HttpResponse(simplejson.dumps(response_dict), mimetype='application/javascript')
    #prevent from caching datatables result
    add_never_cache_headers(response)
    return response
