from cmh.usermgr.models import MenuItem
from cmh.usermgr.constants import UserRoles

from cmh.usermgr.models import Citizen

def get_or_create_citizen (mobile, name):

    try:
        citizen = Citizen.objects.get (mobile = mobile)
    except Citizen.DoesNotExist:
        citizen = Citizen.objects.create (mobile = mobile, name = name)

    return citizen

def get_user_menus (user):
    if user.is_authenticated ():
        role = get_user_role (user)
        return MenuItem.objects.filter (role = role)
    else:
        return MenuItem.objects.filter (role = UserRoles.ANONYMOUS)

def get_user_role (user):
    return UserRoles.ANONYMOUS
