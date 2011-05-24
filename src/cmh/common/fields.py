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

import re
from django import forms
from django.contrib.auth.models import User


class StripCharField (forms.CharField):
    def clean (self, value):
        value = super (StripCharField, self).clean (value)
        if value != None:
            return value.strip ()
        else:
            return ''

class UsernameField (forms.CharField):
    def __init__ (self, check = True, *args, **kwargs):
        self.check = check
        super (UsernameField, self).__init__ (*args, **kwargs)

    def clean (self, value):
        value = super (UsernameField, self).clean (value)
        if self.check:
            if User.objects.filter (username = value).count () != 0:
                raise forms.ValidationError ("Username is already registered")
        return value


class PhoneNumberField (forms.CharField):
    def __init__ (self, *args, **kwargs):
        super (PhoneNumberField, self).__init__ (*args, **kwargs)

    def clean (self, value):
        value = super (PhoneNumberField, self).clean (value)
        if value != None:
            value = value.strip ()
            if re.match (r'^(\+91)?[1-9][0-9]{9}$', value) == None:
                raise forms.ValidationError ("Please enter a valid Indian " +
                                             "phone number")
            return value
        else:
            return ''

class DefaultChoiceField (forms.ChoiceField):
    def __init__ (self, *args, **kwargs):
        if 'choices' in kwargs:
            kwargs ['choices'].insert (0, ('-1', '----'))
        else:
            kwargs ['choices'] = [('-1', '----')]
        super (DefaultChoiceField, self).__init__ (*args, **kwargs)


class SpacedSelectInput (forms.Select):
    def __init__ (self, *args, **kwargs):
        if 'attrs' in kwargs:
            kwargs ['attrs'].update ({'style' : 'width:100%'})
        else:
            kwargs ['attrs'] = {'style' : 'width:100%'}
        super (SpacedSelectInput, self).__init__ (*args, **kwargs)

class SpacedTextInput (forms.TextInput):
    def __init__ (self, *args, **kwargs):
        if 'attrs' in kwargs:
            kwargs ['attrs'].update ({'style' : 'width:100%'})
        else:
            kwargs ['attrs'] = {'style' : 'width:100%'}
        super (SpacedTextInput, self).__init__ (*args, **kwargs)

class AutoCompleteOffTextInput (SpacedTextInput):
    def __init__ (self, *args, **kwargs):
        if 'attrs' in kwargs:
            kwargs ['attrs'].update ({'autocomplete' : 'off'})
        else:
            kwargs ['attrs'] = {'autocomplete' : 'off', 'style' : 'width:100%'}
        super (AutoCompleteOffTextInput, self).__init__ (*args, **kwargs)

