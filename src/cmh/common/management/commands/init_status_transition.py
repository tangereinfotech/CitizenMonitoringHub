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
from cmh.common.models import Category, Attribute, LatLong, CodeName
from cmh.issuemgr.models import ComplaintItem, StatusTransition
from cmh.usermgr.constants import UserRoles
from cmh.usermgr.models import AppRole, MenuItem
from cmh.issuemgr.constants import *


class Command (NoArgsCommand):
    def handle (self, *args, **kwargs):
        self.populate_role_menus ()
        self.populate_complaint_status ()

    def populate_role_menus (self):
        try:
            anonymous = AppRole.objects.get (role = UserRoles.ANONYMOUS)
            anonymous.name = 'Anonymous'
            anonymous.save ()
        except AppRole.DoesNotExist:
            anonymous = AppRole.objects.create (role = UserRoles.ANONYMOUS, name = 'Anonymous')

        try:
            cso = AppRole.objects.get (role = UserRoles.CSO)
            cso.name = 'CSO Member'
            cso.save ()
        except AppRole.DoesNotExist:
            cso = AppRole.objects.create (role = UserRoles.CSO, name = 'CSO Member')

        try:
            delegate = AppRole.objects.get (role = UserRoles.DELEGATE)
            delegate.name = 'Delegate'
            delegate.save ()
        except AppRole.DoesNotExist:
            delegate = AppRole.objects.create (role = UserRoles.DELEGATE, name = 'Delegate')

        try:
            official = AppRole.objects.get (role = UserRoles.OFFICIAL)
            official.name = 'Official'
            official.save ()
        except AppRole.DoesNotExist:
            official = AppRole.objects.create (role = UserRoles.OFFICIAL, name = 'Official')

        try:
            dm = AppRole.objects.get (role = UserRoles.DM)
            dm.name = 'District Magistrate'
            dm.save ()
        except AppRole.DoesNotExist:
            dm = AppRole.objects.create (role = UserRoles.DM, name = 'District Magistrate')

        anonymous_menu = [{'name' : 'Home',
                           'url' : '/'},
                          {'name' : 'Submit Complaint',
                           'url' : '/complaint/'},
                          {'name' : 'Track Complaint',
                           'url' : '/complaint/track/'},
                          ]

        cso_menu = [{'name' : 'Home',
                     'url' : '/'},
                    {'name' : 'Accept',
                     'url' : '/complaint/accept/'},
                    {'name' : 'My Issues',
                     'url' : '/complaint/my_issues/'},
                    {'name' : 'Manage Masters',
                     'url' : '/masters/'},
                    ]

        self._ensure_menu (anonymous, anonymous_menu)
        self._ensure_menu (cso, cso_menu)
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

    def populate_complaint_status (self):
        try:
            cat_complaintstatus = Category.objects.get (key = 'Status')
        except Category.DoesNotExist:
            cat_complaintstatus = Category.objects.create (key = 'Status')

        statuses = ['New', 'Reopened', 'Acknowledged', 'Open', 'Resolved', 'Closed']
        for status in statuses:
            print "Checking/ Creating - " + status
            try:
                s = Attribute.objects.get (value = status, category = cat_complaintstatus)
            except Attribute.DoesNotExist:
                s = Attribute.objects.create (value = status, category = cat_complaintstatus)


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

