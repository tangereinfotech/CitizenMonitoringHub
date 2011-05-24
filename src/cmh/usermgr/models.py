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

from cmh.common.models import ComplaintDepartment, ComplaintType

class Citizen(models.Model):
    name   = models.CharField (max_length = 500, blank = True, null = True)
    mobile = models.CharField (max_length = 15, blank=True,null=True)

    def __unicode__(self):
        return "Citizen: " + self.name


class CmhUser (models.Model):
    user = models.OneToOneField (User)
    phone = models.CharField (max_length = 20, blank = True, null = True)

    def get_desc_name (self):
        return "%s <%s>" % (self.user.get_full_name (),
                              self.user.username)

    def get_role_name (self):
        role = AppRole.objects.get_user_role (self.user)
        if role == None:
            return ""
        else:
            return UserRoles.ROLE_MAP[role.role]

    def set_user_role (self, role):
        approle = {UserRoles.CSO: ROLE_CSO,
                   UserRoles.DELEGATE: ROLE_DELEGATE,
                   UserRoles.OFFICIAL: ROLE_OFFICIAL,
                   UserRoles.DM: ROLE_DM}[role]
        approle.users.add (self.user)
        approle.save ()

    def _get_phone_number (self):
        if self.phone == None: return ""
        else: return self.phone

    phone_number = property (_get_phone_number)


class RoleException (Exception):
    pass


class AppRoleManager (models.Manager):
    def get_user_role (self, user):
        if user.is_authenticated ():
            try:
                return AppRole.objects.get (users = user)
            except AppRole.MultipleObjectsReturned:
                raise RoleException ("Multiple Roles for user: " + user.username)
            except AppRole.DoesNotExist:
                ROLE_ANONYMOUS.users.add (user)
                return ROLE_ANONYMOUS
        else:
            return ROLE_ANONYMOUS

class AppRole (models.Model):
    role  = models.IntegerField ()
    name  = models.CharField (max_length = 50)
    users = models.ManyToManyField (User)

    objects = AppRoleManager ()

    def __unicode__ (self):
        return self.name


class MenuItem (models.Model):
    name   = models.CharField (max_length = 500)
    url    = models.CharField (max_length = 500)
    role   = models.ForeignKey (AppRole)
    serial = models.IntegerField ()

    class Meta:
        unique_together = (('role', 'serial', 'url'),)


class Official(models.Model):
    user        = models.OneToOneField (User)
    supervisor  = models.ForeignKey ('Official', blank=True, null=True)
    departments = models.ManyToManyField (ComplaintDepartment, blank = True, null = True)
    title       = models.CharField (max_length = 20, blank = True, null = True)
    designation = models.CharField (max_length = 200, blank = True, null = True)
    complainttypes = models.ManyToManyField (ComplaintType, blank = True, null = True)

    def __unicode__(self):
        return u'Official: ' + self.user.username


