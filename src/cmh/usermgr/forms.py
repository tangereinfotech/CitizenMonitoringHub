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

from cmh.common.fields import PhoneNumberField

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _

from cmh.captcha.fields import CaptchaField
import re

class UserLoginForm (forms.Form):
    username = forms.CharField(label=_("Username"),
                               max_length=30,
                               widget=forms.TextInput (attrs = {'tabindex' : '1'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput (attrs = {'tabindex' : '2'}))
    def clean (self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            username = self.cleaned_data ['username']
            password = self.cleaned_data ['password']
            user = authenticate (username = username, password = password)
            if user is None:
                if User.objects.filter (username = username).count () != 0:
                    raise forms.ValidationError (_('Username / Password does not match'))
                else:
                    raise forms.ValidationError (_('Username is not registered'))
            elif user.is_active == False:
                raise forms.ValidationError (_('Account  suspended. Contact Administrator'))
        self.valid_user = user
        return self.cleaned_data

class UserRegisterForm(forms.Form):
    username        = forms.CharField(label=_("username"), max_length=30)
    password        = forms.CharField(label=_("password"), widget=forms.PasswordInput)
    repassword      = forms.CharField(label=_("repassword"), widget=forms.PasswordInput)
    fname           = forms.CharField(label=_("fname"), max_length=30)
    lname           = forms.CharField(label=_("lname"), max_length=30)
    streetaddress   = forms.CharField(label=_("streetaddress"), max_length=100)
    town            = forms.CharField(label=_("town"), max_length=50)
    district        = forms.CharField(label=_("district"), max_length=50)
    state           = forms.CharField(label=_("state"), max_length=50)
    pincode         = forms.IntegerField(label=_("pincode"))
    phone           = forms.CharField(label=_("phone")  ,max_length=15)
    mobile          = forms.CharField(label=_("mobile") ,max_length=15)
    email           = forms.EmailField(label=_("email"))
    captcha  = CaptchaField()

    def clean_username(self):
        username = self.cleaned_data['username']
        if (re.match('^([a-zA-Z_0-9]|[_.])+$',username) !=None):
            try:
                user = User.objects.get(username=username)
                raise forms.ValidationError(_("Username already Exist"))
            except User.DoesNotExist:
                return username
        else:
            raise forms.ValidationError(_("Username format is invalid"))


    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if (re.match('^\+?\d{4,15}$',mobile) !=None):
            return mobile
        else:
            raise forms.ValidationError(_("Mobile number format is invalid"))

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if (re.match('^\+?\d{4,15}$',phone) !=None):
            return phone
        else:
            raise forms.ValidationError(_("Phone number format is invalid"))

class ProfileEditForm (forms.Form):
    name     = forms.CharField(max_length= 200)
    phone    = PhoneNumberField ()
    username = forms.CharField(max_length= 200, required="false")


class PasswordUpdateForm(forms.Form):
    oldpassword = forms.CharField (label=_("Old password:"), widget=forms.PasswordInput)
    newpassword1 = forms.CharField (label=_("New password:"), widget=forms.PasswordInput)
    newpassword2 = forms.CharField (label=_("Confirm Password:"), widget=forms.PasswordInput)

    def __init__ (self, user, *args, **kwargs):
        self.user = user
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)

    def clean_oldpassword (self):
        if self.user.check_password (self.cleaned_data ['oldpassword']) == False:
            raise forms.ValidationError (_("Old password is wrong"))
        return self.cleaned_data ['oldpassword']

    def clean_newpassword2 (self):
        np1 = self.cleaned_data ['newpassword1']
        np2 = self.cleaned_data ['newpassword2']

        if np1 != np2:
            raise forms.ValidationError (_("Passwords do not match"))

        return np2

    def save (self):
        self.user.set_password (self.cleaned_data ['newpassword1'])
        self.user.save ()
        return self.user
