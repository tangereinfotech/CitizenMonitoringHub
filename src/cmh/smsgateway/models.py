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

class TextMessageManager (models.Manager):
    def queue_text_message (self, phone, message):
        return TextMessage.objects.create (phone = phone, message = message)

class TextMessage (models.Model):
    phone     = models.CharField (max_length = 20)
    message   = models.CharField (max_length = 500)
    processed = models.BooleanField (default = False)
    created   = models.DateTimeField (auto_now_add = True)
    processed_time = models.DateTimeField(null=True)
    objects = TextMessageManager ()

class ReceivedTextMessage (models.Model):
    sender  = models.CharField (max_length = 20)
    message = models.CharField (max_length = 500)
    valid   = models.NullBooleanField (default = False)
    created = models.DateTimeField (auto_now_add = True)

class IgnoredTextMessage (models.Model):
    sender  = models.CharField (max_length = 20)
    message = models.CharField (max_length = 500)
    valid   = models.NullBooleanField (default = False)
    created = models.DateTimeField (auto_now_add = True)

class SenderBlacklist (models.Model):
    sender = models.CharField (max_length = 20)
