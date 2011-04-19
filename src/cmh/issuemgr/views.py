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

import re

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render_to_response
from django.utils import simplejson as json

from cmh.common.models import Category, Attribute, CodeName, LatLong
from cmh.common.models import get_code2name, get_child_attributes

from cmh.issuemgr.constants import VILLAGES, COMPLAINT_TYPES
from cmh.issuemgr.models import ComplaintItem
from cmh.issuemgr.forms import ComplaintForm, ComplaintLocationBox, ComplaintTypeBox, LOCATION_REGEX


def index (request):
    if request.method == 'GET':
        return render_to_response ('complaint.html')
    else:
        form = ComplaintForm (request.POST)
        if form.is_valid ():
            form.save ()
            return render_to_response ('complaint_submitted.html')
        else:
            print request.POST
            print form.errors
            return render_to_response ('complaint.html', {'errors' : form.errors})


def locations (request):
    try:
        form = ComplaintLocationBox (request.GET)
        if form.is_valid ():
            term = form.cleaned_data ['term']
            matches = re.search (LOCATION_REGEX, term)
            g = matches.groups ()
            names = []
            for village in VILLAGES:
                vill_code = village.value
                vill_name = CodeName.objects.get (code = vill_code).name

                if term.lower () in vill_name.lower ():
                    gp_code = village.parent.value
                    block_code = village.parent.parent.value

                    gp_name = CodeName.objects.get (code = gp_code).name
                    block_name = CodeName.objects.get (code = block_code).name

                    names.append ({'display' : vill_name,
                                   'detail' : ('Gram Panchayat: %s<br/>Block: %s' %
                                               (gp_name, block_name)),
                                   'id' : village.id})
            return HttpResponse (json.dumps (names))
    except:
        import traceback
        traceback.print_exc ()
    return HttpResponse (json.dumps ([]))


def categories (request):
    try:
        form = ComplaintTypeBox (request.GET)
        if form.is_valid ():
            retvals = []
            words = set ([x.lower () for x in form.cleaned_data ['term'].split ()])

            for cpl_type in COMPLAINT_TYPES:
                cpl_code = cpl_type.value
                cpl_item = ComplaintItem.objects.get (code = cpl_code)
                cpl_words = set ([x.lower () for x in cpl_item.name.split ()])
                if len (cpl_words & words) != 0:
                    cpl_dept = CodeName.objects.get (code = cpl_type.parent.value).name
                    retvals.append ({'display' : cpl_item.name,
                                     'detail' : '%s<br/>Department: %s' % (cpl_item.desc, cpl_dept),
                                     'id' : cpl_type.id})
            return HttpResponse (json.dumps (retvals))
    except:
        import traceback
        traceback.print_exc ()
    return HttpResponse (json.dumps ([]))
