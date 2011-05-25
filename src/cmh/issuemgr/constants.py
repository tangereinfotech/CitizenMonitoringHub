from cmh.common.models import ComplaintStatus

STATUS_NEW      = ComplaintStatus.objects.get (name = 'New')
STATUS_REOPEN   = ComplaintStatus.objects.get (name = 'Reopened')
STATUS_ACK      = ComplaintStatus.objects.get (name = 'Acknowledged')
STATUS_OPEN     = ComplaintStatus.objects.get (name = 'Open')
STATUS_RESOLVED = ComplaintStatus.objects.get (name = 'Resolved')
STATUS_CLOSED   = ComplaintStatus.objects.get (name = 'Closed')

class HotComplaintPeriod:
    WEEK    = 1
    MONTH   = 2
    QUARTER = 3

