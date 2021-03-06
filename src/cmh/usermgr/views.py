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

import os
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from cmh.common.utils import check_email, check_phone, check_mobile
from cmh.usermgr.forms import ProfileEditForm, UserLoginForm, UserRegisterForm
# from cmh.usermgr.models import createuser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from cmh.usermgr.utils import get_user_menus
from cmh.common.utils import debug
from cmh.usermgr.forms import PasswordUpdateForm


def dologin (request):
    form = UserLoginForm ()
    if request.method == 'POST':
        form = UserLoginForm (request.POST)
        if form.is_valid ():
            login (request, form.valid_user)
            request.session.set_expiry (0)
            return HttpResponseRedirect (settings.LOGIN_REDIRECT_URL)
    return render_to_response ('login.html',
                               {'form': form,
                                'menus' : get_user_menus (request.user, dologin),
                                'user' : request.user})

@login_required
def gotomyprofile (request):
    if request.method=="GET":
        cmhuser = request.user.cmhuser
        return render_to_response('profile.html',
                                {'obj' : cmhuser,
                                 'menus' : get_user_menus (request.user,gotomyprofile),
                                 'user' : request.user})
    elif request.method=="POST":
        if 'edit' in request.POST:
            cmhuser = request.user.cmhuser
            return render_to_response('edit.html',
                                      {'menus'  : get_user_menus (request.user,gotomyprofile),
                                       'user'   : request.user,
                                       'form'   : ProfileEditForm (),
                                       'obj'    : cmhuser})
        elif 'savechanges' in request.POST:
            form = ProfileEditForm (request.POST)
            if form.is_valid ():
                user    = request.user
                cmhuser = user.cmhuser

                user.first_name = request.POST ['name']
                user.save ()

                cmhuser.phone = request.POST['phone']
                cmhuser.save()

                return HttpResponseRedirect (reverse (gotomyprofile))
            else:
                cmhuser = request.user.cmhuser
                return render_to_response('edit.html',
                                          {'obj'   : form,
                                           'menus' : get_user_menus (request.user,gotomyprofile),
                                           'user'  : request.user})

        elif 'reset' in request.POST:
            return render_to_response ('reset_password.html',
                                       {'form' : PasswordUpdateForm (request.user),
                                        'menus': get_user_menus (request.user,gotomyprofile),
                                        'user'  : request.user}
                                        )
        elif 'set_password' in request.POST:
            try:
                form = PasswordUpdateForm (request.user,
                                           request.POST)
                if form.is_valid ():
                    form.save ()
                    return render_to_response ('password_reset_success.html',
                                               {'menus': get_user_menus (request.user,gotomyprofile),
                                                'user'  : request.user})

                else:
                    debug ("Form is not valid" + str (form.errors))
                    return render_to_response ('reset_password.html',
                                               {'form' : form,
                                                'menus': get_user_menus (request.user,gotomyprofile),
                                                'user'  : request.user})
            except:
                import traceback
                traceback.print_exc ()
        elif 'cancel' in request.POST:
            return HttpResponseRedirect (reverse (gotomyprofile))


def dologout (request):
    logout (request)
    return HttpResponseRedirect (settings.LOGIN_REDIRECT_URL)

