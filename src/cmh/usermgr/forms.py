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

class ProfileEditForm (forms.Form):
    name     = forms.CharField(max_length= 200, label="NAME")
    phone    = PhoneNumberField (label="PHONE NUMBER")
    username = forms.CharField(max_length= 200, label="USER NAME", required="false")


class PasswordUpdateForm(forms.Form):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    oldpassword = forms.CharField(label="Old password", widget=forms.PasswordInput, required = True)
    newpassword1 = forms.CharField(label="New password", widget=forms.PasswordInput, required = True)
    newpassword2 = forms.CharField(label="New password (Confirm)", widget=forms.PasswordInput, required = True)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordUpdateForm, self).__init__(*args, **kwargs)
