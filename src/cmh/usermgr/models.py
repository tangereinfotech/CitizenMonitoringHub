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

import sys, traceback
from django.db import models
from django.contrib.auth.models import User

from cmh.common.models import ComplaintDepartment, ComplaintType, AppRole
from cmh.common.utils import get_random_string

class Citizen(models.Model):
    name   = models.CharField (max_length = 500, blank = True, null = True)
    mobile = models.CharField (max_length = 15, blank=True,null=True)

    def __unicode__(self):
        return "Citizen: " + self.name


class CmhUser (models.Model):
    user = models.OneToOneField (User)
    phone = models.CharField (max_length = 20, blank = True, null = True)

    def get_desc_name (self):
        return "%s <%s>" % (self.user.get_full_name (), self.user.username)

    def __unicode__ (self):
        return self.get_desc_name ()

    def get_role_name (self):
        from cmh.common.constants import UserRoles

        role = AppRole.objects.get_user_role (self.user)
        if role == None:
            return ""
        else:
            return UserRoles.ROLE_MAP[role.role]

    def set_user_role (self, role):
        from cmh.common.constants import UserRoles

        approle = {UserRoles.CSO: UserRoles.ROLE_CSO,
                   UserRoles.DELEGATE: UserRoles.ROLE_DELEGATE,
                   UserRoles.OFFICIAL: UserRoles.ROLE_OFFICIAL,
                   UserRoles.DM: UserRoles.ROLE_DM}[role]
        approle.users.add (self.user)
        approle.save ()

    def get_user_role (self):
        return AppRole.objects.get_user_role (self.user)

    def _get_phone_number (self):
        if self.phone == None: return ""
        else: return self.phone

    def reset_password (self):
        from cmh.common.constants import PASSWORD_LEN, PASSWORD_MSG

        password = get_random_string (PASSWORD_LEN)
        message = PASSWORD_MSG % (cmhuser.phone, password)
        debug (message)
        TextMessage.objects.queue_text_message (cmhuser.phone, message)

    phone_number = property (_get_phone_number)

    def _get_department_name (self):
        from cmh.common.constants import UserRoles

        if self.get_user_role () in [UserRoles.ROLE_OFFICIAL, UserRoles.ROLE_DELEGATE]:
            return self.user.official.department.name
        else:
            return ""

    department_name = property (_get_department_name)

    def _get_department (self):
        from cmh.common.constants import UserRoles

        if self.get_user_role () in [UserRoles.ROLE_OFFICIAL, UserRoles.ROLE_DELEGATE]:
            return self.user.official.department
        else:
            return None

    department = property (_get_department)

    def _get_supervisor (self):
        from cmh.common.constants import UserRoles

        if self.get_user_role () in [UserRoles.ROLE_OFFICIAL, UserRoles.ROLE_DELEGATE]:
            return self.user.official.supervisor
        else:
            return ""

    supervisor_names = property (_get_supervisor)


class Official(models.Model):
    user        = models.OneToOneField (User)
    supervisor  = models.ForeignKey ('Official', blank=True, null=True)
    title       = models.CharField (max_length = 20, blank = True, null = True)
    designation = models.CharField (max_length = 200, blank = True, null = True)
    complainttypes = models.ManyToManyField (ComplaintType, blank = True, null = True)
    department  = models.ForeignKey (ComplaintDepartment, blank = True, null = True)

    class Meta:
        unique_together = (("supervisor", "department"),)

    def __unicode__(self):
        return u'Official: ' + self.user.username

