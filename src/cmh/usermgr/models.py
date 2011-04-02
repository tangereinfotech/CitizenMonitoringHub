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

from django.db import models
from django.contrib.auth.models import User
from cmh.common.models import Attribute, Category
import sys, traceback

# Create your models here.
class Location(models.Model):
    address     = models.CharField(max_length=100,blank=True,null=True)
    town        = models.CharField(max_length=20)
    district    = models.CharField(max_length=20)
    state       = models.CharField(max_length=20)
    pincode     = models.IntegerField()
    latdegree   = models.IntegerField(blank=True,null=True)
    latmin      = models.IntegerField(blank=True,null=True)
    latsec      = models.IntegerField(blank=True,null=True)
    latdir      = models.CharField(max_length=1,blank=True,null=True)
    londegree   = models.IntegerField(blank=True,null=True)
    lonmin      = models.IntegerField(blank=True,null=True)
    lonsec      = models.IntegerField(blank=True,null=True)
    londir      = models.CharField(max_length=1,blank=True,null=True)

    def __unicode__(self):
        return self.town

    class Meta:
        ordering = ['pincode']

class Citizen(models.Model):
    fname       = models.CharField(max_length=30)
    lname       = models.CharField(max_length=30)
    #location    = models.ForeignKey(Location)
    mobile      = models.IntegerField(blank=True,null=True)
    phone       = models.IntegerField(blank=True,null=True)
    email       = models.EmailField(blank=True,null=True)
    user        = models.OneToOneField(User,blank=True,null=True)

    def __unicode__(self):
        return u'%s %s' % (self.fname, self.lname)

    class Meta:
        ordering = ['fname']

class Official(models.Model):
    designation = models.CharField (max_length = 200, blank = True, null = True)
    fname       = models.CharField (max_length=30)
    lname       = models.CharField (max_length=30)
    location    = models.ForeignKey (Location)
    mobile      = models.CharField (max_length=15, blank=True,null=True)
    phone       = models.CharField (max_length=15, blank=True,null=True)
    email       = models.EmailField (blank=True,null=True)
    superivor   = models.ForeignKey ('Official', blank=True, null=True)
    user        = models.OneToOneField (User)
    department  = models.ForeignKey (Attribute)
    def __unicode__(self):
        return u'%s %s' % (self.fname, self.lname)

    def getSuperivor(self):
        return self.superivor

    class Meta:
        ordering = ['fname']


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



