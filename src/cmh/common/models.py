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

class CodeName (models.Model):
    code = models.CharField (max_length = 100)
    name = models.CharField (max_length = 500)

    class Meta:
        abstract = True



