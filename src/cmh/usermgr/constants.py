from cmh.usermgr.models import AppRole

class UserRoles:
    ANONYMOUS = 1
    CSO       = 2
    DELEGATE  = 3
    OFFICIAL  = 4
    DM        = 5

    ROLE_MAP = {ANONYMOUS : "Anonymous",
                CSO : 'CMH Member',
                DELEGATE : 'Delegate',
                OFFICIAL : 'Official',
                DM : 'District Magistrate'}

    ROLE_ANONYMOUS = AppRole.objects.get (role = UserRoles.ANONYMOUS)
    ROLE_CSO       = AppRole.objects.get (role = UserRoles.CSO)
    ROLE_DELEGATE  = AppRole.objects.get (role = UserRoles.DELEGATE)
    ROLE_OFFICIAL  = AppRole.objects.get (role = UserRoles.OFFICIAL)
    ROLE_DM        = AppRole.objects.get (role = UserRoles.DM)

