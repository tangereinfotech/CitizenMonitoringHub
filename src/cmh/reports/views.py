from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.utils.simplejson import dumps
from django.utils.translation import ugettext as _
from cmh.issuemgr.models import Complaint, ComplaintEvidence, ComplaintReminder, ComplaintClosureMetric, ComplaintManager
from django.contrib.auth.decorators import login_required
from cmh.usermgr.utils import get_user_menus

def get_complaint_no(c):
    if (c is not None):
        return c.complaintno
    else:
        return ''

def get_filed_on(c, fmt="%y.%m.%d"):
    if ((c is not None) and (c.original is not None) and (c.original.logdate is not None)):
        return c.original.logdate.strftime(fmt)
    else:
        return ''

def get_last_updated(c,fmt="%y.%m.%d"):
    if (c is not None):
        return c.created.strftime(fmt)
    else:
        return 'Not available'

def get_filed_on_sort(c, fmt="%Y%m%d"):
    return get_filed_on(c, fmt)

def get_last_updated_sort(c,fmt="%Y%m%d"):
    return get_last_updated(c, fmt)

def get_department(c):
    if ((c is not None) and (c.department is not None) and (c.department.code is not None)):
        return c.department.code
    else:
        return ''

def get_location(c):
    if ((c is not None) and (c.location is not None)):
        return c.location.search[:-22]

def get_description(c):
    if ((c is not None) and (c.original is not None)):
        return c.original.description
    elif (c is not None):
        return c.description
    else:
        return ''

def get_latest_update(c):
    if (c is not None):
        return c.description
    else:
        return ''

def get_filed_by(c):
    if (c is not None) and (c.filedby is not None):
        return c.filedby.name
    else:
        return ''

def get_accepted_by(c):
    comps = Complaint.objects.filter(complaintno = c.complaintno)
    ack_comps = comps.filter(curstate__name = 'Acknowledged').order_by('created')
    if len(ack_comps) > 0:
        ack_comp = ack_comps[0]
        if ack_comp.creator != None:
            return ack_comp.creator.username
        return 'Not available'
    else:
        return 'Not available'

def get_last_updated_by(c):
    if (c.creator != None) and (c.creator != ''):
        return c.creator.username
    else:
        return 'System'

def get_workflow_state(c):
    if (c is not None):
        return c.curstate.name
    else:
        return ''

def get_attachments(c):
    evi_str = ''
    comps = Complaint.objects.filter(complaintno = c.complaintno)
    for c in comps:
        for evi in c.evidences.all():
            evi_str = evi_str+  '<a href=' + evi.url + ' target="_blank">' + evi.filename + '</a><br/>'
    return evi_str

def get_action(c):
    update_url = "/complaint/track/" + c.complaintno
    update_url = '<a href=' + update_url + ' target="_blank">update</a>'
    return update_url

columProperties = {
    0: { 'code'     :'complaintno',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Complaint No'),
        'type'      : 'string',
        'search_str': _('Search Complaint Numbers'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'fnGetData' : get_complaint_no
    },
    1: {'code'      : 'filed_on',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Filed On(YY.MM.DD)'),
        'type'      : 'string',
        'search_str': _('Search Filed On Date'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'fnGetData' : get_filed_on

    },
    2: {'code'      : 'last_updated',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Last Updated(YY.MM.DD)'),
        'type'      : 'string',
        'search_str': _('Search Last Updated'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'fnGetData' : get_last_updated
    },
    3: {'code'      :'department',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Department'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : False,
        'search_str': _('Search Department'),
        'fnGetData' : get_department
    },
    4: {'code': 'location',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Location(Vill/Gram Panchayat/Block)'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Description'),
        'fnGetData' : get_location
    },
    5: {'code': 'description',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Description'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Description'),
        'fnGetData' : get_description
    },
    6: {'code': 'latest_update',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Latest Update'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Latest Update'),
        'fnGetData' : get_latest_update
    },
    7: {'code': 'filed_by',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Filed By'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Filed By'),
        'fnGetData' : get_filed_by
    },
    8: {'code': 'accepted_by',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Accepted By'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Accepted By'),
        'fnGetData' : get_accepted_by,
    },
    9: {'code': 'last_updated_by',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Last Updated By'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
         'search_str': _('Search Last Updated By'),
        'fnGetData' : get_last_updated_by,
    },
    10: {'code': 'workflow_state',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Complaint Status'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Workflow State'),
        'fnGetData' : get_workflow_state,
    },
    11: {'code': 'attachments',
        'searchable': False,
        'sortable'  : False,
        'name'      : _('Attachments'),
        'type'      : 'html',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': '',
        'fnGetData' : get_attachments,
    },
    12 : {'code' : 'action',
          'searchable': False,
          'sortable'  : False,
          'name'      :_('Action'),
          'type'      : 'html',
          'sClass'    : 'cellformat',
          'bVisible'  : True,
          'search_str': '',
        'fnGetData' : get_action,
    }
}

def home(request):
    return render_to_response('report_all_issues.html', {'cols': columProperties, 'menus': get_user_menus(request.user, home)}, context_instance = RequestContext(request))


def my_issues_data(request):
    latest_complaints = Complaint.objects.filter(latest = True)
    cdata = []
    for comp in latest_complaints:
        row = []
        for i in range(0,len(columProperties)):
            row.append(columProperties[i]['fnGetData'](comp))
        cdata.append(row)

    mdata = dumps({'aaData': cdata})
    return HttpResponse(mdata)
