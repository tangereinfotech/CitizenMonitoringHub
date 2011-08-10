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

import urllib
import urllib2

params = urllib.urlencode({'from' : '9980836967', 'secret' : '0123456789', 'message' : '5.3.3 Apurva This is a complaint'})
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
req = urllib2.Request ("http://localhost:8000/smsg/", params, headers)
response = urllib2.urlopen (req)
print response.read ()
