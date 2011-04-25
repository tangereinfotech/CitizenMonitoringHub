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
from cmh.usermgr.models import Citizen, Official, Citizen
from cmh.common.models import CodeName, Category, Attribute

class ComplaintItem (CodeName):
    desc    = models.CharField (max_length = 5000)

class Complaint(models.Model):
    base        = models.ForeignKey (Attribute, blank = True, null = True,
                                     related_name = 'complaintbase')
    complaintno = models.CharField (max_length = 50, blank = True, null = True)
    description = models.CharField (max_length=200)
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

    def clone (self):
        return Complaint.objects.create (base = self.base,
                                         complaintno = self.complaintno,
                                         description = self.description,
                                         department = self.department,
                                         cutstate = self.curstate,
                                         filedby = self.filedby,
                                         assignto = self.assignto,
                                         location = self.location,
                                         logdate = self.logdate,
                                         original = self)


    def __unicode__ (self):
        return self.complaintno
