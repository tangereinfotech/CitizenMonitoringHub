from django import template

from cmh.common.models import AppRole
from cmh.common.models import StatusTransition

from cmh.common.constants import UserRoles

from cmh.issuemgr.constants import STATUS_NEW, STATUS_ACK

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

register.filter ('is_updatable', is_updatable)
register.filter ('get_evidence_display', get_evidence_display)
register.filter ('can_add_evidence', can_add_evidence)
