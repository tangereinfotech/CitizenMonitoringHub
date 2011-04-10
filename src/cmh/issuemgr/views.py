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

from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render_to_response
from django.utils import simplejson as json

from cmh.common.models import Category, Attribute, CodeName, LatLong
from cmh.common.models import get_code2name, get_child_attributes
from cmh.issuemgr.models import Department, ComplaintItem


country = Attribute.objects.get (category__key = 'Country')

def index (request):
    states = country.attribute_set.all ()
    return render_to_response ('complaint.html', {'states' : _prepare_select_element (states)})

def select_region (request):
    try:
        str_cat, str_attr = _parse_selection (request.POST ['select'])
        l2_regions = get_child_attributes (str_cat, str_attr)
        l2_values = _prepare_select_element (l2_regions)
        print l2_values
        return HttpResponse (json.dumps (l2_values))
    except:
        return HttpResponse ('')

def submit (request):
    print request.POST
    return render_to_response ('complaint_submitted.html')



def _parse_selection (select_val):
    try:
        cat, attr = select_val.split (',')
        cat_name, str_cat = cat.split (':')
        attr_name, str_attr = attr.split (':')
        if cat_name == 'cat' and attr_name == 'val':
            return (str_cat, str_attr)
        else:
            return None
    except:
        return None

def _prepare_select_element (values):
    return [{'optval' : ('cat:' + value.category.key + ',val:' + value.value),
             'name' : get_code2name (value.value)}
            for value in values]
