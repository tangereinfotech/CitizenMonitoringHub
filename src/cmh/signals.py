from django.db.models.signals import post_save
from django.dispatch import receiver
from cmh.issuemgr.models import Complaint
from cmh.reports.report_issues import create_or_update_idr
from cmh.common.models import ComplaintDepartment


@receiver(post_save, sender = Complaint, weak=False)
def update_all_issues_complaint_report(sender, **kwargs):
    comp = kwargs['instance']
    create_or_update_idr(comp)

@receiver(post_save, sender = ComplaintDepartment)
def update_all_issues_complaint_department(sender, **kwargs):
    department = kwargs['instance']
    idrs = IssuesDataReport.objects.filter(department = department).update(department_name = department.code)
