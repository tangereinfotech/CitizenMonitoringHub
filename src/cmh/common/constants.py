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

from cmh.common.models import AppRole
from cmh.common.models import District

PASSWORD_LEN = 6
PASSWORD_MSG = "Username: %s ; Password: %s"

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

    try:
        ROLE_ANONYMOUS = AppRole.objects.get (role = ANONYMOUS)
    except AppRole.DoesNotExist:
        ROLE_ANONYMOUS = None

    try:
        ROLE_CSO = AppRole.objects.get (role = CSO)
    except AppRole.DoesNotExist:
        ROLE_CSO = None

    try:
        ROLE_DELEGATE = AppRole.objects.get (role = DELEGATE)
    except AppRole.DoesNotExist:
        ROLE_DELEGATE = None

    try:
        ROLE_OFFICIAL = AppRole.objects.get (role = OFFICIAL)
    except AppRole.DoesNotExist:
        ROLE_OFFICIAL = None

    try:
        ROLE_DM = AppRole.objects.get (role = DM)
    except AppRole.DoesNotExist:
        ROLE_DM = None


class DeployDistrict:
    try:
        DISTRICT = District.objects.all ()[0]
    except:
        DISTRICT = None
