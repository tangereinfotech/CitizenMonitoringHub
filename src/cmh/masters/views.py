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

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import simplejson as json

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from cmh.usermgr.models import CmhUser, Official
from cmh.usermgr.utils import get_user_menus
from cmh.usermgr.constants import UserRoles

from cmh.common.models import ComplaintDepartment
from cmh.common.utils import debug

from cmh.masters.forms import AddCSOMember, RegisterDM, DmId, EditDM
from cmh.masters.forms import AddEditOfficial, DepartmentSelected

@login_required
def masters (request):
    # Ensure CmhUser model instance exists for all User's
    for user in User.objects.filter (cmhuser = None):
        cmhuser = CmhUser.objects.create (user = user)

    cmhusers = CmhUser.objects.all ()

    paginator = Paginator (cmhusers, 10)

    try:
        page = int (request.GET.get ('page', '1'))
    except ValueError:
        page = 1

    try:
        cmhusers = paginator.page (page)
    except (EmptyPage, InvalidPage):
        cmhusers = paginator.page (paginator.num_pages)

    return render_to_response ("masters.html",
                               {'menus' : get_user_menus (request.user,masters),
                                'cmhusers' : cmhusers,
                                'user' : request.user})

@login_required
def process_dm (request):
    cmhuser_dm = CmhUser.objects.filter (user__approle__role = UserRoles.DM)
    if request.method == 'GET':
        if cmhuser_dm.count () == 0:
            return render_to_response ('create_dm.html',
                                       {'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user,
                                        'form' : RegisterDM ()})
        elif cmhuser_dm.count () == 1:
            return render_to_response ('view_dm.html',
                                       {'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user,
                                        'dm' : cmhuser_dm [0]})
        else:
            return render_to_response ('error_dm_count.html',
                                       {'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
    elif request.method == 'POST':
        if 'register' in request.POST: # Registering a new DM
            form = RegisterDM (request.POST)
            if form.is_valid ():
                dm = form.save ()
                return render_to_response ('view_dm.html',
                                           {'menus' : get_user_menus (request.user,process_dm),
                                            'user' : request.user,
                                            'dm' : dm})
            else:
                return render_to_response ('create_dm.html',
                                           {'menus' : get_user_menus (request.user,process_dm),
                                            'user' : request.user,
                                            'form' : form})
        elif 'cancel' in request.POST: # Cancel DM registration
            return HttpResponseRedirect (reverse (masters))
        elif 'edit_dm' in request.POST: # Edit DM record
            form = DmId (request.POST)
            if form.is_valid ():
                dmid = form.cleaned_data ['dmid']
                try:
                    dm = CmhUser.objects.get (user__approle__role = UserRoles.DM,
                                              id = dmid)
                    formdata = {'dmid' : dm.id,
                                'username' : dm.user.username,
                                'name' : dm.user.get_full_name (),
                                'phone' : dm.phone}
                    form = EditDM (formdata)
                    return render_to_response ('edit_dm.html',
                                               {'menus':get_user_menus(request.user,process_dm),
                                                'user' : request.user,
                                                'form' : form})
                except CmhUser.DoesNotExist, CmhUser.MultipleObjectsReturned:
                    return HttpResponse (reverse (masters))
        elif 'reset_dm' in request.POST:
            # FIXME: Point to send new password through SMS
            return HttpResponse ('Reset Password not implemented')
        elif 'edit_save' in request.POST:
            debug ("Saving a DM object")
            form = EditDM (request.POST)
            if form.is_valid ():
                try:
                    dmid = form.cleaned_data ['dmid']
                    dm = CmhUser.objects.get (user__approle__role = UserRoles.DM,
                                              id = dmid)
                    user = dm.user
                    user.first_name = form.cleaned_data ['name']
                    user.set_password ('123') # FIXME: Send password after saving the CmhUser object
                    user.save ()

                    dm.phone = form.cleaned_data ['phone']
                    dm.save ()
                    return HttpResponseRedirect (reverse (process_dm))
                except CmhUser.DoesNotExist:
                    return render_to_response ('error.html',
                                               {'error' : "Invalid DM Object",
                                                'menus' : get_user_menus (request.user,process_dm),
                                                'user' : request.user})
                except CmhUser.MultipleObjectsReturned:
                    return render_to_response ('error.html',
                                               {'error' : "DM is not a singleton",
                                                'menus' : get_user_menus (request.user,process_dm),
                                                'user' : request.user})
                except:
                    import traceback
                    traceback.print_exc ()
            else:
                debug ("Invalid form:" , form.errors)
                return render_to_response ('edit_dm.html',
                                           {'menus': get_user_menus(request.user,process_dm),
                                            'user' : request.user,
                                            'form' : form})
        elif 'edit_cancel' in request.POST:
            return HttpResponseRedirect (reverse (process_dm))
        else:
            return HttpResponseRedirect (reverse (masters))
    else:
        return HttpResponseRedirect (reverse (masters))

@login_required
def officials (request):
    if request.method == 'GET':
        query = (Q (user__approle__role = UserRoles.OFFICIAL) |
                 Q (user__approle__role = UserRoles.DELEGATE))
        cmhusers = CmhUser.objects.filter (query)
        paginator = Paginator (cmhusers, 10)

        try:
            page = int (request.GET.get ('page', '1'))
        except ValueError:
            page = 1

        try:
            cmhusers = paginator.page (page)
        except (EmptyPage, InvalidPage):
            cmhusers = paginator.page (paginator.num_pages)

        return render_to_response ('officials.html',
                                   {'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user,
                                    'cmhusers' : cmhusers})
    else:
        return render_to_response ('error.html',
                                   {'error': 'No other method is supported',
                                    'menus' : get_user_menus (request.user,process_dm),
                                    'user' : request.user})

@login_required
def add_official (request):
    cmhuser_dm = CmhUser.objects.filter (user__approle__role = UserRoles.DM)
    if request.method == 'GET':
        if cmhuser_dm.count () == 0:
            return render_to_response ('error.html',
                                       {'error' : 'District Magistrate must be registered',
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
        elif cmhuser_dm.count () > 1:
            return render_to_response ('error.html',
                                       {'error' : 'Multiple DMs defined [%d]',
                                        'menus' : get_user_menus (request.user,process_dm),
                                        'user' : request.user})
        else:
            departments = ComplaintDepartment.objects.all ()
            return render_to_response ('add_official.html',
                                          {'menus' : get_user_menus (request.user,process_dm),
                                           'user' : request.user,
                                           'form' : AddEditOfficial (departments = departments)})
    elif request.method == 'POST':
        if 'add_add_official' in request.POST:
            if 'pos_supervisors' in request.session:
                supervisors = json.loads (request.session ['pos_supervisors'])
            departments = ComplaintDepartment.objects.all ()
            form = AddEditOfficial (request.POST,
                                    departments = departments,
                                    supervisors = supervisors)

            if form.is_valid ():
                form.save ()
                return HttpResponseRedirect (reverse (officials))
            else:
                return render_to_response ('add_official.html',
                                           {'menus' : get_user_menus (request.user,process_dm),
                                            'user' : request.user,
                                            'form' : form})
        elif 'add_cancel_official' in request.POST:
            return HttpResponseRedirect (reverse (officials))
        else:
            return HttpResponseRedirect (reverse (officials))

    else:
        return HttpResponseRedirect (reverse (officials))


@login_required
def department_selected (request):
    form = DepartmentSelected (request.GET)
    if form.is_valid ():
        debug (form)
        try:
            dept_id = form.cleaned_data ['department']
            supervisors = Official.objects.filter (departments__id = dept_id,
                                                   supervisor = None)
            sups = [(supervisor.id, supervisor.user.cmhuser.get_desc_name ())
                    for supervisor in supervisors]
            sups.insert (0, ('-1', '----'))
            serialized = json.dumps (sups)
            request.session ['pos_supervisors'] = serialized
            return HttpResponse (serialized)
        except:
            return HttpResponse ([])
    else:
        return HttpResponse ([])


@login_required
def csomembers (request):
    cmhusers = CmhUser.objects.filter (user__approle__role = UserRoles.CSO)

    paginator = Paginator (cmhusers, 10)

    try:
        page = int (request.GET.get ('page', '1'))
    except ValueError:
        page = 1

    try:
        cmhusers = paginator.page (page)
    except (EmptyPage, InvalidPage):
        cmhusers = paginator.page (paginator.num_pages)

    return render_to_response ("cso_master.html",
                               {'menus' : get_user_menus (request.user,csomembers),
                                'cmhusers' : cmhusers,
                                'user' : request.user})



@login_required
def add_cso_user (request):
    if request.method == 'GET':
        return render_to_response ('add_cso_member.html',
                                   {'menus' : get_user_menus (request.user,add_cso_user),
                                    'user' : request.user,
                                    'form' : AddCSOMember ()})
    elif request.method == 'POST':
        form = AddCSOMember (request.POST)
        if 'add' in request.POST:
            if form.is_valid ():
                form.save ()
                return HttpResponseRedirect (reverse (csomembers))
            else:
                return render_to_response ('add_cso_member.html',
                                           {'menus' : get_user_menus (request.user,add_cso_user),
                                            'user' : request.user,
                                            'form' : form})
        else:
            return HttpResponseRedirect (reverse (csomembers))
    else:
        return HttpResponseRedirect ("/")
