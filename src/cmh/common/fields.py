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
from datetime import datetime, date


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

class SpacedROTextInput (forms.TextInput):
    def __init__ (self, *args, **kwargs):
        if 'attrs' in kwargs:
            kwargs ['attrs'].update ({'style' : 'width:100%', 'readonly' : 'readonly'})
        else:
            kwargs ['attrs'] = {'style' : 'width:100%', 'readonly' : 'readonly'}
        super (SpacedROTextInput, self).__init__ (*args, **kwargs)

class AutoCompleteOffTextInput (SpacedTextInput):
    def __init__ (self, *args, **kwargs):
        if 'attrs' in kwargs:
            kwargs ['attrs'].update ({'autocomplete' : 'off'})
        else:
            kwargs ['attrs'] = {'autocomplete' : 'off', 'style' : 'width:100%'}
        super (AutoCompleteOffTextInput, self).__init__ (*args, **kwargs)

class SpacedTextField (forms.CharField):
    def __init__ (self, *args, **kwargs):
        kwargs ['widget'] = SpacedTextInput ()
        super (SpacedTextField, self).__init__ (*args, **kwargs)

class SpacedROTextField (forms.CharField):
    def __init__ (self, *args, **kwargs):
        kwargs ['widget'] = SpacedROTextInput ()
        super (SpacedROTextField, self).__init__ (*args, **kwargs)


class LatLongField (forms.DecimalField):
    def __init__ (self, *args, **kwargs):
        kwargs ['widget'] = forms.TextInput (attrs = {'style' : 'width: 100%'})
        kwargs ['min_value'] = -180
        kwargs ['max_value'] = 180
        super (LatLongField, self).__init__ (*args, **kwargs)


class MultiNumberIdField (forms.CharField):
    def to_python (self, value):
        if not value: return []
        return [int (x) for x in value.split (',')]

    def validate (self, value_list):
        super (MultiNumberIdField, self).validate (value_list)
        for number in value_list:
            try:
                n = int (number)
            except ValueError:
                raise forms.ValidationError ("Non number in MultiNumberIdField")

class FormattedDateField (forms.CharField):
    def clean (self, value):
        super (FormattedDateField, self).clean (value)
        try:
            (day, month, year) = value.split ('/')
            day = int (day)
            month = int (month)
            year = int (year)

            if (month < 1 and month > 12) or (year < 1970 and year > datetime.now ().year):
                raise forms.ValidationError ("Invalid Date - month / year: " + value)

            days = [31, self.get_feb_days (year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if (day < 1 and day > days [month - 1]):
                raise forms.ValidationError ("Invalid Date - date: " + value)
        except:
            raise forms.ValidationError ("Invalid date - general failure : " + value)
        return self.to_python (value)

    def to_python (self, value):
        (day, month, year) = value.split ('/')
        day = int (day)
        month = int (month)
        year = int (year)
        return date (year, month, day)


    def get_feb_days (self, year):
        if year % 100 == 0:
            if year % 400 == 0: leap = True
            else: leap = False
        else:
            if year % 4 == 0: leap = True
            else: leap = False

        if leap:
            return 29
        else:
            return 28

