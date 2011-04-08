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

from django.db import models
from cmh.usermgr.models import Location, Citizen, Official
from cmh.common.models import CodeName


class State (CodeName):
    pass

class District (CodeName):
    state = models.ForeignKey (State)

class Block (CodeName):
    distt = models.ForeignKey (District)

class GramPanchayat (CodeName):
    block = models.ForeignKey (Block)

class Village (CodeName):
    gp = models.ForeignKey (GramPanchayat)
    latitude = models.FloatField ()
    longitude = models.FloatField ()

class ComplaintState (models.Model):
    state = models.CharField (max_length=100)

    def __unicode__(self):
        return self.state

class Department (CodeName):
    state = models.ForeignKey (State, blank = True, null = True)

class ComplaintItem (CodeName):
    desc    = models.CharField (max_length = 5000)
    department = models.ForeignKey (Department)

class Complaint(models.Model):
    base        = models.ForeignKey (ComplaintItem, blank = True, null = True)
    complaintno = models.CharField (max_length = 50, blank = True, null = True)
    description = models.CharField (max_length=200)
    department  = models.ForeignKey (Department, blank = True, null = True)
    curstate    = models.ForeignKey (ComplaintState)
    filedby     = models.ForeignKey (Citizen)
    assignto    = models.ForeignKey (Official, blank = True, null = True)
    location    = models.ForeignKey (Village, blank = True, null = True)
    original    = models.ForeignKey ('Complaint', blank = True, null = True)
    created     = models.DateTimeField (auto_now_add = True)


