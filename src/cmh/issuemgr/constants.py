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

STATUS_NEW      = ComplaintStatus.objects.get (name = 'New')
STATUS_REOPEN   = ComplaintStatus.objects.get (name = 'Reopened')
STATUS_ACK      = ComplaintStatus.objects.get (name = 'Acknowledged')
STATUS_OPEN     = ComplaintStatus.objects.get (name = 'Open')
STATUS_RESOLVED = ComplaintStatus.objects.get (name = 'Resolved')
STATUS_CLOSED   = ComplaintStatus.objects.get (name = 'Closed')

class HotComplaintPeriod:
    WEEK    = 1
    MONTH   = 2
    QUARTER = 3


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Unspecified','Unspecified')
)

COMMUNITY_CHOICES = (
    ('SC/ST', 'SC / ST'),
    ('Others','Others'),
    ('Unspecified','Unspecified')
)
