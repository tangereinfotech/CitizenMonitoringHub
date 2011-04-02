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
from cmh.PeopleMgr.models import Location, Citizen, Official
from cmh.Common.models import Category, Attribute

class ComplaintState (models.Model):
    state = models.CharField(max_length=20)

    def __unicode__(self):
        return self.state

class Complaint(models.Model):
    origindate  = models.DateField ()
    description = models.CharField (max_length=200)
    filedby     = models.ForeignKey (Citizen)
    assignto    = models.ForeignKey (Official)
    location    = models.ForeignKey (Location)
    curstate    = models.ForeignKey (ComplaintState)
    complaintno = models.IntegerField()
    complainttype = models.ForeignKey (Attribute, blank = True, null = True, related_name = "complainttype")
    department    = models.ForeignKey (Attribute, blank = True, null = True, related_name = "department")

    def __unicode__(self):
        return u'%d, %s' % (self.complaintno, self.curstate)

    class Meta:
        ordering =['curstate']


class ComplaintHistory(models.Model):
    statefrom       = models.ForeignKey(ComplaintState, related_name='complainthistorystatefrom')
    stateto         = models.ForeignKey(ComplaintState, related_name='complainthistorystateto')
    description     = models.CharField(max_length=200)
    changedate      = models.DateField()
    complaint       = models.ForeignKey(Complaint)

    class Meta:
        ordering = ['-changedate']

