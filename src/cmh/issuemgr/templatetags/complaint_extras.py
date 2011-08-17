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

from django import template
from datetime import datetime

from cmh.common.models import AppRole
from cmh.common.models import StatusTransition

from cmh.common.constants import UserRoles

from cmh.issuemgr.constants import STATUS_NEW, STATUS_ACK

from cmh.issuemgr.models import Complaint, ComplaintReminder

register = template.Library ()

@register.filter
def is_updatable (complaint, user):
    role = AppRole.objects.get_user_role (user)
    if StatusTransition.objects.get_allowed_statuses (role, complaint.curstate).count () == 0:
        return False
    else:
        return True

@register.filter
def get_evidence_display (evidence, user):
    role = AppRole.objects.get_user_role (user)
    if role == UserRoles.ROLE_CSO or role == UserRoles.ROLE_DM:
        retstr  = ('<a href="' + evidence.url + '" target="_blank">'
                   + evidence.filename + '</a>')
    else:
        retstr = evidence.filename
    return retstr

@register.filter
def can_add_evidence (complaint, user):
    if complaint.curstate == STATUS_NEW or complaint.curstate == STATUS_ACK:
        role = AppRole.objects.get_user_role (user)
        if role == UserRoles.ROLE_CSO or role == UserRoles.ROLE_DM:
            return True
    return False

@register.filter
def can_set_reminder (complaintno, user):
    if ComplaintReminder.objects.filter (user = user, complaintno = complaintno).count () != 0:
        return False
    return True

@register.filter
def can_del_reminder (complaintno, user):
    if ComplaintReminder.objects.filter (user = user, complaintno = complaintno).count () != 0:
        return True
    return False

@register.filter
def get_reminder (complaintno, user):
    try:
        cr = ComplaintReminder.objects.get (user = user, complaintno = complaintno)
        return cr.reminderon
    except:
        return "No Reminder"

@register.filter
def description_with_reminder (complaint, user):
    description = complaint.description
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        description = "<span style='color:#ff3333;font-style:italic'>" + description + " </span>"
    return description

@register.filter
def get_mdgs (comptype):
    return ", ".join (sorted ([m.mdg.goalnum for m in comptype.complaintmdg_set.all ()]))


@register.filter
def complaintno_with_reminder (complaint, user):
    retval = complaint.complaintno
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        retval = "<span style='color:#ff3333;font-style:italic'>" + retval + "</span>"
    return retval

@register.filter
def logdate_with_reminder (complaint, user):
    retval = complaint.logdate.strftime ("%b %d, %Y")
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        retval = "<span style='color:#ff3333;font-style:italic'>" + retval + "</span>"
    return retval

@register.filter
def curstate_with_reminder (complaint, user):
    retval = str (complaint.curstate)
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        retval = "<span style='color:#ff3333;font-style:italic'>" + retval + "</span>"
    return retval

@register.filter
def created_with_reminder (complaint, user):
    retval = complaint.created.strftime ("%b %d, %Y, %I:%M %p")
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        retval = "<span style='color:#ff3333;font-style:italic'>" + retval + "</span>"
    return retval

@register.filter
def get_scheme_datasets (dataset, deptid):
    return zip (dataset [deptid]['schemes'], dataset [deptid]['dpoints'])

@register.filter
def get_schemes (dataset, deptid):
    return dataset [deptid]['schemes']

@register.filter
def get_schemes_data (dataset, deptid):
    return dataset [deptid]['dpoints']

