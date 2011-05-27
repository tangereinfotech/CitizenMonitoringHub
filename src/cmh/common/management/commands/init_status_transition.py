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

from django.core.management.base import NoArgsCommand, CommandError
from cmh.common.models import StatusTransition
from cmh.common.models import AppRole, MenuItem

from cmh.usermgr.constants import UserRoles

from cmh.issuemgr.constants import *


class Command (NoArgsCommand):
    def handle (self, *args, **kwargs):
        self.populate_role_menus ()

    def populate_role_menus (self):
        anonymous = AppRole.objects.get (role = UserRoles.ANONYMOUS)
        cso = AppRole.objects.get (role = UserRoles.CSO)
        delegate = AppRole.objects.get (role = UserRoles.DELEGATE)
        official = AppRole.objects.get (role = UserRoles.OFFICIAL)
        dm = AppRole.objects.get (role = UserRoles.DM)

        anonymous_menu = [{'name' : 'Home', 'url' : '/'},
                          {'name' : 'Submit Issue', 'url' : '/complaint/'},
                          {'name' : 'Track Issue', 'url' : '/complaint/track/'},]

        cso_menu = [{'name' : 'Home', 'url' : '/'},
                    {'name' : 'My Issues', 'url' : '/complaint/my_issues/'},
                    {'name' : 'Accept', 'url' : '/complaint/accept/'},
                    {'name' : 'Track', 'url' : '/complaint/track/'},
                    {'name' : 'Masters', 'url' : '/masters/'},]

        delegate_menu = [{'name' : 'Home', 'url' : '/'},
                         {'name' : 'My Issues', 'url' : '/complaint/my_issues/'},
                         {'name' : 'Track', 'url' : '/complaint/track/'},]

        official_menu = [{'name' : 'Home', 'url' : '/'},
                         {'name' : 'My Issues', 'url' : '/complaint/my_issues/'},
                         {'name' : 'Track', 'url' : '/complaint/track/'},]

        dm_menu = [{'name' : 'Home', 'url' : '/'},
                   {'name' : 'My Issues', 'url' : '/complaint/my_issues/'},
                   {'name' : 'Track', 'url' : '/complaint/track/'},]

        self._ensure_menu (anonymous, anonymous_menu)
        self._ensure_menu (cso, cso_menu)
        self._ensure_menu (delegate, delegate_menu)
        self._ensure_menu (official, official_menu)
        self._ensure_menu (dm, dm_menu)

        self._populate_status_transitions (cso, delegate, official, dm, anonymous)

    def _ensure_menu (self, role, menus):
        serial = 1
        for md in menus:
            try:
                mi = MenuItem.objects.get (name = md ['name'], role = role)
                mi.url = md ['url']
                mi.serial = serial
                mi.save ()
            except MenuItem.DoesNotExist:
                mi = MenuItem.objects.create (name = md ['name'], url = md ['url'],
                                              serial = serial, role = role)
            serial += 1

    def _populate_status_transitions (self, cso, delegate, official, dm, anonymous):
        matrix = [{'role' : cso,
                   'trans' : [{'cur' : STATUS_NEW,
                               'new' : [STATUS_ACK]},
                              {'cur' : STATUS_ACK,
                               'new' : [STATUS_OPEN, STATUS_RESOLVED]},
                              {'cur' : STATUS_OPEN,
                               'new' : [STATUS_RESOLVED]},
                              {'cur' : STATUS_RESOLVED,
                               'new' : [STATUS_REOPEN, STATUS_CLOSED]},
                              {'cur' : STATUS_REOPEN,
                               'new' : [STATUS_ACK, STATUS_RESOLVED]}]},
                  {'role' : delegate,
                   'trans' : [{'cur' : STATUS_OPEN,
                               'new' : [STATUS_RESOLVED]}]},
                  {'role' : official,
                   'trans' : [{'cur' : STATUS_OPEN,
                               'new' : [STATUS_RESOLVED]}]},
                  {'role' : dm,
                   'trans' : [{'cur' : STATUS_OPEN,
                               'new' : [STATUS_RESOLVED]}]},
                  {'role' : anonymous,
                   'trans' : [{'cur' : STATUS_RESOLVED,
                               'new' : [STATUS_REOPEN, STATUS_CLOSED]}]}]

        for rt in matrix:
            print "Processing transitions for: " + rt ['role'].name
            for trans in rt ['trans']:
                for newstate in trans ['new']:
                    try:
                        cur = StatusTransition.objects.get (role = rt ['role'],
                                                            curstate = trans ['cur'],
                                                            newstate = newstate)
                    except StatusTransition.DoesNotExist:
                        cur = StatusTransition.objects.create (role = rt ['role'],
                                                               curstate = trans ['cur'],
                                                               newstate = newstate)

