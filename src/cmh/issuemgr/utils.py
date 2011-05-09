from datetime import datetime
from django.conf import settings

from cmh.issuemgr.constants import VILLAGES

def update_complaint_sequence (complaint):
    from cmh.issuemgr.models import Complaint

    todays_complaints = Complaint.objects.filter (created__year  = complaint.created.year,
                                                  created__month = complaint.created.month,
                                                  created__day   = complaint.created.day,
                                                  original = None)
    todays_complaints = todays_complaints.order_by ('created')

    first_complaint = todays_complaints [0]
    complaint.complaintno = '%s.%06d' % (complaint.created.strftime ('%Y%m%d'),
                                         (complaint.id - first_complaint.id + 1))
    complaint.save ()



def get_location_attr (block_no, gp_no, vill_no):
    loc_code = "%s.%03d.%03d.%03d" % (settings.DEPLOY_DISTT_CODE,
                                      int (block_no),
                                      int (gp_no),
                                      int (vill_no))

    return VILLAGES.get (value = loc_code)


