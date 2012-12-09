from cmh.issuemgr.models import Complaint, ComplaintEvidence, ComplaintReminder, ComplaintClosureMetric, ComplaintManager
from cmh.smsgateway.models import TextMessage
from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.utils.simplejson import dumps
from django.http import HttpResponse

def get_generated_time(t):
    if (t is not None and t.created):
        return t.created.strftime("%y.%m.%d")
    else:
        return ''

def get_processed_time(t):
    if (t is not None and t.processed_time is not None):
        return t.created.strftime("%y.%m.%d")
    else:
        return ''

def get_processed(t):
    if (t is not None and t.processed is not None):
        return t.processed
    else:
        return ''

def get_recepient(t):
    if (t is not None and t.phone is not None):
        return t.phone
    else:
        return ''

def get_message(t):
    if (t is not None and t.message is not None):
        return t.message
    else:
        return ''

sms_logs_column_properties = {
    0: { 'code'     :'generated_time',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Generated Time'),
        'type'      : 'string',
        'search_str': _('Search Generated Time'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'fnGetData' : get_generated_time
    },
    1: { 'code'     :'processed_time',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Processed Time'),
        'type'      : 'string',
        'search_str': _('Search Processed Time'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'fnGetData' : get_processed_time
    },
    2: { 'code'     :'processed',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Processed'),
        'type'      : 'string',
        'search_str': _('Search Processed'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'fnGetData' : get_processed
    },
    3: { 'code'     :'recepient',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Recepient'),
        'type'      : 'string',
        'search_str': _('Search Recepient'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'fnGetData' : get_recepient
    },
    4: { 'code'     :'message',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Message'),
        'type'      : 'string',
        'search_str': _('Search Message'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'fnGetData' : get_message
    },
}

def report_sms_logs_data(request):
    mdata = cache.get('sms_logs_data')
    if mdata == None:
        cdata = []
        messages = TextMessage.objects.all()
        for msg in messages:
            row = []
            for i in range(0,len(sms_logs_column_properties)):
                row.append(sms_logs_column_properties[i]['fnGetData'](msg))
            cdata.append(row)
        mdata = dumps({'aaData': cdata})
        cache.set('sms_logs_data', mdata,24*60*60)
    return HttpResponse(mdata)
