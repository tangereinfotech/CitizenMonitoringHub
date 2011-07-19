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

from cmh.smsgateway.models import TextMessage
from cmh.common.utils import debug

def queue_complaint_update_sms (mobile, complaint_message, complaint):
    if len (complaint_message.strip ()) != 0:
        complaint_message = complaint_message.replace ('____', complaint.complaintno)
        TextMessage.objects.queue_text_message (mobile, complaint_message)
        debug ("Queued message [[%s]] for mobile [%s]" %
               (complaint_message, str (mobile)))
    else:
        debug ("Message empty - so not queueing")


def queue_sms (mobile, message):
    debug ("Queueing message [[%s]] for mobile [%s]" % (message, str (mobile)))
    TextMessage.objects.queue_text_message (mobile, message)


