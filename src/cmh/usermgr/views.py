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
                        return render_to_response ('loggedinbase.html', {'user' : user})
            except Exception, e:
                pass

        return render_to_response ('login.html', {'form': form,})
    else:
        return render_to_response ('login.html', {'form': form})



def dologout (request):
    logout (request)
    return HttpResponseRedirect (settings.LOGIN_URL)


# def doregister (request,form_class=UserLoginForm):
#     form = UserRegisterForm ()
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data ['username']
#             password = form.cleaned_data ['password']
#             repassword = form.cleaned_data ['repassword']
#             fname = form.cleaned_data['fname']
#             lname = form.cleaned_data['lname']
#             mobile  = form.cleaned_data['mobile']
#             email  = form.cleaned_data['email']
#             phone  = form.cleaned_data['phone']
#             street  = form.cleaned_data['streetaddress']
#             town  = form.cleaned_data['town']
#             district  = form.cleaned_data['district']
#             state  = form.cleaned_data['state']
#             pincode  = form.cleaned_data['pincode']

#             try:
#                 if username == None or len (username.strip ()) == 0:
#                     return HttpResponse(" Error Username is wrong")
#                 else:
#                     username = username.strip ()

#                 if email != None and len (email.strip ()) != 0:
#                     email = email.strip ()
#                     if check_email (email) == False:
#                         return HttpResponse("Error Wrong Email format")
#                 else:
#                     email = None

#                 try:
#                     user = User.objects.get (username = username)
#                     return HttpResponse("User name already exists")
#                 except User.DoesNotExist:
#                     pass

#                 if (password.__ne__(repassword)):
#                     return HttpResponse("Both password don't match")
#                 else:
#                     pass

#                 try:
#                      (user) = createuser( request = request,
#                                           username = username,
#                                           fname = fname,
#                                           lname = lname,
#                                           password = password,
#                                           email = email,
#                                           phone = phone,
#                                           mobile = mobile,
#                                           superivor = None,
#                                           street = street,
#                                           town =town,
#                                           district = district,
#                                           state = state,
#                                           pincode = pincode
#                                          )
#                      return HttpResponse("User is added in the database")

#                 except Exception:
#                     import traceback
#                     traceback.print_exc()
#                     pass


#             except Exception:
#                 pass

#             return render_to_response ('register.html', {'form': form,})
#         else:
#             return render_to_response ('register.html', {'form': form,})
#     else:
#         return render_to_response ('register.html', {'form': form})
