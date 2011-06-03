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
from django.db.models import Avg, Max, Min, Count, Q
from django.contrib.auth.decorators import login_required

from cmh.common.models import Country, State, District
from cmh.common.models import Block, GramPanchayat, Village
from cmh.common.models import ComplaintType, StatusTransition
from cmh.common.models import AppRole

from cmh.common.utils import debug

from cmh.issuemgr.constants import STATUS_NEW, STATUS_REOPEN, STATUS_ACK
from cmh.issuemgr.constants import STATUS_OPEN, STATUS_RESOLVED, STATUS_CLOSED
from cmh.issuemgr.constants import HotComplaintPeriod

from cmh.issuemgr.models import Complaint
from cmh.issuemgr.forms import ComplaintForm, ComplaintLocationBox, ComplaintTypeBox
from cmh.issuemgr.forms import ComplaintTrackForm
from cmh.issuemgr.forms import ComplaintDepartmentBox, ComplaintUpdateForm, HotComplaintForm
from cmh.issuemgr.forms import AcceptComplaintForm, LOCATION_REGEX, DepartmentIdList

from cmh.smsgateway.models import TextMessage

from cmh.usermgr.constants import UserRoles
from cmh.usermgr.utils import get_user_menus


def index (request):
    if request.method == 'GET':
        try:
            form = ComplaintForm ()
            return render_to_response ('complaint.html',
                                       {'form' : form,
                                        'menus' : get_user_menus (request.user,index),
                                        'user' : request.user,
                                        'val':'Submit Issue',
                                        'post_url' : reverse (index),
                                        'map' : {'center_lat' : 23.20119,
                                                 'center_long' : 77.081795,
                                                 'zoom_level' : 13}})
        except:
            import traceback
            traceback.print_exc ()
    elif request.method == 'POST':
        form = ComplaintForm (request.POST)
        if form.is_valid ():
            complaint = form.save (None)
            debug ("Sending message for complaint acceptance")
            TextMessage.objects.queue_text_message (complaint.filedby.mobile,
                                                    "Your complaint is registered. Ref Num: " + complaint.complaintno)
            return render_to_response ('complaint_submitted.html',
                                       {'menus' : get_user_menus (request.user,index),
                                        'user' : request.user,
                                        'complaint' : complaint})
        else:
            return render_to_response ('complaint.html',
                                       {'form': form,
                                        'errors' : form.errors,
                                        'menus' : get_user_menus (request.user,index),
                                        'user' : request.user,
                                        'post_url' : reverse (index),
                                        'map' : {'center_lat' : 23.20119,
                                                 'center_long' : 77.081795,
                                                 'zoom_level' : 13}})
    else:
        return HttpResponse ()


ALL_DEPT_ID = 0
def get_category_map_update (request):
    try:
        print request.POST
        form = DepartmentIdList (request.POST)
        if form.is_valid ():
            ids = form.cleaned_data ['departments']
            complaints = Complaint.objects.filter (latest = True).order_by ('location')

            if not ALL_DEPT_ID in ids:
                complaints = complaints.filter (department__id__in = ids)

            debug ("Count of complaints: " + str (complaints.count ()))

            retval = {}
            for complaint in complaints:
                location = complaint.location
                if location != None:
                    if retval.has_key (location.id):
                        retval [location.id]['count'] += 1
                    else:
                        retval [complaint.location.id] = {'count' : 1,
                                                          'name' : location.name,
                                                          'latitude': location.lattd,
                                                          'longitude' : location.longd}

            return HttpResponse (json.dumps (retval))
        else:
            print "form is not valid"
            return HttpResponse (json.dumps ({}))
    except:
        import traceback
        traceback.print_exc ()



def locations (request):
    try:
        form = ComplaintLocationBox (request.GET)
        if form.is_valid ():
            term = form.cleaned_data ['term']
            matches = re.search (LOCATION_REGEX, term)
            g = matches.groups ()
            villages = Village.objects.filter (search__icontains = term.lower ())
            names = [{'display' : village.name,
                      'detail' : ('Gram Panchayat: %s<br/>Block: %s' %
                                  (village.grampanchayat.name,
                                   village.grampanchayat.block.name)),
                      'id' : village.id}
                     for village in Village.objects.filter (search__icontains
                                                            = term.lower ())]
            return HttpResponse (json.dumps (names))
        else:
            debug ("Form is invalid: " + str (form.errors))
    except:
        debug ("General exception")
        import traceback
        traceback.print_exc ()
    return HttpResponse (json.dumps ([]))


def categories (request):
    try:
        form = ComplaintTypeBox (request.GET)
        if form.is_valid ():
            retvals = []
            words = set ([x.lower () for x in form.cleaned_data ['term'].split ()])


            complaint_types = ComplaintType.objects.all ()
            for word in words:
                complaint_types = complaint_types.filter (search__icontains = word)

            for cpl_type in complaint_types:
                retvals.append ({'display' : cpl_type.summary,
                                 'detail' : ('%s<br/>Department: %s' %
                                             (cpl_type.cclass,
                                              cpl_type.department.name)),
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
def metrics (request):
    its = []
    cs = Complaint.objects.filter (latest = True)
    complaint_types = ComplaintType.objects.all ().order_by ('id')
    for issue_type in complaint_types:
        its.append ({'name' : issue_type.summary,
                     'new_reopened' : cs.filter ((Q (curstate = STATUS_NEW) |
                                                  Q (curstate = STATUS_REOPEN)),
                                                 complainttype = issue_type).count (),
                     'acknowledged' : cs.filter (complainttype = issue_type,
                                                 curstate = STATUS_ACK).count (),
                     'opened' : cs.filter (complainttype = issue_type,
                                           curstate = STATUS_OPEN).count (),
                     'resolved' : cs.filter (complainttype = issue_type,
                                             curstate = STATUS_RESOLVED).count (),
                     'closed' : cs.filter (complainttype = issue_type,
                                           curstate = STATUS_CLOSED).count ()})
    return render_to_response ('complaint_metrics.html',
                               {'issue_types' : its,
                                'menus' : get_user_menus (request.user,metrics),
                                'user' : request.user})


@login_required
def accept (request):
    if request.method == 'GET':
        form = AcceptComplaintForm ()
        return render_to_response ('complaint.html', {'form' : form,
                                                      'menus' : get_user_menus (request.user,accept),
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
                                       {'menus' : get_user_menus (request.user,accept),
                                        'user' : request.user,
                                        'complaint' : complaint})
        else:
            return render_to_response ('complaint.html',
                                       {'form': form,
                                        'menus' : get_user_menus (request.user,accept),
                                        'user' : request.user,
                                        'post_url' : reverse (accept),
                                        'map' : {'center_lat' : 23.20119,
                                                 'center_long' : 77.081795,
                                                 'zoom_level' : 13}})
    else:
        pass


@login_required
def all_issues (request):
    issues = Complaint.objects.filter (latest = True)

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
                               {'menus' : get_user_menus (request.user,all_issues),
                                'user' : request.user,
                                'issues' : issues})

@login_required
def my_issues (request):
    role = AppRole.objects.get_user_role (request.user)
    statuses = StatusTransition.objects.get_changeable_statuses (role)
    issues = Complaint.objects.get_latest_complaints ().filter (curstate__in = statuses).order_by ('-created')

    role = request.user.cmhuser.get_user_role ()
    if role == UserRoles.ROLE_OFFICIAL or role == UserRoles.ROLE_DELEGATE:
        official = request.user.official
        issues = issues.filter (department__in = official.departments.all ())

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
                                'menus' : get_user_menus (request.user,my_issues),
                                'user' : request.user})


def update (request, complaintno, complaintid):
    complaints = Complaint.objects.filter (complaintno = complaintno).order_by ('-created')
    base = complaints.get (original = None)
    current = complaints.get (latest = True)
    user_role = AppRole.objects.get_user_role (request.user)
    newstatuses = StatusTransition.objects.get_allowed_statuses (user_role, current.curstate)

    if newstatuses.count () == 0:
        return render_to_response ('update-cannot-do.html',
                                   {'menus' : get_user_menus (request.user,update),
                                    'user' : request.user})
    else:
        if request.method == 'GET':
            if request.META.has_key ('HTTP_REFERER'):
                prev_page = request.META ['HTTP_REFERER']
            else:
                prev_page = reverse (track_issues, args = [complaintno,current.id])

            return render_to_response ('update.html',
                                       {'form' : ComplaintUpdateForm (current,
                                                                      newstatuses),
                                        'base' : base,
                                        'current' : current,
                                        'complaints' : complaints,
                                        'newstatuses' : newstatuses,
                                        'menus' : get_user_menus (request.user,update),
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
                    form.save (request.user)
                    return HttpResponseRedirect (prev_page)
                else:
                    return render_to_response ('update.html',
                                               {'form' : form,
                                                'base' : base,
                                                'current' : current,
                                                'complaints' : complaints,
                                                'newstatuses' : newstatuses,
                                                'menus' : get_user_menus (request.user,update),
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
                                'menus' : get_user_menus (request.user,track_issues),
                                'user' : request.user,
                                'updatable' : updatable})

def track (request):
    if request.method == "GET":
        return render_to_response ('track.html',
                                   {'user' : request.user,
                                    'menus' : get_user_menus (request.user, track),
                                    'val':'Track Issue',
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
                                        'menus' : get_user_menus (request.user,track),
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

            now = datetime.now ()
            period1 = now - reldelta
            period2 = period1 - reldelta
            period3 = period2 - reldelta
            period4 = period3 - reldelta

            # FIXME: remove 'exclude (base = None)' once the form to "update"
            # a new issue to acked issue is fixed to update the issuetype ('base')
            # instead of just the department.
            period_issues = Complaint.objects.filter (created__lte = now, created__gt = period4, original = None).exclude (complainttype = None)

            issue_codes = set ([issue.complainttype.id for issue in period_issues])

            issue_table = []
            for issue_code in issue_codes:
                issue_table.append ((issue_code, period_issues.filter (complainttype__id = issue_code).count ()))
            issue_table = sorted (issue_table, key = (lambda x: x[1]), reverse = True)
            issue_table = issue_table [:5]

            periods = [(now, period1), (period1, period2), (period2, period3), (period3, period4)]

            datapoints = []
            issuetypes = []
            for issue_id, issue_count in issue_table:
                datapoints.append ([[te.strftime ("%Y-%m-%d 12:01AM"),
                                     period_issues.filter (complainttype__id = issue_id,
                                                           created__lte = te,
                                                           created__gte = ts).count ()]
                                    for te, ts in periods])
                ct = ComplaintType.objects.get (id = issue_id)
                issuetypes.append ({'label': ct.summary, 'showLabel': True})
        except:
            import traceback
            traceback.print_exc ()
    retval = {'datapoints' : datapoints,
              'x_interval' : x_interval,
              'issuetypes' : issuetypes}
    return HttpResponse (json.dumps (retval))


