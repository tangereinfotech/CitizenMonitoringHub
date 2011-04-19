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
from cmh.issuemgr.models import ComplaintItem
from cmh.issuemgr.forms import ComplaintForm, ComplaintLocationBox


country = Attribute.objects.get (category__key = 'Country')

def index (request):
    states = country.attribute_set.all ()
    depts  = Attribute.objects.filter (category__key = 'Complaint Department')
    return render_to_response ('complaint.html', {'states' : _prepare_select_element (states),
                                                  'departments' : _prepare_select_element (depts)})

def locations (request):
    try:
        form = ComplaintLocationBox (request.GET)
        if form.is_valid ():
            term = form.cleaned_data ['term']
            names = []
            for village in country.get_category_descendents ('Village'):
                vill_codename = CodeName.objects.get (code = village.value)
                if term.lower () in vill_codename.name.lower ():
                    names.append ("%s [%s, %s]" % (vill_codename.name,
                                                   CodeName.objects.get (code = village.parent.value).name,
                                                   CodeName.objects.get (code = village.parent.parent.value).name))


            return HttpResponse (json.dumps (names))
    except:
        import traceback
        traceback.print_exc ()
    return HttpResponse (json.dumps ([]))

def select_children (request):
    try:
        str_cat, str_attr = _parse_selection (request.POST ['select'])
        l2_regions = get_child_attributes (str_cat, str_attr)
        l2_values = _prepare_select_element (l2_regions)
        return HttpResponse (json.dumps (l2_values))
    except:
        return HttpResponse ('')


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

def get_complaint_description (request):
    str_cat, str_attr = _parse_selection (request.POST ['select'])
    try:
        attr_complaintitem = ComplaintItem.objects.get (code = str_attr)
        return HttpResponse (json.dumps ({'description' : attr_complaintitem.desc}))
    except ComplaintItem.DoesNotExist:
        return HttpResponse ('')

def submit (request):
    complaint_form = ComplaintForm (request.POST)
    if complaint_form.is_valid ():
        errors = []
        try:
            (str_state, str_state) = _parse_selection (complaint_form.cleaned_data ['complaint_state'])
            attr_state = Attribute.objects.get (value = str_state, category__key = str_state)
            print attr_state.value
        except Attribute.DoesNotExist:
            errors.append ('Incorrect Selection for State')

        try:
            (str_distt, str_distt) = _parse_selection (complaint_form.cleaned_data ['complaint_distt'])
            attr_distt = Attribute.objects.get (value = str_distt, category__key = str_distt)
            print attr_distt.value
        except Attribute.DoesNotExist:
            errors.append ('Incorrect Selection for District')

        try:
            (str_block, str_block) = _parse_selection (complaint_form.cleaned_data ['complaint_block'])
            attr_block = Attribute.objects.get (value = str_block, category__key = str_block)
            print attr_block.value
        except Attribute.DoesNotExist:
            errors.append ('Incorrect Selection for Block')

        print errors

        return render_to_response ('complaint_submitted.html')
    else:
        states = country.attribute_set.all ()
        depts  = Attribute.objects.filter (category__key = 'Complaint Department')
        return render_to_response ('complaint.html',
                                   {'states' : _prepare_select_element (states),
                                    'departments' : _prepare_select_element (depts),
                                    'errors' : complaint_form.errors})


