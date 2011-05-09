from cmh.common.models import Attribute

COUNTRY    = Attribute.objects.get (category__key = 'Country')
COMPLAINT  = Attribute.objects.get (category__key = 'Complaint')

STATES     = COUNTRY.get_category_descendents ('State')
VILLAGES   = COUNTRY.get_category_descendents ('Village')
COMPLAINT_TYPES   = COMPLAINT.get_category_descendents ('Complaint Type')

STATUS_NEW      = Attribute.objects.get (category__key = 'Status', value = 'New')
STATUS_REOPEN   = Attribute.objects.get (category__key = 'Status', value = 'Reopened')
STATUS_ACK      = Attribute.objects.get (category__key = 'Status', value = 'Acknowledged')
STATUS_OPEN     = Attribute.objects.get (category__key = 'Status', value = 'Open')
STATUS_RESOLVED = Attribute.objects.get (category__key = 'Status', value = 'Resolved')
STATUS_CLOSED   = Attribute.objects.get (category__key = 'Status', value = 'Closed')

DEPARTMENTS = COMPLAINT.get_category_descendents ('Complaint Department')

STATUSES = Attribute.objects.filter (category__key = 'Status')
