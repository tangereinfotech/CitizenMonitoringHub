from django import template

from cmh.common.models import AppRole
from cmh.common.models import StatusTransition

register = template.Library ()

def is_updatable (complaint, user):
    role = AppRole.objects.get_user_role (user)
    if StatusTransition.objects.get_allowed_statuses (role, complaint.curstate).count () == 0:
        return False
    else:
        return True

register.filter ('is_updatable', is_updatable)
