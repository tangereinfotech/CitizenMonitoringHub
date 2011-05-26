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
            AppRole.objects.get (role = UserRoles.ANONYMOUS)
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.ANONYMOUS)
        try:
            AppRole.objects.get (role = UserRoles.CSO)
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.CSO)
        try:
            AppRole.objects.get (role = UserRoles.DELEGATE)
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.DELEGATE)
        try:
            AppRole.objects.get (role = UserRoles.OFFICIAL)
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.OFFICIAL)
        try:
            AppRole.objects.get (role = UserRoles.DM)
        except AppRole.DoesNotExist:
            AppRole.objects.create (role = UserRoles.DM)


