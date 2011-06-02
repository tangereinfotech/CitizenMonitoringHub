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

import math

from django.core.management.base import NoArgsCommand

from cmh.common.models import Village, GramPanchayat, Block
from cmh.common.models import District, State, Country

class Command (NoArgsCommand):
    def handle (self, *args, **kwargs):
        for gp in GramPanchayat.objects.all ():
            latlongs = [(villg.lattd, villg.longd) for villg in gp.village_set.all ()]
            (lat, lon) = self.find_geo_center (latlongs)
            gp.lattd = lat
            gp.longd = lon
            gp.save ()

        for block in Block.objects.all ():
            latlongs = [(gp.lattd, gp.longd) for gp in block.grampanchayat_set.all ()]
            (lat, lon) = self.find_geo_center (latlongs)
            block.lattd = lat
            block.longd = lon
            block.save ()

        for distt in District.objects.all ():
            latlongs = [(block.lattd, block.longd) for gp in distt.block_set.all ()]
            (lat, lon) = self.find_geo_center (latlongs)
            distt.lattd = lat
            distt.longd = lon
            distt.save ()

        for state in State.objects.all ():
            latlongs = [(distt.lattd, distt.longd) for gp in state.district_set.all ()]
            (lat, lon) = self.find_geo_center (latlongs)
            state.lattd = lat
            state.longd = lon
            state.save ()

        for country in Country.objects.all ():
            latlongs = [(state.lattd, state.longd) for gp in country.state_set.all ()]
            (lat, lon) = self.find_geo_center (latlongs)
            country.lattd = lat
            country.longd = lon
            country.save ()



    def find_geo_center (self, latlongs):
        latav = sum (filter (lambda (x): x < 90,
                             [lat for lat, lon in latlongs])) /len (latlongs)
        lonav = sum (filter (lambda (x): x < 90,
                             [lon for lat, lon in latlongs]))/len (latlongs)

        return (latav, lonav)

