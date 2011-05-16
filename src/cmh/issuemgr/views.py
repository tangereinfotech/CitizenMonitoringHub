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

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Avg, Max, Min, Count
from django.contrib.auth.decorators import login_required

from cmh.common.models import Category, Attribute, CodeName, LatLong
from cmh.common.models import get_code2name, get_child_attributes

from cmh.issuemgr.constants import VILLAGES, COMPLAINT_TYPES, DEPARTMENTS
from cmh.issuemgr.models import ComplaintItem, Complaint, StatusTransition
from cmh.issuemgr.forms import ComplaintForm, ComplaintLocationBox, ComplaintTypeBox
from cmh.issuemgr.forms import ComplaintTrackForm
from cmh.issuemgr.forms import ComplaintDepartmentBox, ComplaintUpdateForm, HotComplaintForm
from cmh.issuemgr.constants import HotComplaintPeriod
from cmh.issuemgr.forms import AcceptComplaintForm, LOCATION_REGEX

from cmh.usermgr.models import AppRole
from cmh.usermgr.models import ROLE_ANONYMOUS, ROLE_CSO, ROLE_DELEGATE, ROLE_OFFICIAL, ROLE_DM
from cmh.usermgr.utils import get_user_menus


def index (request):
    if request.method == 'GET':
        form = ComplaintForm ()
        return render_to_response ('complaint.html',
                                   {'form' : form,
                                    'menus' : get_user_menus (request.user),
                                    'user' : request.user,
                                    'post_url' : reverse (index),
                                    'map' : {'center_lat' : 23.20119,
                                             'center_long' : 77.081795,
                                             'zoom_level' : 13}})
    elif request.method == 'POST':
        form = ComplaintForm (request.POST)
        if form.is_valid ():
            complaint = form.save (None)
            return render_to_response ('complaint_submitted.html',
                                       {'menus' : get_user_menus (request.user),
                                        'user' : request.user,
                                        'complaint' : complaint})
        else:
            return render_to_response ('complaint.html',
                                       {'form': form,
                                        'errors' : form.errors,
                                        'menus' : get_user_menus (request.user),
                                        'user' : request.user,
                                        'post_url' : reverse (index),
                                        'map' : {'center_lat' : 23.20119,
                                                 'center_long' : 77.081795,
                                                 'zoom_level' : 13}})
    else:
        return HttpResponse ()

def get_category_map_update (request, category):
    if category == 'all':
        complaints = Complaint.objects.all ().order_by ('location')
        retval = {}
        for complaint in complaints:
            if retval.has_key (complaint.location.id):
                retval [complaint.location.id]['count'] += 1
            else:
                try:
                    latlong = LatLong.objects.get (location__id = complaint.location.id)
                    retval [complaint.location.id] = {'count' : 1,
                                                      'latitude': latlong.latitude,
                                                      'longitude' : latlong.longitude}
                except:
                    pass
        return HttpResponse (json.dumps (retval))
    else:
        return HttpResponse (json.dumps ([]))


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


def departments (request):
    try:
        form = ComplaintDepartmentBox (request.GET)
        if form.is_valid ():
            retvals = []
            term = form.cleaned_data ['term']
            for department in DEPARTMENTS:
                dept_code = department.value
                dept_name = CodeName.objects.get (code = dept_code).name

                if term.lower () in dept_name.lower ():
                    retvals.append ({'display' : dept_name,
                                     'id' : department.id,
                                     'detail' : ''})
            return HttpResponse (json.dumps (retvals))

    except:
        import traceback
        traceback.print_exc ()
    return HttpResponse (json.dumps ([]))


@login_required
def accept (request):
    if request.method == 'GET':
        form = AcceptComplaintForm ()
        return render_to_response ('complaint.html', {'form' : form,
                                                      'menus' : get_user_menus (request.user),
                                                      'user' : request.user,
                                                      'post_url' : reverse (accept),
                                                      'map' : {'center_lat' : 23.20119,
                                                               'center_long' : 77.081795,
                                                               'zoom_level' : 13}})
    elif request.method == 'POST':
        form = AcceptComplaintForm (request.POST)
        if form.is_valid ():
            complaint = form.save (request.user)
            return render_to_response ('complaint_submitted.html',
                                       {'menus' : get_user_menus (request.user),
                                        'user' : request.user,
                                        'complaint' : complaint})
        else:
            return render_to_response ('complaint.html', {'form': form,
                                                          'menus' : get_user_menus (request.user),
                                                          'user' : request.user,
                                                          'post_url' : reverse (accept),
                                                          'map' : {'center_lat' : 23.20119,
                                                                   'center_long' : 77.081795,
                                                                   'zoom_level' : 13}})
    else:
        pass


@login_required
def my_issues (request):
    role = AppRole.objects.get_user_role (request.user)
    statuses = StatusTransition.objects.get_changeable_statuses (role)
    issues = Complaint.objects.get_latest_complaints ().filter (curstate__in = statuses).order_by ('-created')
    paginator = Paginator (issues, 10)

    try:
        page = int (request.GET.get ('page', '1'))
    except ValueError:
        page = 1

    try:
        issues = paginator.page (page)
    except (EmptyPage, InvalidPage):
        issues = paginator.page (paginator.num_pages)

    return render_to_response ('my_issues.html',
                               {'issues' : issues,
                                'menus' : get_user_menus (request.user),
                                'user' : request.user})


def update (request, complaintno, complaintid):
    complaints = Complaint.objects.filter (complaintno = complaintno).order_by ('-created')
    base = complaints.get (original = None)
    current = complaints.get (latest = True)
    user_role = AppRole.objects.get_user_role (request.user)
    newstatuses = StatusTransition.objects.get_allowed_statuses (user_role,
                                                                 current.curstate)

    if newstatuses.count () == 0:
        return render_to_response ('update-cannot-do.html',
                                   {'menus' : get_user_menus (request.user),
                                    'user' : request.user})
    else:
        if request.method == 'GET':
            if request.META.has_key ('HTTP_REFERER'):
                prev_page = request.META ['HTTP_REFERER']
            else:
                prev_page = reverse (track_issues, args = [complaintno,current.id])

            return render_to_response ('update.html',
                                       {'form' : ComplaintUpdateForm (current, newstatuses),
                                        'base' : base,
                                        'current' : current,
                                        'complaints' : complaints,
                                        'newstatuses' : newstatuses,
                                        'menus' : get_user_menus (request.user),
                                        'user' : request.user,
                                        'prev' : prev_page})
        elif request.method == 'POST':
            # FIXME: Ensure that the isue state transition complies to
            # the desginated role permissions
            if request.POST.has_key ('prev'):
                prev_page = request.POST ['prev']
            elif request.META.has_key ('HTTP_REFERER'):
                prev_page = request.META ['HTTP_REFERER']
            else:
                prev_page = reverse (track_issues, args = [complaintno,current.id])

            if request.POST.has_key ('save'):
                form = ComplaintUpdateForm (current, newstatuses, request.POST)
                if form.is_valid ():
                    form.save ()
                    return HttpResponseRedirect (prev_page)
                else:
                    return render_to_response ('update.html',
                                               {'form' : form,
                                                'base' : base,
                                                'current' : current,
                                                'complaints' : complaints,
                                                'newstatuses' : newstatuses,
                                                'menus' : get_user_menus (request.user),
                                                'user' : request.user,
                                                'prev' : prev_page})
            elif request.POST.has_key ('cancel'):
                return HttpResponseRedirect (prev_page)
            else:
                return HttpResponseRedirect ("/")
        else:
            pass

def track_issues (request, complaintno, complaintid):
    complaints = Complaint.objects.filter (complaintno = complaintno).order_by ('-created')
    base = complaints.get (original = None)
    current = complaints.get (latest = True)
    user_role = AppRole.objects.get_user_role (request.user)
    newstatuses = StatusTransition.objects.get_allowed_statuses (user_role, current.curstate)

    if newstatuses.count () == 0:
        updatable = False
    else:
        updatable = True

    return render_to_response ('track_issues.html',
                               {'base' : base,
                                'current' : current,
                                'complaints' : complaints,
                                'menus' : get_user_menus (request.user),
                                'user' : request.user,
                                'updatable' : updatable})

def track (request):
    if request.method == "GET":
        return render_to_response ('track.html',
                                   {'user' : request.user,
                                    'menus' : get_user_menus (request.user),
                                    'form' : ComplaintTrackForm ()})
    else:
        form = ComplaintTrackForm (request.POST)
        if form.is_valid ():
            complaintno = form.cleaned_data ['complaintno']
            current = Complaint.objects.get (complaintno = complaintno, latest = True)
            return HttpResponseRedirect (reverse (track_issues,
                                                  args = [form.cleaned_data ['complaintno'],
                                                          current.id]))
        else:
            return render_to_response ('track.html',
                                       {'user' : request.user,
                                        'menus' : get_user_menus (request.user),
                                        'form' : form})


def hot_complaints (request):
    form = HotComplaintForm (request.GET)
    if form.is_valid ():
        try:
            reqperiod = form.cleaned_data ['period']
            if reqperiod == HotComplaintPeriod.WEEK:
                x_interval = '1 week'
                reldelta = relativedelta (weeks = +1)
            elif reqperiod == HotComplaintPeriod.MONTH:
                x_interval = '1 month'
                reldelta = relativedelta (months = +1)
            elif reqperiod == HotComplaintPeriod.QUARTER:
                x_interval = '3 month'
                reldelta = relativedelta (months = +3)
            else:
                x_interval = '1 week'
                reldelta = relativedelta (weeks = +1)

            now = date.today ()
            period1 = now - reldelta
            period2 = period1 - reldelta
            period3 = period2 - reldelta
            period4 = period3 - reldelta

            # FIXME: remove 'exclude (base = None)' once the form to "update"
            # a new issue to acked issue is fixed to update the issuetype ('base')
            # instead of just the department.
            period_issues = Complaint.objects.filter (created__lte = now, created__gt = period4, original = None).exclude (base = None)

            issue_codes = set ([issue.base.id for issue in period_issues])

            issue_table = []
            for issue_code in issue_codes:
                issue_table.append ((issue_code, period_issues.filter (base__id = issue_code).count ()))
            issue_table = sorted (issue_table, key = (lambda x: x[1]), reverse = True)
            issue_table = issue_table [:5]

            periods = [(now, period1), (period1, period2), (period2, period3), (period3, period4)]

            datapoints = []
            issuetypes = []
            for issue_entry in issue_table:
                datapoints.append ([[te.strftime ("%Y-%m-%d 12:01AM"),
                                     period_issues.filter (base__id = issue_entry [0],
                                                           created__lte = te,
                                                           created__gte = ts).count ()]
                                    for te, ts in periods])
                issueattr = COMPLAINT_TYPES.get (id = issue_entry [0])
                issuetypes.append ({'label': CodeName.objects.get (code = issueattr.value).name,
                                    'showLabel': True})
        except:
            import traceback
            traceback.print_exc ()
    return HttpResponse (json.dumps ({'datapoints' : datapoints,
                                      'x_interval' : x_interval,
                                      'issuetypes' : issuetypes}))


