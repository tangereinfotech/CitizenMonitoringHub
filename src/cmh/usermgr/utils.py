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

from django.core.urlresolvers import reverse
from cmh.common.models import MenuItem, AppRole
from cmh.usermgr.constants import UserRoles

from cmh.usermgr.models import Citizen

def get_or_create_citizen (mobile, name):
    try:
        citizen = Citizen.objects.get (mobile = mobile)
    except Citizen.DoesNotExist:
        citizen = Citizen.objects.create (mobile = mobile, name = name)

    return citizen

def get_user_menus (user, fnname):
    if user.is_authenticated ():
        role = AppRole.objects.get_user_role (user)
    else:
        role = UserRoles.ANONYMOUS

    menus = MenuItem.objects.filter (role = role).order_by ('serial')

    url  = reverse (fnname)
    try:
        selmenuitem = MenuItem.objects.get (role = role, url = url)
    except MenuItem.DoesNotExist:
        selmenuitem = None

    retmenus = []
    for mi in menus:
        if selmenuitem != None:
            retmenus.append({'url' : mi.url,
                             'name' : mi.name,
                             'class' : ('ui-tabs-selected ui-state-active'
                                        if mi.id == selmenuitem.id else '')})
        else:
            retmenus.append({'url' : mi.url,
                             'name' : mi.name,
                             'class' : ''})

    return retmenus



