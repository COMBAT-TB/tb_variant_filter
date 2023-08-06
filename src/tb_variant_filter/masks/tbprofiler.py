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
from neo4j import GraphDatabase
import requests

from ..region_list import RegionList


class TBProfilerRegions(RegionList):
    url = "https://raw.githubusercontent.com/jodyphelan/TBProfiler/master/db/tbdb.bed"
    name = "TBProfiler"
    description = "TBProfiler resistance genes"
    project_url = "https://github.com/jodyphelan/TBProfiler"
    regions = [       Location(locus='Rv0005', start=5040, end=7467, strand=1),
        Location(locus='Rv0006', start=7102, end=10018, strand=1),
        Location(locus='Rv0407', start=490583, end=491993, strand=1),
        Location(locus='Rv0486', start=575148, end=576990, strand=1),
        Location(locus='Rv0529', start=619691, end=621065, strand=1),
        Location(locus='Rv0667', start=759607, end=763525, strand=1),
        Location(locus='Rv0668', start=763170, end=767520, strand=1),
        Location(locus='Rv0676c', start=775386, end=778680, strand=1),
        Location(locus='Rv0677c', start=778277, end=779105, strand=1),
        Location(locus='Rv0678', start=778790, end=779687, strand=1),
        Location(locus='Rv0682', start=781360, end=782134, strand=1),
        Location(locus='Rv0701', start=800609, end=801662, strand=1),
        Location(locus='Rv1173', start=1302731, end=1305701, strand=1),
        Location(locus='Rv1258c', start=1405881, end=1407540, strand=1),
        Location(locus='Rv1267c', start=1415981, end=1417547, strand=1),
        Location(locus='Rv1305', start=1460845, end=1461490, strand=1),
        Location(locus='rrs', start=1471646, end=1473582, strand=1),
        Location(locus='rrl', start=1473458, end=1476995, strand=1),
        Location(locus='Rv1483', start=1673148, end=1674383, strand=1),
        Location(locus='Rv1484', start=1673848, end=1675211, strand=1),
        Location(locus='Rv1630', start=1833342, end=1835187, strand=1),
        Location(locus='Rv1694', start=1917740, end=1918946, strand=1),
        Location(locus='Rv1854c', start=2101451, end=2103242, strand=1),
        Location(locus='Rv1908c', start=2153689, end=2156570, strand=1),
        Location(locus='Rv1918c', start=2167449, end=2170812, strand=1),
        Location(locus='Rv1979c', start=2221519, end=2223364, strand=1),
        Location(locus='Rv2043c', start=2288481, end=2290323, strand=1),
        Location(locus='Rv2245', start=2517915, end=2519565, strand=1),
        Location(locus='Rv2416c', start=2713924, end=2715586, strand=1),
        Location(locus='Rv2428', start=2725912, end=2726980, strand=1),
        Location(locus='Rv2447c', start=2745935, end=2747798, strand=1),
        Location(locus='Rv2535c', start=2859100, end=2860618, strand=1),
        Location(locus='Rv2671', start=2986639, end=2987815, strand=1),
        Location(locus='Rv2752c', start=3064315, end=3066391, strand=1),
        Location(locus='Rv2754c', start=3066993, end=3068161, strand=1),
        Location(locus='Rv2764c', start=3073480, end=3074671, strand=1),
        Location(locus='Rv2780', start=3086620, end=3088135, strand=1),
        Location(locus='Rv2983', start=3338918, end=3339962, strand=1),
        Location(locus='Rv3083', start=3448304, end=3450191, strand=1),
        Location(locus='Rv3106', start=3473807, end=3475577, strand=1),
        Location(locus='Rv3197A', start=3568201, end=3568879, strand=1),
        Location(locus='Rv3236c', start=3611759, end=3613316, strand=1),
        Location(locus='Rv3261', start=3640343, end=3641738, strand=1),
        Location(locus='Rv3262', start=3641335, end=3643081, strand=1),
        Location(locus='Rv3423c', start=3839994, end=3841620, strand=1),
        Location(locus='Rv3457c', start=3877264, end=3878707, strand=1),
        Location(locus='Rv3547', start=3986644, end=3987499, strand=1),
        Location(locus='Rv3596c', start=4037958, end=4040904, strand=1),
        Location(locus='Rv3601c', start=4043662, end=4044481, strand=1),
        Location(locus='Rv3793', start=4239663, end=4243347, strand=1),
        Location(locus='Rv3794', start=4243004, end=4246717, strand=1),
        Location(locus='Rv3795', start=4246314, end=4250010, strand=1),
        Location(locus='Rv3805c', start=4266753, end=4269036, strand=1),
        Location(locus='Rv3806c', start=4268725, end=4270033, strand=1),
        Location(locus='Rv3854c', start=4325804, end=4330174, strand=1),
        Location(locus='Rv3855', start=4327349, end=4328399, strand=1),
        Location(locus='Rv3862c', start=4337971, end=4338721, strand=1),
        Location(locus='Rv3919c', start=4407328, end=4408476, strand=1)
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
            graph = GraphDatabase.driver(uri=bolt_url)
            self.regions = RegionList.locus_list_to_locations(graph, data, "locus", "name")
            graph.close()
