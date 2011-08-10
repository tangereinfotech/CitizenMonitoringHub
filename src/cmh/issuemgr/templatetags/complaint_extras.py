from django import template
from datetime import datetime

from cmh.common.models import AppRole
from cmh.common.models import StatusTransition

from cmh.common.constants import UserRoles

from cmh.issuemgr.constants import STATUS_NEW, STATUS_ACK

from cmh.issuemgr.models import Complaint, ComplaintReminder

register = template.Library ()

def is_updatable (complaint, user):
    role = AppRole.objects.get_user_role (user)
    if StatusTransition.objects.get_allowed_statuses (role, complaint.curstate).count () == 0:
        return False
    else:
        return True

def get_evidence_display (evidence, user):
    role = AppRole.objects.get_user_role (user)
    if role == UserRoles.ROLE_CSO or role == UserRoles.ROLE_DM:
        retstr  = ('<a href="' + evidence.url + '" target="_blank">'
                   + evidence.filename + '</a>')
    else:
        retstr = evidence.filename
    return retstr

def can_add_evidence (complaint, user):
    if complaint.curstate == STATUS_NEW or complaint.curstate == STATUS_ACK:
        role = AppRole.objects.get_user_role (user)
        if role == UserRoles.ROLE_CSO or role == UserRoles.ROLE_DM:
            return True
    return False

def can_set_reminder (complaintno, user):
    if ComplaintReminder.objects.filter (user = user, complaintno = complaintno).count () != 0:
        return False
    return True

def can_del_reminder (complaintno, user):
    if ComplaintReminder.objects.filter (user = user, complaintno = complaintno).count () != 0:
        return True
    return False

def get_reminder (complaintno, user):
    try:
        cr = ComplaintReminder.objects.get (user = user, complaintno = complaintno)
        return cr.reminderon
    except:
        return "No Reminder"

def description_with_reminder (complaint, user):
    description = complaint.description
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        description = "<span style='color:#ff3333;font-style:italic'>" + description + " </span>"
    return description

def get_mdgs (comptype):
    return ", ".join (sorted ([m.goalnum for m in comptype.complaintmdg_set.all ()]))


def complaintno_with_reminder (complaint, user):
    retval = complaint.complaintno
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        retval = "<span style='color:#ff3333;font-style:italic'>" + retval + "</span>"
    return retval

def logdate_with_reminder (complaint, user):
    retval = complaint.logdate.strftime ("%b %d, %Y")
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        retval = "<span style='color:#ff3333;font-style:italic'>" + retval + "</span>"
    return retval

def curstate_with_reminder (complaint, user):
    retval = str (complaint.curstate)
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        retval = "<span style='color:#ff3333;font-style:italic'>" + retval + "</span>"
    return retval

def created_with_reminder (complaint, user):
    retval = complaint.created.strftime ("%b %d, %Y, %I:%M %p")
    crs = ComplaintReminder.objects.filter (user = user,
                                            complaintno = complaint.complaintno,
                                            reminderon__lte = datetime.today ().date ()).order_by ('reminderon')
    if crs.count () != 0:
        retval = "<span style='color:#ff3333;font-style:italic'>" + retval + "</span>"
    return retval


register.filter ('is_updatable', is_updatable)
register.filter ('get_evidence_display', get_evidence_display)
register.filter ('can_add_evidence', can_add_evidence)
register.filter ('can_set_reminder', can_set_reminder)
register.filter ('can_del_reminder', can_del_reminder)
register.filter ('get_reminder', get_reminder)
register.filter ('description_with_reminder', description_with_reminder)
register.filter ('get_mdgs', get_mdgs)
register.filter ('complaintno_with_reminder', complaintno_with_reminder)
register.filter ('logdate_with_reminder',     logdate_with_reminder)
register.filter ('curstate_with_reminder',    curstate_with_reminder)
register.filter ('created_with_reminder',     created_with_reminder)

