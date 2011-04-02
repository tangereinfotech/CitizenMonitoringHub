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

