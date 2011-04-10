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

import sys, traceback
from django.db import models
from django.contrib.auth.models import User
from cmh.common.models import Attribute, Category, CodeName

class Citizen(models.Model):
    user        = models.OneToOneField(User,blank=True,null=True)
    mobile      = models.IntegerField(blank=True,null=True)

    def __unicode__(self):
        return "Citizen: " + self.user.username

class Department (CodeName):
    pass

class Official(models.Model):
    user        = models.OneToOneField (User)
    designation = models.CharField (max_length = 200, blank = True, null = True)
    supervisor  = models.ForeignKey ('Official', blank=True, null=True)
    location    = models.ForeignKey (Attribute, related_name = 'location')
    mobile      = models.CharField (max_length=15, blank=True,null=True)
    department  = models.ManyToManyField (Department)

    def __unicode__(self):
        return u'Official: ' + self.user.username


def createuser(request, username, fname, lname, password, email, phone, mobile, superivor, street, town,district, state, pincode):
    try:
        user = User.objects.get(username = username)
        sys.stderr.write ("User already exists: " + username + "\n")
    except User.DoesNotExist:
        user = User.objects.create (username=username, password=password, is_active = False)
        loc = Location.objects.create(address=street,town=town,district=district,state=state,pincode=pincode)
        Official.objects.create(fname=fname, lname=lname,email=email,mobile=mobile, phone=phone,superivor=superivor,user=user, location=loc)

    return (user)


def createlocation(request, street, town,district, state, pincode):

    try:
        loc = Location.objects.create(address=street,town=town,district=district,state=state,pincode=pincode)

    except Exception:
        sys.stderr.write("Unable to create location")

    return (loc)



