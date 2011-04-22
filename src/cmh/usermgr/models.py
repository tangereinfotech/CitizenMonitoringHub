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
from cmh.common.models import Attribute, Category, CodeName

class Citizen(models.Model):
    name   = models.CharField (max_length = 500, blank = True, null = True)
    mobile = models.CharField (max_length = 15, blank=True,null=True)

    def __unicode__(self):
        return "Citizen: " + self.name


class Official(models.Model):
    user        = models.OneToOneField (User)
    designation = models.CharField (max_length = 200, blank = True, null = True)
    supervisor  = models.ForeignKey ('Official', blank=True, null=True)
    location    = models.ForeignKey (Attribute, related_name = 'location_official')
    mobile      = models.CharField (max_length=15, blank=True,null=True)
    department  = models.ManyToManyField (Attribute, related_name = 'department_official')

    def __unicode__(self):
        return u'Official: ' + self.user.username


class AppRole (models.Model):
    role  = models.IntegerField ()
    name  = models.CharField (max_length = 50)
    users = models.ManyToManyField (User)

    def __unicode__ (self):
        return self.name


class MenuItem (models.Model):
    name   = models.CharField (max_length = 500)
    url    = models.CharField (max_length = 500)
    role   = models.ForeignKey (AppRole)
    serial = models.IntegerField ()

    class Meta:
        unique_together = (('role', 'serial'),)
