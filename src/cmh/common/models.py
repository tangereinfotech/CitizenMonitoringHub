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

from django.db import models
from django.contrib.auth.models import User

class Location (models.Model):
    code = models.CharField (max_length = 200)
    name = models.CharField (max_length = 2000)
    lattd = models.FloatField (blank = True, null = True)
    longd = models.FloatField (blank = True, null = True)

    class Meta:
        abstract = True

class Country (Location):
    pass

class State (Location):
    country = models.ForeignKey (Country)

class District (Location):
    state = models.ForeignKey (State)

class Block (Location):
    district = models.ForeignKey (District)

class GramPanchayat (Location):
    block = models.ForeignKey (Block)

class Village (Location):
    grampanchayat = models.ForeignKey (GramPanchayat)
    search = models.CharField (max_length = 5000)

class ComplaintDepartment (models.Model):
    code = models.CharField (max_length = 200)
    name = models.CharField (max_length = 5000)
    district = models.ForeignKey (District)

class ComplaintType (models.Model):
    code = models.CharField (max_length = 200)
    summary = models.CharField (max_length = 2000)
    department = models.ForeignKey (ComplaintDepartment)
    cclass = models.CharField (max_length = 500, blank = True, null = True)
    defsmsnew = models.CharField (max_length = 2000, blank = True, null = True)
    defsmsack = models.CharField (max_length = 2000, blank = True, null = True)
    defsmsopen = models.CharField (max_length = 2000, blank = True, null = True)
    defsmsres  = models.CharField (max_length = 2000, blank = True, null = True)
    defsmsclo = models.CharField (max_length = 2000, blank = True, null = True)
    search = models.CharField (max_length = 10000, blank = True, null = True)

class ComplaintMDG (models.Model):
    complainttype = models.ForeignKey (ComplaintType)
    goalnum = models.CharField (max_length = 20)

class ComplaintStatus (models.Model):
    name = models.CharField (max_length = 50)

    def __unicode__ (self):
        return self.name



class RoleException (Exception):
    pass


class AppRoleManager (models.Manager):
    def get_user_role (self, user):
        from cmh.common.constants import UserRoles
        if user.is_authenticated ():
            try:
                return AppRole.objects.get (users = user)
            except AppRole.MultipleObjectsReturned:
                raise RoleException ("Multiple Roles for user: " + user.username)
            except AppRole.DoesNotExist:
                UserRoles.ROLE_ANONYMOUS.users.add (user)
                return UserRoles.ROLE_ANONYMOUS
        else:
            return UserRoles.ROLE_ANONYMOUS

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


class StatusTransitionManager (models.Manager):
    def get_allowed_statuses (self, role, curstate):
        return ComplaintStatus.objects.filter (statustransitionnewstate__curstate = curstate, statustransitionnewstate__role = role)

    def get_changeable_statuses (self, role):
        return ComplaintStatus.objects.filter (statustransitioncurstate__role = role)


class StatusTransition (models.Model):
    role     = models.ForeignKey (AppRole, blank = True, null = True,)
    curstate = models.ForeignKey (ComplaintStatus, related_name = 'statustransitioncurstate')
    newstate = models.ForeignKey (ComplaintStatus, related_name = 'statustransitionnewstate')

    objects = StatusTransitionManager ()

