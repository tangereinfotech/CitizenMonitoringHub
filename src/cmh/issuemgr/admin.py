from django.contrib import admin
from cmh.issuemgr.models import ComplaintState, Complaint

admin.site.register(ComplaintState)
admin.site.register(Complaint)
