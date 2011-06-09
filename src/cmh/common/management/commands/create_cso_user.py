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

from django.contrib.auth.models import User

from cmh.common.constants import UserRoles
from cmh.usermgr.models import CmhUser

class Command (NoArgsCommand):
    def handle (self, *args, **kwargs):
        try:
            u = User.objects.create (username = 'cso')
            u.set_password ('123')
            u.save ()
            cu = CmhUser.objects.create (user = u, phone = '9977001872')
            cu.set_user_role (UserRoles.CSO)
        except:
            pass
