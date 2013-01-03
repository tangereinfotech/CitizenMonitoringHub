from django.db import models
from django.contrib.auth.models import User

class IssuesDataReport(models.Model):
    complaintno = models.CharField(max_length = 14, null=True)
    filed_on    = models.CharField(max_length = 10, null= True)
    last_updated = models.CharField(max_length = 10, null=True)
    department = models.CharField(max_length = 50, null = True)
    filed_by  = models.CharField(max_length = 50, null = True)
    location  = models.CharField(max_length = 70, null = True)
    description = models.CharField(max_length = 400, null = True)
    latest_update = models.CharField(max_length = 400,null = True )
    accepted_by = models.CharField(max_length = 30, null = True)
    last_updated_by = models.CharField(max_length = 30, null = True)
    complaint_status = models.CharField(max_length = 20, null = True)
    attachments = models.CharField(max_length = 400,null = True)

class ReminderReport(models.Model):
    comp_report = models.ForeignKey(IssuesDataReport)
    comp_user = models.ForeignKey(User)
    reminder  = models.CharField(max_length = 10)

