from django import template

from cmh.usermgr.models import AppRole
from cmh.issuemgr.models import StatusTransition

register = template.Library ()

def is_updatable (complaint, user):
    role = AppRole.objects.get_user_role (user)
    if StatusTransition.objects.get_allowed_statuses (role, complaint.curstate).count () == 0:
        return False
    else:
        return True

register.filter ('is_updatable', is_updatable)
