# encoding: utf-8
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

from django.core.management.base import NoArgsCommand

from cmh.common.models import AppRole

from cmh.usermgr.constants import UserRoles


class Command (NoArgsCommand):
    def handle (self, *args, **kwargs):
        try:
            AppRole.objects.get (role = UserRoles.ANONYMOUS, name = "Anonymous")
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.ANONYMOUS, name = "Anonymous")
        try:
            AppRole.objects.get (role = UserRoles.CSO, name = "CSO Member")
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.CSO, name = "CSO Member")
        try:
            AppRole.objects.get (role = UserRoles.DELEGATE, name = "Delegate")
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.DELEGATE, name = "Delegate")
        try:
            AppRole.objects.get (role = UserRoles.OFFICIAL, name = 'Official')
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.OFFICIAL, name = 'Official')
        try:
            AppRole.objects.get (role = UserRoles.DM, name = 'District Magistrate')
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.DM, name = 'District Magistrate')


