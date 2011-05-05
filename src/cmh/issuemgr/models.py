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
from django.contrib.auth.models import User

from cmh.usermgr.models import Citizen, Official, Citizen, AppRole
from cmh.common.models import CodeName, Category, Attribute

class ComplaintItem (CodeName):
    desc    = models.CharField (max_length = 5000)

class ComplaintManager (models.Manager):
    def get_latest_complaints (self):
        return Complaint.objects.filter (latest = True)

class Complaint(models.Model):
    base        = models.ForeignKey (Attribute, blank = True, null = True,
                                     related_name = 'complaintbase')
    complaintno = models.CharField (max_length = 50, blank = True, null = True)
    description = models.CharField (max_length=1000)
    department  = models.ForeignKey (Attribute, blank = True, null = True,
                                     related_name = 'complaintdepartment')
    curstate    = models.ForeignKey (Attribute, blank = True, null = True,
                                     related_name = 'complnaintstate')
    filedby     = models.ForeignKey (Citizen)
    assignto    = models.ForeignKey (Official, blank = True, null = True)
    location    = models.ForeignKey (Attribute, blank = True, null = True,
                                     related_name = 'complaintlocation')
    logdate     = models.DateField (blank = True, null = True)
    original    = models.ForeignKey ('Complaint', blank = True, null = True)
    created     = models.DateTimeField (auto_now_add = True)
    latest      = models.BooleanField (default = True)
    creator     = models.ForeignKey (User, blank = True, null = True)
    comment     = models.CharField (max_length = 1000, blank = True, null = True)

    objects = ComplaintManager ()

    def clone (self):
        self.latest = False
        self.save ()
        return Complaint.objects.create (base = self.base,
                                         complaintno = self.complaintno,
                                         description = self.description,
                                         department = self.department,
                                         curstate = self.curstate,
                                         filedby = self.filedby,
                                         assignto = self.assignto,
                                         location = self.location,
                                         logdate = self.logdate,
                                         original = self)

    def get_location_name (self):
        if self.location != None:
            vill_code = self.location.value
            gp_code = self.location.parent.value
            block_code = self.location.parent.parent.value
            vill_name = CodeName.objects.get (code = vill_code).name
            gp_name = CodeName.objects.get (code = gp_code).name
            block_name = CodeName.objects.get (code = block_code).name

            return "%s [%s, %s]" % (vill_name, gp_name, block_name)
        else:
            return "----"


    def get_department_name (self):
        if self.department != None:
            dept_code = self.department.value
            dept_name = CodeName.objects.get (code = dept_code).name
        else:
            dept_name = "----"
        return dept_name

    def get_official_name (self):
        if self.assignto != None:
            return self.assignto.user.username
        else:
            return "----"

    def __unicode__ (self):
        return self.complaintno

class StatusTransitionManager (models.Manager):
    def get_allowed_statuses (self, role, curstate):
        return Attribute.objects.filter (newstate__curstate = curstate, newstate__role = role)

class StatusTransition (models.Model):
    role     = models.ForeignKey (AppRole, blank = True, null = True,)
    curstate = models.ForeignKey (Attribute, related_name = 'curstate', blank = True, null = True)
    newstate = models.ForeignKey (Attribute, related_name = 'newstate', blank = True, null = True)

    objects = StatusTransitionManager ()
