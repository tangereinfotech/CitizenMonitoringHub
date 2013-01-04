from django.db import models
from django.contrib.auth.models import User
from cmh.common.models import ComplaintDepartment, ComplaintStatus

class IssuesDataReport(models.Model):
    complaintno = models.CharField(max_length = 20, null=True, blank=True)
    filed_on    = models.CharField(max_length = 20, null=True, blank=True)
    last_updated = models.CharField(max_length = 20, null=True, blank=True)
    department = models.ForeignKey(ComplaintDepartment, blank=True, null=True)
    department_name = models.CharField(max_length = 50, blank=True, null=True)
    filed_by  = models.TextField(null=True, blank=True)
    location  = models.CharField(max_length = 70, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    latest_update = models.TextField(null=True, blank=True)
    accepted_by = models.CharField(max_length = 50, null=True, blank=True)
    last_updated_by = models.CharField(max_length = 50, null=True, blank=True)
    complaint_status = models.CharField(max_length = 20, null=True, blank=True)
    action = models.CharField(max_length = 400, null=True, blank=True)
    attachments = models.TextField(null=True, blank=True)

class ReminderReport(models.Model):
    comp_report = models.ForeignKey(IssuesDataReport)
    comp_user = models.ForeignKey(User)
    reminder  = models.CharField(max_length = 10)

