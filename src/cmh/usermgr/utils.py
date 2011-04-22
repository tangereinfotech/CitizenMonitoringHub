# encoding: utf-8
#
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

from cmh.usermgr.models import MenuItem, AppRole
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
        return MenuItem.objects.filter (role = role).order_by ('serial')
    else:
        return MenuItem.objects.filter (role__role = UserRoles.ANONYMOUS).order_by ('serial')

cso_role       = AppRole.objects.get (role = UserRoles.CSO)
delegate_role  = AppRole.objects.get (role = UserRoles.DELEGATE)
official_role  = AppRole.objects.get (role = UserRoles.OFFICIAL)
dm_role        = AppRole.objects.get (role = UserRoles.DM)
anonymous_role = AppRole.objects.get (role = UserRoles.ANONYMOUS)

def get_user_role (user):
    if cso_role.users.filter (id = user.id).count () != 0:
        return cso_role
    elif delegate_role.users.filter (id = user.id).count () != 0:
        return delegate_role
    elif official_role.users.filter (id = user.id).count () != 0:
        return official_role
    elif dm_role.users.filter (id = user.id).count () != 0:
        return dm_role
    else:
        return anonymous_role
