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

