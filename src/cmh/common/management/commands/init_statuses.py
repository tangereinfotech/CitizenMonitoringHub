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

from cmh.common.models import ComplaintStatus
from django.core.management.base import NoArgsCommand

class Command (NoArgsCommand):
    def handle (self, *args, **kwargs):
        try:
            ComplaintStatus.objects.get (name = 'New')
        except ComplaintStatus.DoesNotExist:
            ComplaintStatus.objects.create (name = 'New')

        try:
            ComplaintStatus.objects.get (name = 'Reopened')
        except ComplaintStatus.DoesNotExist:
            ComplaintStatus.objects.create (name = 'Reopened')
        try:
            ComplaintStatus.objects.get (name = 'Acknowledged')
        except ComplaintStatus.DoesNotExist:
            ComplaintStatus.objects.create (name = 'Acknowledged')

        try:
            ComplaintStatus.objects.get (name = 'Open')
        except ComplaintStatus.DoesNotExist:
            ComplaintStatus.objects.create (name = 'Open')

        try:
            ComplaintStatus.objects.get (name = 'Resolved')
        except ComplaintStatus.DoesNotExist:
            ComplaintStatus.objects.create (name = 'Resolved')

        try:
            ComplaintStatus.objects.get (name = 'Closed')
        except ComplaintStatus.DoesNotExist:
            ComplaintStatus.objects.create (name = 'Closed')


