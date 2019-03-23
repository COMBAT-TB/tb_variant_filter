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


class MTBseqRegions(RegionList):
    url = "https://raw.githubusercontent.com/ngs-fzb/MTBseq_source/master/var/res/MTB_Resistance_Mediating.txt"
    name = "MTBseq"
    description = "MTBseq antibiotic resistance genes"
    project_url = "https://github.com/ngs-fzb/MTBseq_source"
    regions = [
        Location(locus="Rv0005", start=5240, end=7267, strand=1),
        Location(locus="Rv0006", start=7302, end=9818, strand=1),
        Location(locus="Rv0486", start=575348, end=576790, strand=1),
        Location(locus="Rv0667", start=759807, end=763325, strand=1),
        Location(locus="Rv0682", start=781560, end=781934, strand=1),
        Location(locus="Rv0701", start=800809, end=801462, strand=1),
        Location(locus="Rv1484", start=1674202, end=1675011, strand=1),
        Location(locus="Rv1630", start=1833542, end=1834987, strand=1),
        Location(locus="Rv1694", start=1917940, end=1918746, strand=1),
        Location(locus="Rv1854c", start=2101651, end=2103042, strand=-1),
        Location(locus="Rv1908c", start=2153889, end=2156111, strand=-1),
        Location(locus="Rv2043c", start=2288681, end=2289241, strand=-1),
        Location(locus="Rv2764c", start=3073680, end=3074471, strand=-1),
        Location(locus="Rv3793", start=4239863, end=4243147, strand=1),
        Location(locus="Rv3794", start=4243233, end=4246517, strand=1),
        Location(locus="Rv3795", start=4246514, end=4249810, strand=1),
        Location(locus="Rv3854c", start=4326004, end=4327473, strand=-1),
        Location(locus="Rv3919c", start=4407528, end=4408202, strand=-1),
        Location(locus="EBG00000313325", start=1471846, end=1473382, strand=1),
        Location(locus="EBG00000313339", start=1473658, end=1476795, strand=1),
    ]

    @doc_inherit
    def load_from_web_and_db(self, bolt_url: str):
        response = requests.get(self.url)
        if response.status_code == 200:
            mtbseq_df = pd.read_csv(StringIO(response.text), delimiter="\t")
            gene_ids = mtbseq_df[
                (mtbseq_df["Region"] == "coding")
                & (~mtbseq_df["Antibiotic"].str.contains("phylo"))  # noqa: W503
            ]["Gene ID"].drop_duplicates()
            rrna_ids = mtbseq_df[
                (mtbseq_df["Region"] == "ribosomal")
                & (~mtbseq_df["Antibiotic"].str.contains("phylo"))  # noqa: W503
            ]["Gene Name"].drop_duplicates()
            mtbseq_ids = pd.DataFrame(pd.concat((gene_ids, rrna_ids)), columns=["id"])
            graph = Graph(uri=bolt_url)
            self.regions = RegionList.locus_list_to_locations(graph, mtbseq_ids, "id")
