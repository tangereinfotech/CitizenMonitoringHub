from django.contrib import admin
from cmh.issuemgr.models import ComplaintState, Complaint, ComplaintHistory

admin.site.register(ComplaintState)
admin.site.register(Complaint)
admin.site.register(ComplaintHistory)
