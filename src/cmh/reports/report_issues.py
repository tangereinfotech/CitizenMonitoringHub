from cmh.issuemgr.models import Complaint, ComplaintEvidence, ComplaintReminder, ComplaintClosureMetric, ComplaintManager
from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.utils.simplejson import dumps,loads
from django.http import HttpResponse,Http404
from cmh.common.constants import UserRoles
from django.core.exceptions import ObjectDoesNotExist
from cmh.common.models import ComplaintDepartment, ComplaintStatus
from cmh.reports.models import IssuesDataReport

def get_complaint_no(c,request=None):
    if (c is not None):
        return c.complaintno
    else:
        return ''

def get_filed_on(c, request=None, fmt="%Y.%m.%d"):
    if ((c is not None) and (c.original is not None) and (c.original.logdate is not None)):
        return c.logdate.strftime(fmt)
    else:
        return ''

def get_last_updated(c,request=None,fmt="%Y.%m.%d::%H:%M"):
    if (c is not None):
        return c.created.strftime(fmt)
    else:
        return 'Not available'

def get_filed_on_sort(c,request=None, fmt="%Y%m%d"):
    return get_filed_on(c, fmt)

def get_last_updated_sort(c,request = None,fmt="%Y%m%d"):
    return get_last_updated(c, fmt)

def get_department(c,request=None):
    if ((c is not None) and (c.department is not None) and (c.department.code is not None)):
        return c.department
    else:
        return None

def get_department_name(c,request=None):
    if ((c is not None) and (c.department is not None) and (c.department.code is not None)):
        return c.department.code
    else:
        return ''

def get_location(c,request=None):
    if ((c is not None) and (c.location is not None)):
        if (c.location.name == c.location.grampanchayat.name):
            return c.location.name + "<br/>"  + c.location.grampanchayat.block.name
        else:
            return c.location.name + "<br/>" + c.location.grampanchayat.name + "<br/>" + c.location.grampanchayat.block.name

def get_description(c,request=None):
    c = Complaint.objects.filter(complaintno = c.complaintno).order_by('created')[0]
    return c.description

def get_latest_update(c,request=None):
    if (c != None):
        return c.description
    else:
        return ''

def get_filed_by(c,request=None):
    if (c is not None) and (c.filedby is not None):
        return c.filedby.name
    else:
        return ''

def get_accepted_by(c,request=None):
    comps = Complaint.objects.filter(complaintno = c.complaintno)
    ack_comps = comps.filter(curstate__name = 'Acknowledged').order_by('created')
    if len(ack_comps) > 0:
        ack_comp = ack_comps[0]
        if ack_comp.creator != None:
            return ack_comp.creator.username
        return 'Not available'
    else:
        return 'Not available'

def get_last_updated_by(c,request=None):
    if (c.creator != None) and (c.creator != ''):
        return c.creator.username
    else:
        return 'System'

def get_workflow_state(c,request=None):
    if (c is not None):
        return c.curstate.name
    else:
        return ''

def get_attachments(c,request=None):
    evi_str = ''
    comps = Complaint.objects.filter(complaintno = c.complaintno)
    for c in comps:
        for evi in c.evidences.all():
            evi_str = evi_str+  '<a href=' + evi.url + ' target="_blank">' + evi.filename + '</a><br/>'
    return evi_str

def get_action(c,request = None):
    update_url = ''
    track_url  = ''
    if c != None:
        if (c.curstate.name != 'Closed'):
            update_url = "/complaint/update/" + c.complaintno
            update_url = '<a href=' + update_url + ' target="_blank">update</a>'
        track_url = "/complaint/track/" + c.complaintno
        track_url = '<a href=' + track_url + ' target="_blank">track</a>'
    return track_url + '<br/>' + update_url

def get_reminder(c,request):
    try:
        reminder = ComplaintReminder.objects.get(complaintno = c.complaintno, user = request.user)
        return reminder.reminderon.strftime("%y.%m.%d")
    except ObjectDoesNotExist:
        return ''
    except:
        return ''

def get_department_select():
    codes = [d.code for d in ComplaintDepartment.objects.all()]
    return sorted(codes)

def get_workflow_select():
    return [s.name for s in ComplaintStatus.objects.all()]
    return ''


all_issues_column_properties = {
    0: { 'code'     :'complaintno',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Complaint No'),
        'type'      : 'string',
        'search_str': _('Search Complaint Numbers'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'inputtype': 'input',
        "sWidth"    : None,
        'fnGetData' : get_complaint_no
    },
    1: {'code'      : 'filed_on',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Filed On'),
        'type'      : 'string',
        'search_str': _('Search Filed On Date'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'inputtype': 'input',
        "sWidth"    : None,
        'fnGetData' : get_filed_on

    },
    2: {'code'      : 'last_updated',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Last Updated'),
        'type'      : 'string',
        'search_str': _('Search Last Updated'),
        'bVisible'  : True,
        'sClass'    : 'cellformat',
        'inputtype': 'input',
        "sWidth"    : None,
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
        'inputtype': 'select',
        "sWidth"    : None,
        'select_option': get_department_select,
        'fnGetData' : get_department
    },
    4: {'code': 'filed_by',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Filed By'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        "sWidth"    : None,
        'search_str': _('Search Filed By'),
        'inputtype': 'input',
        'fnGetData' : get_filed_by
    },
    5: {'code': 'location',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Location'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        "sWidth"    : None,
        'search_str': _('Search Locations'),
        'inputtype': 'input',
        'fnGetData' : get_location
    },
    6: {'code': 'description',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Description'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        "sWidth"    : "200px",
        'search_str': _('Search Description'),
        'inputtype': 'input',
        'fnGetData' : get_description
    },
    7: {'code': 'latest_update',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Latest Update'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Latest Update'),
        'inputtype': 'input',
        "sWidth"    : "200px",
        'fnGetData' : get_latest_update
    },
    8: {'code': 'accepted_by',
        'searchable': True,
        'sortable'  : True,
        'name'      : _('Accepted By'),
        'type'      : 'string',
        'sClass'    : 'cellformat',
        'bVisible'  : True,
        'search_str': _('Search Accepted By'),
        'inputtype': 'input',
        "sWidth"    : None,
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
        'inputtype': 'input',
        "sWidth"    : None,
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
        'inputtype': 'select',
        "sWidth"    : None,
        'select_option': get_workflow_select,
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
        "sWidth"    : None,
        'inputtype': 'input',
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
          "sWidth"    : None,
          'inputtype': 'input',
          'fnGetData' : get_action,
    },
    13 : {'code' : 'reminder',
          'searchable': True,
          'sortable'  : True,
          'name'      :_('Reminder'),
          'search_str': _('Search Reminder Date'),
          'type'      : 'html',
          'sClass'    : 'cellformat',
          'bVisible'  : False,
           "sWidth"    : None,
          'inputtype': 'input',
          'fnGetData' : get_reminder,
    }
}
def compose_all_data():
    comps = Complaint.objects.filter(latest = True)
    for comp in comps:
        create_or_update_idr(comp)

from datetime import datetime
def report_all_issues_data(request):
    cdata = []
    for idr in IssuesDataReport.objects.all():
        row = {}
        row['0'] = idr.complaintno
        row['1'] = idr.filed_on
        row['2'] = idr.last_updated
        row['3'] = idr.department_name
        row['4'] = idr.filed_by
        row['5'] = idr.location
        row['6'] = idr.description
        row['7'] = idr.latest_update
        row['8'] = idr.accepted_by
        row['9'] = idr.last_updated_by
        row['10'] = idr.complaint_status
        row['11'] = idr.attachments
        row['12'] = idr.action
        row['13'] = ''
        row["DT_RowID"] = str(idr.complaintno)
        cdata.append(row)
    return HttpResponse(dumps({'aaData': cdata}))

def report_my_issues_data(request):

    cdata = []
    role = request.user.cmhuser.get_user_role()
    if (role == UserRoles.ROLE_OFFICIAL or role == UserRoles.ROLE_DELEGATE):
        official = request.user.official
        idrs = IssuesDataReport.objects.filter(department = official.department)
        for idr in idrs:
            row = {}
            row['0'] = idr.complaintno
            row['1'] = idr.filed_on
            row['2'] = idr.last_updated
            row['3'] = idr.department_name
            row['4'] = idr.filed_by
            row['5'] = idr.location
            row['6'] = idr.description
            row['7'] = idr.latest_update
            row['8'] = idr.accepted_by
            row['9'] = idr.last_updated_by
            row['10'] = idr.complaint_status
            row['11'] = idr.attachments
            row['12'] = idr.action
            row['13'] = ''
            row["DT_RowID"] = str(idr.complaintno)
            cdata.append(row)
        return HttpResponse(dumps({'aaData': cdata}))
    elif (role == UserRoles.ROLE_DM or UserRoles.ROLE_CSO):
        return report_all_issues_data(request)
    else:
        raise Http404

def create_or_update_idr(ch_comp):
    if ch_comp.complaintno:
        cs = Complaint.objects.filter(complaintno = ch_comp.complaintno).filter(latest = True)
        if cs.count() == 1:
            comp = cs[0]
            try:
                idr = IssuesDataReport.objects.get(complaintno = comp.complaintno)
                idr.complaintno = get_complaint_no(comp)
                idr.filed_on = get_filed_on(comp)
                idr.last_updated = get_last_updated(comp)
                idr.department = get_department(comp)
                idr.department_name = get_department_name(comp)
                idr.filed_by = get_filed_by(comp)
                idr.location= get_location(comp)
                idr.description = get_description(comp)
                idr.latest_update = get_latest_update(comp)
                idr.accepted_by = get_accepted_by(comp)
                idr.last_updated_by = get_last_updated_by(comp)
                idr.complaint_status = get_workflow_state(comp)
                idr.attachments = get_attachments(comp)
                idr.action = get_action(comp)
                idr.save()
            except ObjectDoesNotExist:
                IssuesDataReport.objects.create(complaintno = get_complaint_no(comp),
                                                filed_on = get_filed_on(comp),
                                                last_updated = get_last_updated(comp),
                                                department = get_department(comp),
                                                department_name = get_department_name(comp),
                                                filed_by = get_filed_by(comp),
                                                location= get_location(comp),
                                                description = get_description(comp),
                                                latest_update = get_latest_update(comp),
                                                accepted_by = get_accepted_by(comp),
                                                last_updated_by = get_last_updated_by(comp),
                                                complaint_status = get_workflow_state(comp),
                                                attachments = get_attachments(comp),
                                                action = get_action(comp)
                                                )

