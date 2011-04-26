from datetime import datetime


def update_complaint_sequence (complaint):
    from cmh.issuemgr.models import Complaint

    todays_complaints = Complaint.objects.filter (created__year  = complaint.created.year,
                                                  created__month = complaint.created.month,
                                                  created__day   = complaint.created.day,
                                                  original = None)
    todays_complaints = todays_complaints.order_by ('created')

    first_complaint = todays_complaints [0]
    complaint.complaintno = '%s.%06d' % (complaint.created.strftime ('%Y%m%d'),
                                         (complaint.id - first_complaint.id))
    complaint.save ()

