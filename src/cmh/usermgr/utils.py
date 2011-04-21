def get_or_create_citizen (mobile, name):
    from cmh.usermgr.models import Citizen

    try:
        citizen = Citizen.objects.get (mobile = mobile)
    except Citizen.DoesNotExist:
        citizen = Citizen.objects.create (mobile = mobile, name = name)

    return citizen

def get_user_menus (user):
    from cmh.usermgr.models import MenuItem
    from cmh.usermgr.constants import UserRoles
    if user.is_authenticated ():
        roles = get_user_roles (user)
        return MenusItem.objects.filter (role = role)
    else:
        return MenusItem.objects.filter (role = UserRoles.ANONYMOUS)

