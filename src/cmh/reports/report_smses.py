from cmh.smsgateway.models import TextMessage, ReceivedTextMessage
from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.utils.simplejson import dumps
from django.http import HttpResponse

def get_generated_time(t):
    if (t.__class__.__name__ == 'TextMessage'):
        if (t is not None and t.created):
            return t.created.strftime("%y.%m.%d %H:%M:%S")
        else:
            return ''
    elif (t.__class__.__name__ == 'ReceivedTextMessage'):
        return t.created.strftime("%y.%m.%d %H:%M:%S")
    else:
        return ''

def get_processed_time(t):
    if (t.__class__.__name__ == 'TextMessage'):
        if (t is not None and t.processed_time is not None):
            return t.created.strftime("%y.%m.%d %H:%M:%S")
        else:
            return ''
    elif (t.__class__.__name__ == 'ReceivedTextMessage'):
        return t.created.strftime("%y.%m.%d %H:%M:%S")
    else:
        return ''

def get_processed(t):
    if (t.__class__.__name__ == 'TextMessage'):
        if (t is not None and t.processed is not None):
            if (t.processed):
                return 'Yes, Processed'
            else:
                return 'Not Yet'
        else:
            return ''
    else:
        return 'NA'

def get_recepient(t):
    if (t.__class__.__name__ == 'TextMessage'):
        if (t is not None and t.phone is not None):
            return t.phone
        else:
            return ''
    else:
        if (t is not None and t.sender is not None):
            return t.sender
        else:
            return ''

def get_message(t):
    if (t is not None and t.message is not None):
        return t.message
    else:
        return ''

def get_processed_state():
    return ['Not Yet', 'Yes, Processed', 'NA']

def get_sms_direction(t):
    if (t.__class__.__name__ == 'TextMessage'):
       return 'Outgoing'
    elif (t.__class__.__name__ == 'ReceivedTextMessage'):
        return 'Incoming'
    else:
        return ''

def get_sms_direction_options():
    return ['Incoming', 'Outgoing']

sms_logs_column_properties = {
    0: { 'code'     :'generated_time',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Generated Time'),
        'type'      : 'string',
        'search_str': _('Search Generated Time'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        "sWidth"    : None,
        'inputtype' : 'input',
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
        'inputtype' : 'input',
        "sWidth"    : None,
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
        'inputtype' : 'select',
        "sWidth"    : None,
        'select_option' : get_processed_state,
        'fnGetData' : get_processed
    },
    3: { 'code'     :'direction',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Direction'),
        'type'      : 'string',
        'search_str': _('Search Direction'),
        'inputtype' : 'select',
        'select_option': get_sms_direction_options,
        'bVisible'  : True,
        "sWidth"    : None,
        'sClass'    : 'cellformat',
        'fnGetData' : get_sms_direction,
    },
    4: { 'code'     :'recepient',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Recepient/Sender'),
        'type'      : 'string',
        'search_str': _('Search Recepient/Sender'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'inputtype' : 'input',
        "sWidth"    : None,
        'fnGetData' : get_recepient
    },
    5: { 'code'     :'message',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Message'),
        'type'      : 'string',
        'search_str': _('Search Message'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'inputtype' : 'input',
        "sWidth"    : None,
        'fnGetData' : get_message
    },
}

def report_sms_logs_data(request):
    mdata = None
    if mdata == None:
        cdata = []
        sent_messages = TextMessage.objects.all()
        rec_messages = ReceivedTextMessage.objects.all()

        for msg in sent_messages:
            row = []
            for i in range(0,len(sms_logs_column_properties)):
                row.append(sms_logs_column_properties[i]['fnGetData'](msg))
            cdata.append(row)
        for msg in rec_messages:
            row = []
            for i in range(0,len(sms_logs_column_properties)):
                row.append(sms_logs_column_properties[i]['fnGetData'](msg))
            cdata.append(row)
        mdata = dumps({'aaData': cdata})
    return HttpResponse(mdata)
