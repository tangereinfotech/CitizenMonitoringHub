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

import re, os
import itertools

from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core import serializers
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils import simplejson as json
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Avg, Max, Min, Count, Q
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.conf import settings
from django.utils.translation import ugettext as _

from cmh.common.models import Country, State, District
from cmh.common.models import Block, GramPanchayat, Village
from cmh.common.models import ComplaintType, StatusTransition
from cmh.common.models import AppRole, ComplaintDepartment

from cmh.common.utils import debug, daterange
from cmh.common.utils import get_datatables_records
from cmh.common.utils import get_session_data, set_session_data
from cmh.common.utils import get_evidence_url, timedelta_to_days

from cmh.issuemgr.constants import STATUS_NEW, STATUS_REOPEN, STATUS_ACK
from cmh.issuemgr.constants import STATUS_OPEN, STATUS_RESOLVED, STATUS_CLOSED
from cmh.issuemgr.constants import HotComplaintPeriod

from cmh.issuemgr.models import Complaint, ComplaintEvidence, ComplaintReminder, ComplaintClosureMetric
from cmh.issuemgr.forms import ComplaintForm, ComplaintLocationBox, ComplaintTypeBox, Report
from cmh.issuemgr.forms import ComplaintTrackForm, LocationStatsForm, ReportForm
from cmh.issuemgr.forms import ComplaintDepartmentBox, ComplaintUpdateForm, HotComplaintForm
from cmh.issuemgr.forms import AcceptComplaintForm, LOCATION_REGEX, ComplaintDisplayParams
from cmh.issuemgr.forms import SetComplaintReminder

from cmh.smsgateway.utils import queue_complaint_update_sms

from cmh.common.constants import UserRoles
from cmh.usermgr.utils import get_user_menus

MY_ISSUES_MODE  = 'my-issues-mode'
ALL_ISSUES_MODE = 'all-issues-mode'


def index (request):
    if request.method == 'GET':
        try:
            form = ComplaintForm ()
            return render_to_response ('complaint.html',
                                       {'form' : form,
                                        'menus' : get_user_menus (request.user,index),
                                        'user' : request.user,
                                        'post_url' : reverse (index)})
        except:
            import traceback
            traceback.print_exc ()
    elif request.method == 'POST':
        form = ComplaintForm (request.POST, request.FILES)
        if form.is_valid ():
            complaint = form.save (None)

            # Handle files
            if 'filename' in request.FILES and request.FILES ['filename'] != None:
                _handle_evidence_upload (complaint, request.FILES ['filename'])

            debug ("Sending message for complaint acceptance")

            if complaint.complainttype != None:
                sms = complaint.complainttype.defsmsnew
            else:
                # HACK ALERT - complaint type is not known so just pick any complaint type and pick its defsmsnew
                complainttypes = ComplaintType.objects.exclude (Q (defsmsnew = '') | Q (defsmsnew = None))
                if complainttypes.count () != 0:
                    sms = complainttypes [0].defsmsnew
                else:
                    sms = None

            if sms != None:
                queue_complaint_update_sms (complaint.filedby.mobile, sms, complaint)

            return render_to_response ('complaint_submitted.html',
                                       {'menus' : get_user_menus (request.user,index),
                                        'user' : request.user,
                                        'complaint' : complaint})
        else:
            return render_to_response ('complaint.html',
                                       {'form' : form,
                                        'errors' : form.errors,
                                        'menus' : get_user_menus (request.user,index),
                                        'user' : request.user,
                                        'post_url' : reverse (index)})
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

            complaints = Complaint.objects.filter (curstate = STATUS_NEW, created__gte = dttm_start, created__lte = dttm_end)
            complaintnos = complaints.values_list('complaintno', flat=True).distinct() #[c.complaintno for c in complaints]

            open_states = [STATUS_NEW, STATUS_ACK, STATUS_OPEN, STATUS_REOPEN]

            complaints = Complaint.objects.filter(curstate__in = open_states, complaintno__in = complaintnos, created__lte = dttm_end).filter(latest = True)

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
                                                      'id' : record [ann_str + '__id'],
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


def getstats (request):
    form = LocationStatsForm (request.POST)

    if form.is_valid ():
        deptids = form.cleaned_data ['departments']
        stdate = form.cleaned_data ['stdate']
        endate = form.cleaned_data ['endate']
        dttm_start = datetime (stdate.year, stdate.month, stdate.day, 0, 0, 0)
        dttm_end   = datetime (endate.year, endate.month, endate.day, 23, 59, 59)

        complaints = Complaint.objects.filter (curstate = STATUS_NEW, created__gte = dttm_start, created__lte = dttm_end)
        #complaintnos = [c.complaintno for c in complaints]
        #rel_complaint_ids = []
        #for cno in complaintnos:
        #    cid = Complaint.objects.filter(complaintno = cno, created__lte = dttm_end).exclude(curstate = STATUS_CLOSED).order_by('-created')[0].pk
        #    rel_complaint_ids.append(cid)
        open_states = [STATUS_NEW, STATUS_ACK, STATUS_OPEN, STATUS_REOPEN]
        #complaints = Complaint.objects.filter(pk__in = rel_complaint_ids).filter(curstate__in = open_states)

        complaintnos = complaints.values_list('complaintno', flat=True).distinct() #[c.complaintno for c in complaints]


        complaints = Complaint.objects.filter(curstate__in = open_states, complaintno__in = complaintnos, created__lte = dttm_end).filter(latest = True)

        if not ALL_DEPT_ID in deptids:
            complaints = complaints.filter (department__id__in = deptids)

        datalevel = form.cleaned_data ['datalevel']
        locid = form.cleaned_data ['locid']

        if datalevel == 'villg':
            loctype = _("Village")
            location = Village.objects.get (id = locid)
            complaints = complaints.filter (location__id = locid)
            uptype = _('Gram Panchayat')
            upname = location.grampanchayat.name
        elif datalevel == 'gramp':
            loctype = _("gramp")
            location = GramPanchayat.objects.get (id = locid)
            complaints = complaints.filter (location__grampanchayat__id = locid)
            uptype = 'Block'
            upname = location.block.name
        elif datalevel == 'block':
            loctype = _("Block")
            location = Block.objects.get (id = locid)
            complaints = complaints.filter (location__grampanchayat__block__id = locid)
            uptype = 'District'
            upname = location.district.name
        elif datalevel == 'distt':
            loctype = "District"
            location = District.objects.get (id = locid)
            complaints = complaints.filter (location__grampanchayat__block__district__id = locid)
            uptype = 'State'
            upname = location.state.name
        elif datalevel == 'state':
            loctype = "State"
            location = State.objects.get (id = locid)
            complaints = complaints.filter (location__grampanchayat__block__district__state__id = locid)
            uptype = 'Country'
            upname = location.country.name
        else:
            raise InvalidDataException ("Invalid data level specified")

        dept_complaints = [{'name' : c ['department__name'],
                            'count' : c ['count']}
                           for c in complaints.values ('department__name', 'department__id').annotate (count=Count ('department__name')).order_by ('department__id')]

        stats = {'count'      : complaints.count (),
                 'name'       : location.name,
                 'type'       : loctype,
                 'locid'      : location.id,
                 'departments': dept_complaints,
                 'uptype'     : uptype,
                 'upname'     : upname,
                 'uncat'      : complaints.filter (department = None).count ()}
        infowindow_data = loader.render_to_string ('location_stats.html', {'stats' : stats})
        return HttpResponse (json.dumps ({'infowindow_data' : infowindow_data,
                                          'loctype' : loctype,
                                          'locid' : location.id}))
    else:
        return HttpResponse ("");


def locations (request):
    try:
        form = ComplaintLocationBox (request.GET)
        if form.is_valid ():
            term = form.cleaned_data ['term']
            matches = re.search (LOCATION_REGEX, term)
            g = matches.groups ()
            villages = Village.objects.filter (search__icontains = term.lower ())
            names = [{'display' : village.name,
                      'detail' : (_('Gram Panchayat:')
                                  + village.grampanchayat.name +
                                  '<br/>' + _('Block: ') +
                                   village.grampanchayat.block.name),
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
                                 'detail' : (cpl_type.cclass + '<br/>' + _('Department: ') +
                                              cpl_type.department.name),
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
        return render_to_response ('accept.html', {'form' : form,
                                                   'menus' : get_user_menus (request.user,accept),
                                                   'user' : request.user,
                                                   'post_url' : reverse (accept)})
    elif request.method == 'POST':
        form = AcceptComplaintForm (request.POST, request.FILES)
        if form.is_valid ():
            complaint = form.save (request.user)

            if 'filename' in request.FILES and request.FILES ['filename'] != None:
                _handle_evidence_upload (complaint.original, request.FILES ['filename'])

            return render_to_response ('complaint_submitted.html',
                                       {'menus' : get_user_menus (request.user,accept),
                                        'user' : request.user,
                                        'complaint' : complaint})
        else:
            return render_to_response ('accept.html',
                                       {'form': form,
                                        'menus' : get_user_menus (request.user,accept),
                                        'user' : request.user,
                                        'post_url' : reverse (accept)})
    else:
        pass


@login_required
def all_issues (request):
    set_session_data (request, ALL_ISSUES_MODE, 'ALL')
    return render_to_response ('all_issues.html',
                               {'menus' : get_user_menus (request.user,all_issues),
                                'user' : request.user,
                                'mode' : 'all'})
@login_required
def all_mode_issues (request, mode):
    set_session_data (request, ALL_ISSUES_MODE, mode.upper ())
    return render_to_response ('all_issues.html',
                               {'menus' : get_user_menus (request.user,all_issues),
                                'user' : request.user,
                                'mode' : mode.lower ()})

@login_required
def all_issues_list (request):
    querySet = Complaint.objects.get_latest_complaints ()

    mode = get_session_data (request, ALL_ISSUES_MODE)
    if mode.lower () == 'rem':
        comp_reminders = ComplaintReminder.objects.filter (user = request.user, reminderon__lte = datetime.today ().date ())
        querySet = querySet.filter (complaintno__in = [c.complaintno for c in comp_reminders])

    querySet = querySet.order_by ('-created')

    columnIndexNameMap = { 0: 'complaintno',
                           1: 'logdate',
                           2: 'description',
                           3: 'curstate',
                           4: 'created'}

    return get_datatables_records(request, querySet, columnIndexNameMap, 'issue_entity_datatable.html')

@login_required
def my_issues (request):
    set_session_data (request, MY_ISSUES_MODE, 'ALL')
    return render_to_response ('my_issues.html',
                               {'menus' : get_user_menus (request.user, my_issues),
                                'user' : request.user,
                                'mode' : 'all'})

@login_required
def my_mode_issues (request, mode):
    set_session_data (request, MY_ISSUES_MODE, mode.upper ())
    return render_to_response ('my_issues.html',
                               {'menus' : get_user_menus (request.user, my_issues),
                                'user' : request.user,
                                'mode' : mode.lower ()})


@login_required
def my_issues_list (request):
    role = AppRole.objects.get_user_role (request.user)
    statuses = StatusTransition.objects.get_changeable_statuses (role)
    querySet = Complaint.objects.get_latest_complaints ()

    mode = get_session_data (request, MY_ISSUES_MODE)
    if mode.lower () == 'rem':
        comp_reminders = ComplaintReminder.objects.filter (user = request.user, reminderon__lte = datetime.today ().date ())
        querySet = querySet.filter (complaintno__in = [c.complaintno for c in comp_reminders])

    querySet = querySet.order_by ('-created')

    role = request.user.cmhuser.get_user_role ()
    if role == UserRoles.ROLE_OFFICIAL or role == UserRoles.ROLE_DELEGATE:
        official = request.user.official
        querySet = querySet.filter (department = official.department)

    columnIndexNameMap = { 0: 'complaintno',
                           1: 'logdate',
                           2: 'description',
                           3: 'curstate',
                           4: 'created'}

    return get_datatables_records (request, querySet, columnIndexNameMap, 'issue_entity_datatable.html')

from django.views.decorators.cache import cache_control
@cache_control(must_revalidate=True, max_age=1)
@login_required
def update (request, complaintno):
    complaints = Complaint.objects.filter (complaintno = complaintno).order_by ('-created')
    base = complaints.get (original = None)

    current = complaints [0]
    if complaints.filter (latest = True).count () != 1:
        complaints.update (latest = False)
        current.latest = True
        current.save ()

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
                form = ComplaintUpdateForm (current, newstatuses, request.POST, request.FILES)
                if form.is_valid ():
                    form.save (request.user)

                    # Handle files
                    if 'filename' in request.FILES and request.FILES ['filename']:
                        _handle_evidence_upload (base, request.FILES ['filename'])

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

from django.views.decorators.cache import cache_control
@cache_control(must_revalidate=True, max_age=1)
def track_issues (request, complaintno):
    complaintno = complaintno.strip ()
    try:
        complaints = Complaint.objects.filter (complaintno = complaintno).order_by ('-created')
        base = complaints.get (original = None)

        current = complaints [0]
        if complaints.filter (latest = True).count != 1:
            complaints.update (latest = False)
            current.latest = True
            current.save ()

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
                                    'menus' : get_user_menus (request.user, track_issues),
                                    'user' : request.user,
                                    'updatable' : updatable,
                                    'reminderform' : SetComplaintReminder (base)})
    except Complaint.DoesNotExist:
        return render_to_response ('track_issues_not_found.html',
                                   {'menus' : get_user_menus (request.user,track_issues),
                                    'user' : request.user,
                                    'complaintno' : complaintno})
    except:
        import traceback
        traceback.print_exc ()
        return render_to_response ('error.html',
                                   {'menus' : get_user_menus (request.user,track_issues),
                                    'user' : request.user})



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
            try:
                current = Complaint.objects.get (complaintno = complaintno, latest = True)
                return HttpResponseRedirect (reverse (track_issues,
                                                      args = [form.cleaned_data ['complaintno']]))
            except Complaint.DoesNotExist:
                return render_to_response ('track_issues_not_found.html',
                                           {'menus' : get_user_menus (request.user, track),
                                            'user' : request.user,
                                            'complaintno' : complaintno})
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

            all_departments = ComplaintDepartment.objects.all ().order_by ('id')
            if ALL_DEPT_ID in deptids:
                deptids = [dept.id for dept in all_departments]

            departments = ComplaintDepartment.objects.filter (id__in = deptids).order_by ('id')

            index = 0
            sel_depts = []
            for d in all_departments:
                if d in departments:
                    sel_depts.append ((index, d))
                index += 1

            names = []
            deptinfo = []
            for pos, dept in sel_depts:
                deptinfo.append ([dept.id, pos])
                names.append (dept.name)

            data = get_complaint_data (deptids, stdate, endate)
            vital_stats = get_vital_stats (deptids, stdate, endate)

            return HttpResponse (json.dumps ({'datapoints' : data, 'names' : names, 'departments' : deptinfo, 'vital_stats' : vital_stats}))
    except:
        import traceback
        traceback.print_exc ()
    vital_stats = {'newc' : 0,
                   'ack' : 0,
                   'ope' : 0,
                   'res' : 0,
                   'clo' : 0,
                   'reo' : 0,
                   'pen' : 0,
                   'unc' : 0}
    return HttpResponse (json.dumps ({'datapoints' : [[]], 'names' : [], 'departments' : [], 'vital_stats' : vital_stats}))

def get_vital_stats (deptids, stdate, endate):
    dttm_start = datetime (stdate.year, stdate.month, stdate.day, 0, 0, 0)
    dttm_end   = datetime (endate.year, endate.month, endate.day, 23, 59, 59)

    complaints = Complaint.objects.filter (created__gte = dttm_start, created__lte = dttm_end, curstate = STATUS_NEW)

    complaintnos = [c.complaintno for c in complaints]

    complaints = Complaint.objects.filter (complaintno__in = complaintnos)

    new_complaints = complaints.filter (curstate = STATUS_NEW)
    ack_complaints = complaints.filter (curstate = STATUS_ACK, department__in = deptids, created__lte = dttm_end)
    ope_complaints = complaints.filter (curstate = STATUS_OPEN, department__in = deptids, created__lte = dttm_end)
    res_complaints = complaints.filter (curstate = STATUS_RESOLVED, department__in = deptids, created__lte = dttm_end)
    clo_complaints = complaints.filter (curstate = STATUS_CLOSED, department__in = deptids, created__lte = dttm_end)
    reo_complaints = complaints.filter (curstate = STATUS_REOPEN, department__in = deptids, created__lte = dttm_end)
    pen_complaints = res_complaints.exclude (complaintno__in = [c.complaintno for c in clo_complaints] + [c.complaintno for c in reo_complaints])

    vital_stats = {'newc' : len (set ([c.complaintno for c in new_complaints])),
                   'ack' : len (set ([c.complaintno for c in ack_complaints])),
                   'ope' : len (set ([c.complaintno for c in ope_complaints])),
                   'res' : len (set ([c.complaintno for c in res_complaints])),
                   'clo' : len (set ([c.complaintno for c in clo_complaints])),
                   'reo' : len (set ([c.complaintno for c in reo_complaints])),
                   'pen' : len (set ([c.complaintno for c in pen_complaints]))}
    return vital_stats


def get_complaint_data (deptids, stdate, endate):

    from cmh.issuemgr.models import TrendChartSummary as TCS
    depts = ComplaintDepartment.objects.filter (id__in = deptids).order_by ('id')
    cdata = []
    for dep in depts:
        dep_row = []
        tcs = dep.trendchartsummary_set.filter(date__gte = stdate, date__lte = endate, filed_on__gte = stdate).values('date').annotate(count = Count('id')).order_by('date')
        for item in tcs:
            dep_row.append([item['date'].strftime("%Y-%m-%d 1:00 AM"), item['count']])
        if len(dep_row) == 0:
            dep_row = [[stdate.strftime("%Y-%m-%d 1:00 AM"), 0]]
        cdata.append(dep_row)
    return cdata


from cmh.issuemgr.models import ReportData

def get_report_stats (stdate, endate,
                      deptids,
                      stateids, disttids, blockids, grampids, villgids):

    if ALL_DEPT_ID in deptids:
        deps = set()
        [deps.add(complaint.department) for complaint in ComplaintType.objects.all()]
        depts = list(deps)
        #depts = ComplaintDepartment.objects.all ()
    else:
        depts = ComplaintDepartment.objects.filter (id__in = deptids)

    states = State.objects.filter (id__in = stateids)
    distts = District.objects.filter (id__in = disttids)
    blocks = Block.objects.filter (id__in = blockids)
    gramps = GramPanchayat.objects.filter (id__in = grampids)
    villgs = Village.objects.filter (id__in = villgids)

    if states.count () != 0:
        blocks = blocks | Block.objects.filter (district__state__id__in = [state.id for state in states])

    if distts.count () != 0:
        blocks = blocks | Block.objects.filter (district__id__in = [distt.id for distt in distts])

    stats = {'stdate_show' : stdate.strftime ("%d %B, %Y"),
             'endate_show' : endate.strftime ("%d %B, %Y"),
             'stdate' : stdate.strftime ("%d/%m/%Y"),
             'endate' : endate.strftime ("%d/%m/%Y"),
             'deptids' : ",".join ([str (x) for x in deptids]),
             'stateids' : ",".join ([str (x) for x in stateids]),
             'disttids' : ",".join ([str (x) for x in disttids]),
             'blockids' : ",".join ([str (x) for x in blockids]),
             'grampids' : ",".join ([str (x) for x in grampids]),
             'villgids' : ",".join ([str (x) for x in villgids]),
             'depts' : depts,
             'blocks' : blocks,
             'gramps' : gramps,
             'villgs' : villgs}
    # Find all villages in the selected locations for the report
    dttm_start = datetime (stdate.year, stdate.month, stdate.day, 0, 0, 0)
    dttm_end   = datetime (endate.year, endate.month, endate.day, 23, 59, 59)
    complaints = Complaint.objects.filter (Q (created__gte = dttm_start)
                                           & Q (created__lte = dttm_end)
                                           & Q (department__in = [dept.id for dept in depts])
                                           & (Q (location__in = villgids)
                                              | Q (location__grampanchayat__id__in = grampids)
                                              | Q (location__grampanchayat__block__id__in = blockids)
                                              | Q (location__grampanchayat__block__district__id__in = disttids)
                                              | Q (location__grampanchayat__block__district__state__id__in = stateids))
                                           )
    new_complaints = complaints.filter (curstate = STATUS_NEW).values_list('complaintno',flat=True).distinct()
    ack_complaints = complaints.filter (curstate = STATUS_ACK).values_list('complaintno',flat=True).distinct()
    ope_complaints = complaints.filter (curstate = STATUS_OPEN).values_list('complaintno',flat=True).distinct()
    res_complaints = complaints.filter (curstate = STATUS_RESOLVED).values_list('complaintno',flat=True).distinct()
    res_complaints_obj = complaints.filter (curstate = STATUS_RESOLVED)
    clo_complaints = complaints.filter (curstate = STATUS_CLOSED).values_list('complaintno', flat=True).distinct()
    reo_complaints = complaints.filter (curstate = STATUS_REOPEN).values_list('complaintno', flat=True).distinct()
    pen_complaints = res_complaints_obj.exclude (complaintno__in = clo_complaints).exclude(complaintno__in = reo_complaints).values_list('complaintno', flat=True).distinct()

    all_complaint_stats = {'new' : new_complaints.count(),
                           'ack' : ack_complaints.count(),
                           'ope' : ope_complaints.count(),
                           'res' : res_complaints.count(),
                           'clo' : clo_complaints.count(),
                           'reo' : reo_complaints.count(),
                           'pen' : pen_complaints.count()}

    new_ack_complaints = complaints.filter (curstate = STATUS_ACK, complaintno__in = new_complaints).values_list('complaintno', flat=True).distinct()
    new_ack_complaints_obj = complaints.filter (curstate = STATUS_ACK, complaintno__in = new_complaints)
    new_ope_complaints = complaints.filter (curstate = STATUS_OPEN, complaintno__in = new_complaints).values_list('complaintno', flat=True).distinct()
    new_res_complaints = complaints.filter (curstate = STATUS_RESOLVED, complaintno__in = new_complaints).values_list('complaintno', flat=True).distinct()
    new_res_complaints_obj = complaints.filter (curstate = STATUS_RESOLVED, complaintno__in = new_complaints)
    new_clo_complaints = complaints.filter (curstate = STATUS_CLOSED, complaintno__in = new_complaints).values_list('complaintno', flat=True).distinct()
    new_reo_complaints = complaints.filter (curstate = STATUS_REOPEN, complaintno__in = new_complaints).values_list('complaintno', flat=True).distinct()
    new_pen_complaints = new_res_complaints_obj.exclude (complaintno__in = new_clo_complaints).exclude(complaintno__in = new_reo_complaints).values_list('complaintno', flat=True).distinct()

    new_complaint_stats = {'new' : new_complaints.count(),
                           'ack' : new_ack_complaints.count(),
                           'ope' : new_ope_complaints.count(),
                           'res' : new_res_complaints.count(),
                           'clo' : new_clo_complaints.count(),
                           'reo' : new_reo_complaints.count(),
                           'pen' : new_pen_complaints.count()}

    stats ['all_complaints'] = all_complaint_stats
    stats ['new_complaints'] = new_complaint_stats

    # RESPONSE VOLUME METRICS
    def get_grouped_data (dataset):
        retdata = {}
        dataset = itertools.groupby (sorted (dataset, key = lambda x: x ['department__id']), key = lambda x : x ['department__id'])
        for deptid, schemedataset in dataset:
            retdata [deptid] = dict ([schemedata ['complainttype__cclass'], schemedata ['count']] for schemedata in schemedataset)

        for dept in depts:
            if retdata.has_key (dept.id) == False:
                retdata [dept.id] = {}

            for ctype in dept.complainttype_set.all ():
                if retdata [dept.id].has_key (ctype.cclass) == False:
                    retdata [dept.id][ctype.cclass] = 0

        return retdata

    ack_grouped = ack_complaints.values ('department__id', 'complainttype__cclass').annotate (count = Count ('complainttype__cclass'))
    clo_grouped = clo_complaints.values ('department__id', 'complainttype__cclass').annotate (count = Count ('complainttype__cclass'))

    ack_grouped = get_grouped_data (ack_grouped)
    clo_grouped = get_grouped_data (clo_grouped)

    volume_stats = {}
    for dept in depts:
        schemes = set ([ct.cclass for ct in dept.complainttype_set.all ()])
        volume_stats [dept.id]= {'schemes' : schemes,
                                 'dpoints' : [[ack_grouped [dept.id][s] for s in schemes],
                                              [clo_grouped [dept.id][s] for s in schemes]]}

    stats ['volume'] = volume_stats

    # RESPONSE TIME METRICS
    now_time = datetime.now ()

    def get_scheme_times (scheme,dept):
        new_scheme_complaints = new_ack_complaints_obj.filter (complainttype__cclass = scheme,department = dept).values_list('complaintno',flat=True).distinct()
        scheme_ccms = ComplaintClosureMetric.objects.filter (complaintno__in = new_scheme_complaints)

        scheme_stats = scheme_ccms.exclude (period = None)
        scheme_ccms_open = scheme_ccms.filter (closed = None).order_by ('created')

        retdata  = {}
        if scheme_ccms_open.count () != 0:
            max_open = timedelta_to_days (now_time - scheme_ccms_open[0].created)
        else:
            max_open = 0

        if scheme_stats.count () != 0:
            scheme_stats = scheme_stats.aggregate (maxper = Max ('period'), avgper = Avg ('period'))
            scheme_max = scheme_stats ['maxper']
            scheme_avg = scheme_stats ['avgper']
        else:
            scheme_max = 0
            scheme_avg = 0

        if max_open > scheme_max:
            scheme_max = max_open

        return {'max' : scheme_max, 'avg' : scheme_avg}

    time_stats = {}
    for dept in depts:
        schemes = set ([ct.cclass for ct in dept.complainttype_set.all ()])
        scheme_times = dict([(s, get_scheme_times (s,dept)) for s in schemes])

        time_stats [dept.id] = {'schemes' : schemes,
                                'dpoints' : [[scheme_times [s]['max'] for s in schemes],
                                             [scheme_times [s]['avg'] for s in schemes]]}

    stats ['time'] = time_stats

    # MOST FILED COMPLAINTS
    most_filed = new_complaints.values ('complainttype__summary', 'department__name', 'complainttype__cclass').annotate (count = Count ('complainttype__cclass'))

    stats ['most_filed'] = [{'summary' : mf ['complainttype__summary'],
                             'num_complaints' : mf ['count'],
                             'department_name' : mf ['department__name'],
                             'cclass' : mf ['complainttype__cclass']}
                            for mf in (sorted (most_filed,
                                               key = lambda x : x ['count'],
                                               reverse = True))[:5]]

    # LONGEST PENDING COMPLAINTS
    longest_pending = Complaint.objects.filter (complaintno__in = new_complaints, latest = True)
    longest_pending = longest_pending.exclude (curstate = STATUS_RESOLVED).exclude (curstate = STATUS_CLOSED).order_by ('created')

    stats ['longest_pending'] = longest_pending [:5]


    # MDG Graph
    stats ['mdgs'] = [[new_complaints.filter (complainttype__complaintmdg__mdg__goalnum = x).count ()] for x in range (1, 8)]

    return stats


def initial_report (request):
    form  = ReportForm (request.POST)

    if form.is_valid ():
        try:
            stdate  = form.cleaned_data ['stdate']
            endate  = form.cleaned_data ['endate']
            deptids = form.cleaned_data ['deptids']
            stateids = form.cleaned_data ['stateids']
            disttids = form.cleaned_data ['disttids']
            blockids = form.cleaned_data ['blockids']
            grampids = form.cleaned_data ['grampids']
            villgids = form.cleaned_data ['villgids']
            mdgindicators = form.cleaned_data ['mdgindicators']
            suggestions   = form.cleaned_data ['suggestions']

            stats = get_report_stats (stdate, endate,
                                      deptids,
                                      stateids,
                                      disttids,
                                      blockids,
                                      grampids,
                                      villgids)

            if 'final' in request.POST:
                final = True
            else:
                final = False

            return render_to_response ('report.html', {'stats' : stats,
                                                       'final' : final,
                                                       'mdgindicators' : mdgindicators,
                                                       'suggestions'   : suggestions})
        except:
            import traceback
            traceback.print_exc ()
    else:
        return HttpResponseRedirect ("/")


def edit_report (request):
    form  = ReportForm (request.POST)
    if form.is_valid ():
        all_depts = ComplaintDepartment.objects.all ()
        if ALL_DEPT_ID in form.cleaned_data ['deptids']:
            deptids = [dept.id for dept in all_depts]
        else:
            deptids = form.cleaned_data ['deptids']

        repform = Report (form.cleaned_data ['stdate'],
                          form.cleaned_data ['endate'],
                          deptids,
                          form.cleaned_data ['blockids'])

        return render_to_response ('reportselection.html', {'form' : repform,
                                                            'stdate' : form.cleaned_data ['stdate'],
                                                            'endate' : form.cleaned_data ['endate'],
                                                            'avldepts' : all_depts.exclude (id__in = deptids),
                                                            'seldepts' : all_depts.filter (id__in = deptids),
                                                            'avlblocks' : Block.objects.exclude (id__in = form.cleaned_data ['blockids']),
                                                            'selblocks' : Block.objects.filter (id__in = form.cleaned_data ['blockids']),
                                                            'gramps' : GramPanchayat.objects.filter (id__in = form.cleaned_data ['grampids']),
                                                            'villgs' : Village.objects.filter (id__in = form.cleaned_data ['villgids']),
                                                            'user' : request.user,
                                                            'menus' : get_user_menus (request.user, edit_report)})



def report(request) :
    if request.method=="POST":
        if 'edit' in request.POST:
            repdata = ReportData.objects.get (id = request.POST ['repdataid'])
            form = Report (repdata)

            return render_to_response('reportselection.html',
                                      {'form':form,
                                       'menus' : get_user_menus (request.user, report),
                                       'user' : request.user,
                                       'repdata' : repdata})

        elif 'final_report' in request.POST:
            repdata = ReportData.objects.get (id = request.POST ['repdataid'])
            stats = get_report_stats (repdata)
            stats['keypts']     = request.POST ['keypoints']
            stats['successtry'] = request.POST ['sucess_story']
            return render_to_response ('report.html', {'stats'      : stats,
                                                       'flag'       : True,
                                                       'staticdata' : repdata})
        elif 'removebutt' in request.POST:
            repdata = ReportData.objects.get (id = request.POST ['repdataid'])
            if "blk" in request.POST:
                idval = request.POST['blk']
                newdata = repdata.block.get(id = idval)
                repdata.block.remove(newdata)
            elif "gp" in request.POST:
                idval = request.POST['gp']
                newdata = repdata.gp.get(id = idval)
                repdata.gp.remove(newdata)
            elif "vill" in request.POST:
                idval = request.POST['vill']
                newdata = repdata.village.get(id = idval)
                repdata.village.remove(newdata)
            repdata.save()
            return render_to_response('reportselection.html',
                                      {'form'      : Report(repdata),
                                       'menus'     : get_user_menus (request.user,report),
                                       'user'      : request.user,
                                       'repdata'   : repdata})
    else:
        raise Http404


def storedata(request, repdataid, identifier, codea, codeb, codec):
    repdata = ReportData.objects.get (id = repdataid)
    if identifier == "DEP":
        depobj = ComplaintDepartment.objects.get(id = codea)
        repdata.department.add (depobj)
    elif identifier == "BLK":
        blkobj = Block.objects.get(id = codea)
        repdata.block.add (blkobj)
    elif identifier == "GP":
        gpobj  = GramPanchayat.objects.get(id = codeb)
        repdata.gp.add (gpobj)
    elif identifier == "VILL":
        villobj = Village.objects.get(id = codec)
        repdata.village.add (villobj)
    repdata.save()
    return HttpResponse()


def removedata(request, repdataid, identifier, codea, codeb, codec):
    repdata = ReportData.objects.get (id = repdataid)
    if identifier == "DEP":
        newdata = repdata.department.get(id = codea)
        repdata.department.remove(newdata)
        repdata.save()
    return HttpResponse()

def data(request, repdataid, cat, idval):
    repdata = ReportData.objects.get (id = repdataid)
    if cat == "blk":
        newdata = repdata.block.get(id = idval)
        repdata.block.remove(newdata)
    elif cat == "gp":
        newdata = repdata.gp.get(id = idval)
        repdata.gp.remove(newdata)
    elif cat == "vill":
        newdata = repdata.village.get(id = idval)
        repdata.village.remove(newdata)
    repdata.save()
    return HttpResponse()

from django.views.static import serve as serve_static_file

@login_required
def get_evidence (request, filename):
    role = AppRole.objects.get_user_role (request.user)
    if role == UserRoles.ROLE_CSO or role == UserRoles.ROLE_DM or role == UserRoles.ROLE_OFFICIAL:
        return serve_static_file (request,
                                  filename,
                                  document_root = settings.EVIDENCE_DIR,
                                  show_indexes = False)
    else:
        return render_to_response ('error.html',
                                   {'error' : _('Unauthorized access to evidence. Will be reported'),
                                    'menus' : get_user_menus (request.user,track_issues),
                                    'user' : request.user})
from cmh.reports.report_issues import create_or_update_idr

def _handle_evidence_upload (complaint, temp_file):
    ufname = temp_file.name
    ufunique = "%s_%d_%s" % (complaint.complaintno, complaint.id, ufname)
    ufpath = os.path.join (settings.EVIDENCE_DIR, ufunique)
    destfile = open (ufpath, 'wb+')
    for chunk in temp_file:
        destfile.write (chunk)
    destfile.close ()

    ce = ComplaintEvidence.objects.create (evfile = ufpath,
                                           filename = ufname,
                                           url = get_evidence_url (ufunique))
    complaint.evidences.add (ce)

    complaint.save ()
    # preferably done through signals for modularity
    create_or_update_idr(complaint)

@login_required
def set_reminder (request, complaintno):
    if request.method == 'POST':
        complaint = Complaint.objects.get (complaintno = complaintno, latest=True)
        form = SetComplaintReminder (complaint, request.POST)
        if form.is_valid ():
            try:
                cr = ComplaintReminder.objects.get (user = request.user,
                                                    complaintno = complaint.complaintno)
                cr.reminderon  = form.cleaned_data ['reminderon']
                cr.save ()
            except ComplaintReminder.DoesNotExist:
                cr = ComplaintReminder.objects.create (user = request.user,
                                                       complaintno = complaint.complaintno,
                                                       reminderon = form.cleaned_data ['reminderon'])
            except ComplaintReminder.MultipleObjectsReturned:
                ComplaintReminder.objects.filter (user = request.user,
                                                  copmlaintno = complaint.complaintno).delete ()
                cr = ComplaintReminder.objects.create (user = request.user,
                                                       complaintno = complaint.complaintno,
                                                       reminderon = form.cleaned_data ['reminderon'])

        return HttpResponseRedirect (reverse (track_issues, args = [complaint.complaintno]))
    else:
        return HttpResponseRedirect ("/")

@login_required
def del_reminder (request, complaintno):
    ComplaintReminder.objects.filter (user = request.user, complaintno = complaintno).delete ()
    return HttpResponseRedirect (reverse (track_issues, args = [complaintno]))

def file_sms (request):
    return render_to_response ('file_sms.html')

def file_phone (request):
    return render_to_response ('file_phone.html')
