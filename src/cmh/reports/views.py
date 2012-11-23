from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.utils.simplejson import dumps
from django.utils.translation import ugettext as _
from cmh.issuemgr.models import Complaint, ComplaintEvidence, ComplaintReminder, ComplaintClosureMetric, ComplaintManager

columProperties = {
    0: { 'code'     :'complaintno',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Complaint No'),
        'type'      : 'string',
        'search_str': _('Search Complaint Numbers'),
        'bVisible'  : True,
        'sClass'    : 'cellformat'
    },
    1: {'code'      : 'filed_on',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Filed On'),
        'type'      : 'date',
        'search_str': _('Search Filed On Date'),
        'bVisible'  : True,
        'sClass'    : 'cellformat'
    },
    2: {'code'      : 'last_updated',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Last Updated'),
        'type'      : 'date',
        'search_str': _('Search Last Updated'),
        'bVisible'  : True,
        'sClass'    : 'cellformat'
    },
    3: {'code'      :'department',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Department'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : False,
        'search_str': _('Search Department')
    },
    4: {'code': 'location',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Location(Vill/Gram Panchayat/Block)'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Description')
    },
    5: {'code': 'description',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Description'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Description')
    },
    6: {'code': 'latest_update',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Latest Update'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Latest Update')
    },
    7: {'code': 'filed_by',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Filed By'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Filed By')
    },
    8: {'code': 'accepted_by',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Accepted By'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Accepted By')
    },
    9: {'code': 'last_updated_by',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Last Updated By'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
         'search_str': _('Search Last Updated By')
    },
    10: {'code': 'workflow_state',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Complaint Status'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Workflow State')
    },
    11: {'code': 'attachments',
        'searchable': False,
        'sortable'  : False,
        'name'      : _('Attachments'),
        'type'      : 'html',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': ''
    },
    12 : {'code' : 'action',
          'searchable': False,
          'sortable'  : False,
          'name'      :_('Action'),
          'type'      : 'html',
          'sClass'    : 'cellformat',
          'bVisible'  : True,
          'search_str': ''
    }
}
def home(request):
    return render_to_response('report_all_issues.html', {'cols': columProperties}, context_instance = RequestContext(request))


def my_issues_data(request):
    latest_complaints = Complaint.objects.filter(latest = True)
    cdata = []
    for comp in latest_complaints:
        row = []
        update_url = "/complaint/track/" + comp.complaintno
        evi_str = ''
        comps = Complaint.objects.filter(complaintno = comp.complaintno)
        for c in comps:
            for evi in c.evidences.all():
                evi_str = evi_str+  '<a href=' + evi.url + '>' + evi.filename + '</a><br/>'
        ack_comps = comps.filter(curstate__name = 'Acknowledged').order_by('created')
        if len(ack_comps) > 0:
            ack_comp = ack_comps[0]
        else:
            ack_comp = ''
        cdata.append([comp.complaintno, comp.logdate.strftime("%d/%m/%y"),comp.created.strftime("%d/%m/%y"), comp.department.code,comp.location.search[:-22],comp.original.description, comp.description, comp.filedby.name, (lambda x: x.creator.username if x and (x.creator != None) else ' ')(ack_comp), (lambda x: x.creator.username if x.creator != None else ' ')(comp),comp.curstate.name[:6],evi_str,'<a href=' + update_url + '>update</a>'])
    mdata = dumps({'aaData': cdata})
    return HttpResponse(mdata)
