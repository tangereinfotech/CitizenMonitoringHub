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

from cmh.issuemgr.constants import GENDER_CHOICES, COMMUNITY_CHOICES


from cmh.usermgr.models import Citizen, Official, Citizen
from cmh.common.models import ComplaintStatus
from cmh.common.models import Country, State, District, Block
from cmh.common.models import GramPanchayat, Village
from cmh.common.models import ComplaintType, ComplaintDepartment

class ComplaintManager (models.Manager):
    def get_latest_complaints (self):
        return Complaint.objects.filter (latest = True)

class Complaint(models.Model):
    complainttype = models.ForeignKey (ComplaintType, blank = True, null = True, related_name = 'complaintbase')
    complaintno   = models.CharField (max_length = 50, blank = True, null = True)
    description   = models.CharField (max_length=1000)
    department    = models.ForeignKey (ComplaintDepartment, blank = True, null = True,
                                     related_name = 'complaintdepartment')
    curstate      = models.ForeignKey (ComplaintStatus, blank = True, null = True,
                                     related_name = 'complnaintstate')
    filedby       = models.ForeignKey (Citizen)
    assignto      = models.ForeignKey (Official, blank = True, null = True)
    location      = models.ForeignKey (Village, blank = True, null = True)
    logdate       = models.DateField (blank = True, null = True)
    created       = models.DateTimeField (auto_now_add = True)
    original      = models.ForeignKey ('Complaint', blank = True, null = True)
    latest        = models.BooleanField (default = True)
    creator       = models.ForeignKey (User, blank = True, null = True)
    comment       = models.CharField (max_length = 1000, blank = True, null = True)
    community     = models.CharField(max_length = 20, blank = True, null = True, choices = COMMUNITY_CHOICES, default = 'Unspecified')
    gender        = models.CharField(max_length = 20, choices = GENDER_CHOICES, blank = True, null = True, default = 'Unspecified')

    ###################################
    # Custom field for analytics only #
    ###################################
    createdate    = models.DateField (auto_now_add = True) # For querying by date

    objects = ComplaintManager ()

    def clone (self, cloner):
        self.latest = False
        self.save ()
        newver = Complaint.objects.create (complainttype = self.complainttype,
                                           complaintno = self.complaintno,
                                           description = self.description,
                                           department = self.department,
                                           curstate = self.curstate,
                                           filedby = self.filedby,
                                           assignto = self.assignto,
                                           location = self.location,
                                           logdate = self.logdate,
                                           original = self,
                                           gender = self.gender,
                                           community = self.community)
        newver.latest = True
        if cloner.is_anonymous () == False:
            newver.creator = cloner
        newver.save ()
        return newver


    def get_location_name (self):
        if self.location != None:
            return "%s [%s, %s]" % (self.location.name,
                                    self.location.grampanchayat.name,
                                    self.location.grampanchayat.block.name)
        else:
            return "----"


    def get_official_name (self):
        if self.assignto != None:
            return self.assignto.user.username
        else:
            return "----"
