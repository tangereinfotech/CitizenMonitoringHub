# encoding: utf-8
# Copyright 2011, Tangere Infotech Pvt Ltd [http://tangere.in]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django import forms
from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.db.models import Q

from django.utils.translation import ugettext as _
from cmh.usermgr.utils import get_user_menus

from cmh.common.models import ComplaintType, ComplaintDepartment
from cmh.common.constants import DeployDistrict

from cmh.issuemgr.models import Complaint

from cmh.issuemgr.forms import DateIndex

def index (request):
    if request.method == 'GET':
        departments = ComplaintDepartment.objects.all ()
        request.session ['blkids']  = ""
        request.session ['villids'] = ""
        request.session ['gpids']   = ""
        request.session ['depids']  = ""
        init_lattd = DeployDistrict.DISTRICT.lattd
        init_longd = DeployDistrict.DISTRICT.longd
        return render_to_response ('index.html',
                                   {'menus' : get_user_menus (request.user,index),
                                    'user'  : request.user,
                                    'form'  : DateIndex(),
                                    'map'   : {'center_lat' : init_lattd,
                                               'center_long' : init_longd},
                                    'departments' : departments})
    elif request.method == 'POST':
        form = SaveMapDataForm (request.POST)
        if form.is_valid ():
            loctype = form.cleaned_data ['loctype']
            locid = form.cleaned_data ['locid']

            session_var = {'Block' : 'blkids',
                           'gramp' : 'gpids',
                           'Village' : 'villids'} [loctype]
            session_data = request.session [session_var]
            session_data = session_data.strip ()

            if len (session_data) == 0:
                request.session [session_var] = "%d" % (locid)
            else:
                sdata = session_data.split (',')
                sdata.append ("%d" % (locid))
                request.session [session_var] = ",".join (set (sdata))
        else:
            pass
        return HttpResponse ("")
    else:
        return HttpResponseRedirect ('/')

def aboutus (request):
    return render_to_response ('aboutus.html', {'menus' : get_user_menus (request.user,index),
                                                'user' : request.user},)


class SaveMapDataForm (forms.Form):
    loctype = forms.ChoiceField (choices = ((_('Block'), _('Block')),
                                            (_('gramp'), _('Gram Panchayat')),
                                            (_('Village'), _('Village'))))
    locid   = forms.IntegerField ()
