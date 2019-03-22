from .. import Location, doc_inherit
from io import StringIO
import pandas as pd
from py2neo import Graph
import requests

from ..region_list import RegionList


class TBprofilerRegions(RegionList):
    url = "https://raw.githubusercontent.com/jodyphelan/TBProfiler/master/db/tbdb.bed"
    name = "TBProfiler"
    regions = [
        Location(locus="Rv0005", start=5240, end=7267, strand=1),
        Location(locus="Rv0006", start=7302, end=9818, strand=1),
        Location(locus="Rv0667", start=759807, end=763325, strand=1),
        Location(locus="Rv0668", start=763370, end=767320, strand=1),
        Location(locus="Rv0678", start=778990, end=779487, strand=1),
        Location(locus="Rv0682", start=781560, end=781934, strand=1),
        Location(locus="Rv0701", start=800809, end=801462, strand=1),
        Location(locus="Rv1267c", start=1416181, end=1417347, strand=-1),
        Location(locus="EBG00000313325", start=1471846, end=1473382, strand=1),
        Location(locus="EBG00000313339", start=1473658, end=1476795, strand=1),
        Location(locus="Rv1483", start=1673440, end=1674183, strand=1),
        Location(locus="Rv1484", start=1674202, end=1675011, strand=1),
        Location(locus="Rv1630", start=1833542, end=1834987, strand=1),
        Location(locus="Rv1694", start=1917940, end=1918746, strand=1),
        Location(locus="Rv1908c", start=2153889, end=2156111, strand=-1),
        Location(locus="Rv2043c", start=2288681, end=2289241, strand=-1),
        Location(locus="Rv2245", start=2518115, end=2519365, strand=1),
        Location(locus="Rv2416c", start=2714124, end=2715332, strand=-1),
        Location(locus="Rv2428", start=2726193, end=2726780, strand=1),
        Location(locus="Rv2447c", start=2746135, end=2747598, strand=-1),
        Location(locus="Rv2671", start=2986839, end=2987615, strand=1),
        Location(locus="Rv2754c", start=3067193, end=3067945, strand=-1),
        Location(locus="Rv2764c", start=3073680, end=3074471, strand=-1),
        Location(locus="Rv2780", start=3086820, end=3087935, strand=1),
        Location(locus="Rv3261", start=3640543, end=3641538, strand=1),
        Location(locus="Rv3423c", start=3840194, end=3841420, strand=-1),
        Location(locus="Rv3601c", start=4043862, end=4044281, strand=-1),
        Location(locus="Rv3793", start=4239863, end=4243147, strand=1),
        Location(locus="Rv3794", start=4243233, end=4246517, strand=1),
        Location(locus="Rv3795", start=4246514, end=4249810, strand=1),
        Location(locus="Rv3854c", start=4326004, end=4327473, strand=-1),
        Location(locus="Rv3855", start=4327549, end=4328199, strand=1),
        Location(locus="Rv3919c", start=4407528, end=4408202, strand=-1),
    ]

    @doc_inherit
    def load_from_web_and_db(self, bolt_url: str):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = pd.read_csv(StringIO(response.text), delimiter='\t',
                               names=["Chromosome", "start", "end", "locus", "name", "resistance"])
            graph = Graph(uri=bolt_url)
            self.regions = RegionList.locus_list_to_locations(graph, data, 'locus')
