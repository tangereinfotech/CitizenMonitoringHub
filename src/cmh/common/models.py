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

class Category(models.Model):
    key   = models.CharField (max_length = 1000)
    parent = models.ForeignKey ('Category', blank = True, null = True)

class Attribute (models.Model):
    value    = models.CharField (max_length = 1000)
    parents  = models.ManyToManyField ('Attribute')
    category = models.ForeignKey ('Category')

    def __unicode__ (self):
        return "%s [%s]" % (self.value, self.category.key)

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


class LatLong (models.Model):
    location = models.ForeignKey (Attribute)
    latitude = models.FloatField ()
    longitude = models.FloatField ()

