from django.db import models
from django.contrib.auth.models import User

class IssuesDataReport(models.Model):
    complaintno = models.CharField(max_length = 14)
    filed_on    = models.CharField(max_length = 10)
    last_updated = models.CharField(max_length = 10)
    department = models.CharField(max_length = 50)
    filed_by  = models.CharField(max_length = 50)
    location  = models.CharField(max_length = 70)
    description = models.CharField(max_length = 400)
    latest_update = models.CharField(max_length = 400)
    accepted_by = models.CharField(max_length = 30)
    last_updated_by = models.CharField(max_length = 30)
    complaint_status = models.CharField(max_length = 20)
    attachments = models.CharField(max_length = 400)

class ReminderReport(models.Model):
    comp_report = models.ForeignKey(IssuesDataReport)
    comp_user = models.ForeignKey(User)
    reminder  = models.CharField(max_length = 10)

