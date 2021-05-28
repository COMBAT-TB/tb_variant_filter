# Copyright (C) 2019  Peter van Heusden <pvh@sanbi.ac.za>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from .. import Location, doc_inherit
from io import StringIO
import pandas as pd
from py2neo import Graph
import requests

from ..region_list import RegionList


class TBProfilerRegions(RegionList):
    url = "https://raw.githubusercontent.com/jodyphelan/TBProfiler/master/db/tbdb.bed"
    name = "TBProfiler"
    description = "TBProfiler resistance genes"
    project_url = "https://github.com/jodyphelan/TBProfiler"
    regions = [
Location(locus='Rv0005', start=4998, end=7267, strand=1),
        Location(locus='Rv0006', start=7268, end=9818, strand=1),
        Location(locus='Rv0407', start=490706, end=491785, strand=1),
        Location(locus='Rv0486', start=575301, end=576786, strand=1),
        Location(locus='Rv0667', start=759310, end=763325, strand=1),
        Location(locus='Rv0668', start=763326, end=767320, strand=1),
        Location(locus='Rv0678', start=778906, end=779487, strand=1),
        Location(locus='Rv0682', start=781312, end=781933, strand=1),
        Location(locus='Rv0701', start=800793, end=801461, strand=1),
        Location(locus='Rv1173', start=1302682, end=1305501, strand=1),
        Location(locus='Rv1267c', start=1416181, end=1417657, strand=1),
        Location(locus='Rv1305', start=1460997, end=1461290, strand=1),
        Location(locus='rrs', start=1471743, end=1473382, strand=1),
        Location(locus='rrl', start=1473383, end=1476795, strand=1),
        Location(locus='Rv1483', start=1673300, end=1674183, strand=1),
        Location(locus='Rv1484', start=1674184, end=1675011, strand=1),
        Location(locus='Rv1630', start=1833380, end=1834987, strand=1),
        Location(locus='Rv1694', start=1917933, end=1918745, strand=1),
        Location(locus='Rv1908c', start=2153889, end=2156148, strand=1),
        Location(locus='Rv2043c', start=2288682, end=2289281, strand=1),
        Location(locus='Rv2245', start=2518115, end=2519365, strand=1),
        Location(locus='Rv2416c', start=2714124, end=2715471, strand=1),
        Location(locus='Rv2428', start=2726088, end=2726780, strand=1),
        Location(locus='Rv2447c', start=2746139, end=2747594, strand=1),
        Location(locus='Rv2535c', start=2859300, end=2860418, strand=1),
        Location(locus='Rv2671', start=2986841, end=2987615, strand=1),
        Location(locus='Rv2754c', start=3067193, end=3068188, strand=1),
        Location(locus='Rv2764c', start=3073680, end=3074471, strand=1),
        Location(locus='Rv2780', start=3086755, end=3087935, strand=1),
        Location(locus='Rv2983', start=3339000, end=3339762, strand=1),
        Location(locus='Rv3261', start=3640142, end=3641538, strand=1),
        Location(locus='Rv3262', start=3641539, end=3642881, strand=1),
        Location(locus='Rv3423c', start=3840198, end=3841713, strand=1),
        Location(locus='Rv3547', start=3986733, end=3987299, strand=1),
        Location(locus='Rv3601c', start=4043862, end=4044280, strand=1),
        Location(locus='Rv3793', start=4239864, end=4243147, strand=1),
        Location(locus='Rv3794', start=4243148, end=4246513, strand=1),
        Location(locus='Rv3795', start=4246514, end=4249810, strand=1),
        Location(locus='Rv3806c', start=4268925, end=4269839, strand=1),
        Location(locus='Rv3854c', start=4326004, end=4327548, strand=1),
        Location(locus='Rv3855', start=4327549, end=4328199, strand=1),
        Location(locus='Rv3919c', start=4407528, end=4408333, strand=1),
    ]

    @doc_inherit
    def load_from_web_and_db(self, bolt_url: str):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = pd.read_csv(
                StringIO(response.text),
                delimiter="\t",
                names=["Chromosome", "start", "end", "locus", "name", "resistance"],
            )
            graph = Graph(uri=bolt_url)
            self.regions = RegionList.locus_list_to_locations(graph, data, "locus")
