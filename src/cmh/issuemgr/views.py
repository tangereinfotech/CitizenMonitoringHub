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
from cmh.issuemgr.forms import ComplaintTrackForm, LocationStatsForm, ReportForm
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

            # HACK ALERT - complaint type is not known so just pick any complaint type and pick its defsmsnew
            message = ComplaintType.objects.all ()[0].defsmsnew.replace ('____', complaint.complaintno)
            TextMessage.objects.queue_text_message (complaint.filedby.mobile, message)

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

        complaints = Complaint.objects.filter (latest = True, created__gte = dttm_start, created__lte = dttm_end)
        complaints = complaints.filter (Q (curstate = STATUS_NEW) | Q (curstate = STATUS_ACK) | Q (curstate = STATUS_REOPEN) | Q (curstate = STATUS_OPEN))

        if not ALL_DEPT_ID in deptids:
            complaints = complaints.filter (department__id__in = deptids)

        datalevel = form.cleaned_data ['datalevel']
        locid = form.cleaned_data ['locid']

        if datalevel == 'villg':
            loctype = "Village"
            location = Village.objects.get (id = locid)
            complaints = complaints.filter (location__id = locid)
            uptype = 'Gram Panchayat'
            upname = location.grampanchayat.name
        elif datalevel == 'gramp':
            loctype = "Gram Panchayat"
            location = GramPanchayat.objects.get (id = locid)
            complaints = complaints.filter (location__grampanchayat__id = locid)
            uptype = 'Block'
            upname = location.block.name
        elif datalevel == 'block':
            loctype = "Block"
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

        stats = {'count' : complaints.count (),
                 'name' : location.name,
                 'type' : loctype,
                 'departments' : dept_complaints,
                 'uptype' : uptype,
                 'upname' : upname}
        return render_to_response ('location_stats.html', {'stats' : stats})

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
    try:
        role = AppRole.objects.get_user_role (request.user)
        statuses = StatusTransition.objects.get_changeable_statuses (role)
        querySet = Complaint.objects.get_latest_complaints ().filter (curstate__in = statuses).order_by ('-created')

        role = request.user.cmhuser.get_user_role ()
        if role == UserRoles.ROLE_OFFICIAL or role == UserRoles.ROLE_DELEGATE:
            official = request.user.official
            querySet = querySet.filter (department = official.department)

        columnIndexNameMap = { 0: 'complaintno',
                               1: 'logdate',
                               2: 'description',
                               3: 'curstate',
                               4: 'created'}

        x = get_datatables_records (request, querySet, columnIndexNameMap, 'issue_entity_datatable.html')
    except:
        import traceback
        traceback.print_exc ()

    return x


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
    complaintno = complaintno.strip ()
    try:
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
    except Complaint.DoesNotExist:
        return render_to_response ('track_issues_not_found.html',
                                   {'menus' : get_user_menus (request.user,track_issues),
                                    'user' : request.user,
                                    'complaintno' : complaintno})
    except:
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

            data  = get_complaint_data (deptids, stdate, endate)

            return HttpResponse (json.dumps ({'datapoints' : data, 'names' : names, 'departments' : deptinfo}))
    except:
        import traceback
        traceback.print_exc ()
    return HttpResponse (json.dumps ({'datapoints' : [[]], 'names' : [], 'departments' : []}))

def get_complaint_data (deptids, stdate, endate):
    complaints = Complaint.objects.filter (createdate__lte = endate, latest = True, department__id__in = deptids)
    open_complaints = complaints.filter (Q (curstate = STATUS_NEW) | Q (curstate = STATUS_ACK) | Q (curstate = STATUS_REOPEN) | Q (curstate = STATUS_OPEN))
    clos_complaints = complaints.filter (Q (curstate = STATUS_RESOLVED) | Q (curstate = STATUS_CLOSED))

    open_data = open_complaints.filter (createdate__gt = stdate).values ('department__id', 'department__name', 'createdate').annotate (Count ('createdate'))
    clos_data = clos_complaints.filter (createdate__gt = stdate).values ('department__id', 'department__name', 'createdate').annotate (Count ('createdate'))

    ds = [d for d in daterange (stdate, endate)]
    depts = ComplaintDepartment.objects.filter (id__in = deptids).order_by ('id')

    composite_data = ([(od ['department__id'], od ['department__name'], od ['createdate'], od ['createdate__count']) for od in open_data]
                      + [(cd ['department__id'], cd ['department__name'], cd ['createdate'], - cd ['createdate__count']) for cd in clos_data])

    begn_open_data = open_complaints.filter (createdate__lte = stdate)
    begn_clos_data = clos_complaints.filter (createdate__lte = stdate)

    for dept in depts:
        composite_data.append ((dept.id,
                                dept.name,
                                stdate,
                                (begn_open_data.filter (department__id = dept.id).count () - begn_clos_data.filter (department__id = dept.id).count ())))

    composite_data = sorted (composite_data, key = (lambda x: x [0]))

    depts_data = group_by_departments (composite_data, ds)

    return depts_data


def group_by_departments (cdata, drange):
    curdeptid = cdata [0][0]
    deptdata = {curdeptid : [cdata [0]]}
    for cd in cdata [1:]:
        if cd [0] == curdeptid:
            deptdata [curdeptid].append (cd)
        else:
            curdeptid = cd [0]
            deptdata [curdeptid] = [cd]

    nd = []
    for did, cstats in deptdata.items ():
        nd.append (combine_dept_data (cstats, drange))

    return nd

def combine_dept_data (cstats, drange):
    cstats = sorted (cstats, key = (lambda x: x [2]))

    cstat = cstats [0]

    dinq = cstat [2] # Date In Question
    dinqdata = {dinq : cstat [3]}

    for cstat in cstats [1:]:
        if cstat [2] == dinq:
            dinqdata [dinq] += cstat [3]
        else:
            dinq = cstat [2]
            dinqdata [dinq] = cstat [3]

    dinqdata = sorted (dinqdata.items (), key = (lambda x: -x[1]))

    dcounter = 0

    curdate = drange [dcounter]
    dcounter += 1
    deptdata = []
    prevcount = 0
    for cstat_date, cstat_count in dinqdata:
        if curdate < cstat_date:
            while curdate < cstat_date:
                deptdata.append ([curdate.strftime ('%Y-%m-%d 1:00 AM'), prevcount])
                curdate = drange [dcounter]
                dcounter += 1
            prevcount += cstat_count
        elif curdate == cstat_date:
            prevcount += cstat_count
            deptdata.append ([curdate.strftime ('%Y-%m-%d 1:00 AM'), prevcount])
            curdate = drange [dcounter]
            dcounter += 1


    while curdate <= drange [-1]:
        deptdata.append ([curdate.strftime ('%Y-%m-%d 12:01 AM'), prevcount])
        curdate += timedelta (days = 1)

    return deptdata


from cmh.issuemgr.models import ReportData
SESSION_REPORT_ID = 'report-id'

def get_repdata_in_session (request):
    if SESSION_REPORT_ID in request.session:
        repdata = ReportData.objects.get (id = int (request.session [SESSION_REPORT_ID]))
    else:
        repdata = ReportData.objects.create ()
        request.session [SESSION_REPORT_ID] = str (repdata.id)

    print "repdata.id ", repdata.id

    return repdata
def reportgeneration (obj):
    #    print "in report generation", obj.strtdate, "   ", obj.enddate, "   ",  obj.department.all(), "   ",  obj.block.all()
    complaint = Complaint.objects.filter(department = obj.department



def report(request) :
    repdata = get_repdata_in_session (request)
    if request.method=="GET" :
        form = Report (repdata)
        return render_to_response('reportselection.html',
                                 {'form':form,
                                  'menus' : get_user_menus (request.user,report),
                                  'user' : request.user})
    elif request.method=="POST":
        postform = ReportForm(request.POST)
        print "validitiy", postform.is_valid()
        if postform.is_valid():
            repdata = get_repdata_in_session (request)
            repdata.strtdate = postform.cleaned_data['strtdate']
            repdata.enddate = postform.cleaned_data['enddate']
            repdata.save()
            finaldata = get_repdata_in_session (request)
            request.session.flush()
            reportgeneration(finaldata)
            return render_to_response('report.html',
                                      {'menus' : get_user_menus (request.user,report),
                                       'user' : request.user})
        else:
            return render_to_response('reportselection.html',
                                      {'form'      : Report(repdata),
                                       'errorpost' : postform,
                                       'menus'     : get_user_menus (request.user,report),
                                       'user'      : request.user})

def storedata(request, identifier, codea, codeb, codec):
    if identifier == "DEP":
        repdata            = get_repdata_in_session (request)
        depobj             = ComplaintDepartment.objects.get(id = codea)
        repdata.department.add (depobj)
        repdata.save()
        return HttpResponse()

    elif identifier == "BLK":
        repdata         = get_repdata_in_session (request)
        blkobj          = Block.objects.get(id = codea)
        repdata.block.add (blkobj)
        repdata.save()
        return HttpResponse()
    elif identifier == "GP":
        repdata         = get_repdata_in_session (request)
        blkobj          = Block.objects.get(id = codea)
        gpobj           = GramPanchayat.objects.get(id = codeb)

        repdata.block.add (blkobj)
        repdata.gp.add (gpobj)

        repdata.save()
        return HttpResponse()
    elif identifier == "VILL":
        repdata         = get_repdata_in_session (request)
        blkobj          = Block.objects.get(id = codea)
        gpobj           = GramPanchayat.objects.get(id = codeb)
        try:
            villobj         = Village.objects.get(id = codec)
            repdata.village.add (villobj)
        except Village.DoesNotExist:
            pass
        repdata.block.add (blkobj)
        repdata.gp.add (gpobj)
        repdata.save()
        return HttpResponse()

