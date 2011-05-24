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

class Location (models.Model):
    code = models.CharField (max_length = 200)
    name = models.CharField (max_length = 2000)
    lattd = models.FloatField (blank = True, null = True)
    longd = models.FloatField (blank = True, null = True)

    class Meta:
        abstract = True

class Country (Location):
    pass

class State (Location):
    country = models.ForeignKey (Country)

class District (Location):
    state = models.ForeignKey (State)

class Block (Location):
    district = models.ForeignKey (District)

class GramPanchayat (Location):
    block = models.ForeignKey (Block)

class Village (Location):
    grampanchayat = models.ForeignKey (GramPanchayat)
    search = models.CharField (max_length = 5000)

class ComplaintDepartment (models.Model):
    code = models.CharField (max_length = 200)
    name = models.CharField (max_length = 5000)
    district = models.ForeignKey (District)

class ComplaintType (models.Model):
    code = models.CharField (max_length = 200)
    summary = models.CharField (max_length = 2000)
    department = models.ForeignKey (ComplaintDepartment)
    cclass = models.CharField (max_length = 500, blank = True, null = True)
    defsmsnew = models.CharField (max_length = 2000, blank = True, null = True)
    defsmsack = models.CharField (max_length = 2000, blank = True, null = True)
    defsmsopen = models.CharField (max_length = 2000, blank = True, null = True)
    defsmsres  = models.CharField (max_length = 2000, blank = True, null = True)
    defsmsclo = models.CharField (max_length = 2000, blank = True, null = True)
    official = models.ForeignKey (Official, blank = True, null = True)




class Category(models.Model):
    key   = models.CharField (max_length = 1000)
    parent = models.ForeignKey ('Category', blank = True, null = True)

class Attribute (models.Model):
    value    = models.CharField (max_length = 1000)
    parent   = models.ForeignKey ('Attribute', blank = True, null = True)
    category = models.ForeignKey ('Category')

    def __unicode__ (self):
        return "%s [%s]" % (self.value, self.category.key)

    def _get_descendents (self):
        children = self.attribute_set.all ()
        if children.count () == 0:
            return children
        else:
            retchildren = children
            for child in children:
                retchildren = retchildren | child._get_descendents ()
            return retchildren

    def get_descendents (self):
        return self._get_descendents ()

    def get_children (self):
        return self.attribute_set.all ()

    def get_category_descendents (self, category):
        return self.get_descendents ().filter (category__key = category)

    def get_value (self):
        return self.value

class CodeName (models.Model):
    code = models.CharField (max_length = 100, unique = True)
    name = models.CharField (max_length = 500)

codenames = CodeName.objects.all ()
def get_code2name (code):
    try:
        return codenames.get (code = code).name
    except CodeName.DoesNotExist:
        return '----'

def get_child_attributes (str_category, str_attribute):
    try:
        parent_attribute = Attribute.objects.get (category__key = str_category,
                                                  value = str_attribute)
        return parent_attribute.attribute_set.all ()
    except Attribute.DoesNotExist:
        return models.Q ()
