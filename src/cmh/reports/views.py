from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.utils.simplejson import dumps
from django.utils.translation import ugettext as _
from cmh.issuemgr.models import Complaint, ComplaintEvidence, ComplaintReminder, ComplaintClosureMetric, ComplaintManager
from django.contrib.auth.decorators import login_required
from cmh.usermgr.utils import get_user_menus
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from cmh.reports.report_issues import all_issues_column_properties, report_all_issues_data, report_my_issues_data
from cmh.reports.report_smses import sms_logs_column_properties,report_sms_logs_data
from django.core.urlresolvers import reverse

@login_required
def home(request):
    return render_to_response('report_generic.html', {'cols': all_issues_column_properties, 'data_url': reverse(all_issues_data), 'menus': get_user_menus(request.user, home)}, context_instance = RequestContext(request))

@login_required
def all_issues_data(request):
    return report_all_issues_data(request)

@login_required
def my_issues_data(request):
    return report_my_issues_data(request)

@login_required
def sms_logs_report(request):
    return render_to_response('report_generic.html', {'cols': sms_logs_column_properties, 'data_url': reverse(sms_logs_data), 'menus': get_user_menus(request.user, sms_logs_report)}, context_instance = RequestContext(request))

@login_required
def sms_logs_data(request):
    return report_sms_logs_data(request)

@login_required
def my_issues(request):
    return render_to_response('report_generic.html', {'cols': all_issues_column_properties, 'data_url': reverse(my_issues_data), 'menus': get_user_menus(request.user, my_issues)}, context_instance = RequestContext(request))
