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

from datetime import datetime, date, timedelta
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
from cmh.common.models import AppRole, ComplaintDepartment

from cmh.common.utils import debug, daterange
from cmh.common.utils import get_datatables_records

from cmh.issuemgr.constants import STATUS_NEW, STATUS_REOPEN, STATUS_ACK
from cmh.issuemgr.constants import STATUS_OPEN, STATUS_RESOLVED, STATUS_CLOSED
from cmh.issuemgr.constants import HotComplaintPeriod

from cmh.issuemgr.models import Complaint
from cmh.issuemgr.forms import ComplaintForm, ComplaintLocationBox, ComplaintTypeBox, Report
from cmh.issuemgr.forms import ComplaintTrackForm
from cmh.issuemgr.forms import ComplaintDepartmentBox, ComplaintUpdateForm, HotComplaintForm
from cmh.issuemgr.forms import AcceptComplaintForm, LOCATION_REGEX, ComplaintDisplayParams

from cmh.smsgateway.models import TextMessage

from cmh.common.constants import UserRoles
from cmh.usermgr.utils import get_user_menus


def index (request):
    if request.method == 'GET':
        try:
            form = ComplaintForm ()
            return render_to_response ('complaint.html',
                                       {'form' : form,
                                        'menus' : get_user_menus (request.user,index),
                                        'user' : request.user,
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
        form = ComplaintDisplayParams (request.POST)
        if form.is_valid ():
            deptids = form.cleaned_data ['departments']
            stdate = form.cleaned_data ['stdate']
            endate = form.cleaned_data ['endate']
            dttm_start = datetime (stdate.year, stdate.month, stdate.day, 0, 0, 0)
            dttm_end   = datetime (endate.year, endate.month, endate.day, 23, 59, 59)

            complaints = Complaint.objects.filter (latest = True, created__gte = dttm_start, created__lte = dttm_end)
            complaints = complaints.filter (Q (curstate = STATUS_NEW) | Q (curstate = STATUS_ACK) | Q (curstate = STATUS_REOPEN) | Q (curstate = STATUS_OPEN))

            if not ALL_DEPT_ID in deptids:
                complaints = complaints.filter (department__id__in = deptids)

            datalevel = form.cleaned_data ['datalevel']
            if datalevel == 'villg':
                ann_str = 'location'
            elif datalevel == 'gramp':
                ann_str = 'location__grampanchayat'
            elif datalevel == 'block':
                ann_str = 'location__grampanchayat__block'
            elif datalevel == 'distt':
                ann_str = 'location__grampanchayat__block__district'
            elif datalevel == 'state':
                ann_str = 'location__grampanchayat__block__district__state'
            else:
                raise Exception ("Invalid data level : " + datalevel)

            records = complaints.values (ann_str + '__id', ann_str, ann_str + '__name', ann_str + '__lattd', ann_str + '__longd').annotate (count = Count (ann_str))
            retval = {}
            for record in records:
                retval [record [ann_str + '__id']] = {'count' : record ['count'],
                                                      'name' : record [ann_str + '__name'],
                                                      'latitude' : record [ann_str + '__lattd'],
                                                      'longitude' : record [ann_str + '__longd']}

            return HttpResponse (json.dumps (retval))
        else:
            debug ("form is not valid")
            return HttpResponse (json.dumps ({}))
    except:
        debug ("exception in return complaint data")
        import traceback
        traceback.print_exc ()
        return HttpResponse (json.dumps ({}))


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
    return render_to_response ('all_issues.html',
                               {'menus' : get_user_menus (request.user,all_issues),
                                'user' : request.user})

@login_required
def all_issues_list (request):
    querySet = Complaint.objects.get_latest_complaints ().order_by ('-created')

    columnIndexNameMap = { 0: 'complaintno',
                           1: 'logdate',
                           2: 'description',
                           3: 'curstate',
                           4: 'created'}

    return get_datatables_records(request, querySet, columnIndexNameMap, 'issue_entity_datatable.html')

@login_required
def my_issues (request):
    return render_to_response ('my_issues.html',
                               {'menus' : get_user_menus (request.user, my_issues),
                                'user' : request.user})


@login_required
def my_issues_list (request):
    role = AppRole.objects.get_user_role (request.user)
    statuses = StatusTransition.objects.get_changeable_statuses (role)
    querySet = Complaint.objects.get_latest_complaints ().filter (curstate__in = statuses).order_by ('-created')

    role = request.user.cmhuser.get_user_role ()
    if role == UserRoles.ROLE_OFFICIAL or role == UserRoles.ROLE_DELEGATE:
        official = request.user.official
        querySet = querySet.filter (department__in = official.departments.all ())

    columnIndexNameMap = { 0: 'complaintno',
                           1: 'logdate',
                           2: 'description',
                           3: 'curstate',
                           4: 'created'}

    return get_datatables_records (request, querySet, columnIndexNameMap, 'issue_entity_datatable.html')


def update (request, complaintno):
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
                prev_page = reverse (track_issues, args = [complaintno])

            return render_to_response ('update.html',
                                       {'form' : ComplaintUpdateForm (current, newstatuses),
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
                prev_page = reverse (track_issues, args = [complaintno])

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

def track_issues (request, complaintno):
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
                                    'form' : ComplaintTrackForm ()})
    else:
        form = ComplaintTrackForm (request.POST)
        if form.is_valid ():
            complaintno = form.cleaned_data ['complaintno']
            current = Complaint.objects.get (complaintno = complaintno, latest = True)
            return HttpResponseRedirect (reverse (track_issues,
                                                  args = [form.cleaned_data ['complaintno']]))
        else:
            return render_to_response ('track.html',
                                       {'user' : request.user,
                                        'menus' : get_user_menus (request.user,track),
                                        'form' : form})

def hot_complaints (request):
    try:
        form = HotComplaintForm (request.GET)
        if form.is_valid ():
            stdate = form.cleaned_data ['stdate']
            endate = form.cleaned_data ['endate']
            deptids = form.cleaned_data ['departments']

            complaints = Complaint.objects.filter (createdate__lte = endate, latest = True)
            open_complaints = complaints.filter (Q (curstate = STATUS_NEW) | Q (curstate = STATUS_ACK) | Q (curstate = STATUS_REOPEN) | Q (curstate = STATUS_OPEN))
            clos_complaints = complaints.filter (Q (curstate = STATUS_RESOLVED) | Q (curstate = STATUS_CLOSED))

            if ALL_DEPT_ID in deptids:
                departments = ComplaintDepartment.objects.all ()
            else:
                departments = ComplaintDepartment.objects.filter (id__in = deptids)

            data  = []
            names = []
            dates = [d for d in daterange (stdate, endate)]
            for dept in departments:
                names.append (dept.name)
                doc = open_complaints.filter (department__id = dept.id)
                dcc = clos_complaints.filter (department__id = dept.id)
                data.append ([[d.strftime ('%Y-%m-%d 12:01 AM'), doc.filter (createdate__lte = d).count () - dcc.filter (createdate__lte = d).count ()]
                              for d in dates])

            return HttpResponse (json.dumps ({'datapoints' : data, 'names' : names}))
        else:
            return HttpResponse (json.dumps ({'datapoints' : [[]], 'names' : []}))
    except:
        import traceback
        traceback.print_exc ()


def report(request) :
    if request.method=="GET" :
        form = Report ()
        return render_to_response('reportselection.html',
                                 {'form':form,
                                  'menus' : get_user_menus (request.user,report),
                                 'user' : request.user})
    elif request.method=="POST" :
        return render_to_response('report.html',
                                 {'menus' : get_user_menus (request.user,report),
                                  'user' : request.user})

