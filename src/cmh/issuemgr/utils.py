from datetime import datetime


def update_complaint_sequence (complaint):
    from cmh.issuemgr.models import Complaint

    todays_complaints = Complaint.objects.filter (created__year  = complaint.created.year,
                                                  created__month = complaint.created.month,
                                                  created__day   = complaint.created.day,
                                                  location       = complaint.location)
    todays_complaints = todays_complaints.order_by ('created')

    first_complaint = todays_complaints [0]
    complaint.complaintno = 'C.%s.%04d.%s' % (complaint.created.strftime ('%m%d'),
                                              (complaint.id - first_complaint.id),
                                              complaint.location.value)
    complaint.save ()



