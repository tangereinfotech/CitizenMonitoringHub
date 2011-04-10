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

import re, random, string
from datetime import datetime, date, timedelta
from cmh.common.models import Category, Attribute
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
    # except:
    #     pass
        #response = get_error_response(request.client_locale, 'E_COMMON_HACK_1')
        #raise InvalidDateSpec("Date format is invalid. Please provide in format mm/dd/yyyy.")

