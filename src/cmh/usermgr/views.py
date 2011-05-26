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
from django.shortcuts import render_to_response

from cmh.common.utils import check_email, check_phone, check_mobile
from cmh.usermgr.form import UserLoginForm, UserRegisterForm
# from cmh.usermgr.models import createuser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from cmh.usermgr.utils import get_user_menus
from cmh.common.utils import debug

def dologin (request):
    form = UserLoginForm ()
    if request.method == 'POST':
        form = UserLoginForm (request.POST)
        if form.is_valid ():
            username = form.cleaned_data ['username']
            password = form.cleaned_data ['password']
            try:
                user = authenticate(username=username, password=password)

                if user is not None:
                    if user.is_active:
                        login (request, user)
                        request.session.set_expiry (0)
                        return HttpResponseRedirect (settings.LOGIN_REDIRECT_URL)
            except Exception, e:
                pass

        return render_to_response ('login.html',
                                   {'form': form,
                                    'menus' : get_user_menus (request.user),
                                    'user' : request.user})
    else:
        return render_to_response ('login.html',
                                   {'form': form,
                                    'menus' : get_user_menus (request.user),
                                    'user' : request.user})

def dologout (request):
    logout (request)
    return HttpResponseRedirect (settings.LOGIN_REDIRECT_URL)
