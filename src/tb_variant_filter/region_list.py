# Copyright (C) 2021  Peter van Heusden <pvh@sanbi.ac.za>
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
from abc import ABC, abstractmethod
import json
import types
from typing import TextIO, List

import pandas as pd
from neo4j import Driver

from . import Location


def bed_to_regions(input_file: TextIO) -> List[Location]:
    regions = []
    count = 1
    for line in input_file:
        fields = line.strip().split("\t")
        assert (
            len(fields) >= 3
        ), f"expect BED file to have at least 3 fields, got: {line}"
        start = int(fields[1])
        end = int(fields[2])
        if len(fields) > 3:
            name = fields[3]
        else:
            name = f"region{count}"
        count += 1
        regions.append(Location(locus=name, start=start, end=end, strand=1))
    return regions


class RegionList(ABC):
    url = ""
    name = ""
    description = ""
    project_url = ""
    # region list is in GFF3 style 1 based, fully closed coordinates
    # like in the first example here: http://genome.ucsc.edu/blog/the-ucsc-genome-browser-coordinate-counting-systems/
    regions = []

    def __init__(self):
        """RegionList - a list of regions to mask out
        :rtype: RegionList
        """
        pass

    @classmethod
    def load_from_json(cls, filename):
        """load region list from json"""
        self = cls()
        with open(filename) as input_file:
            data = json.load(input_file)
            self.url = data["url"]
            self.name = data["name"]
            self.regions = [Location.from_dict(loc) for loc in data["regions"]]
            self.description = data["description"]
            self.project_url = data["project_url"]
        return self

    def save_to_json(self, filename):
        """save object contents to filename"""
        with open(filename, "w") as output_file:
            json.dump(self.to_dict(), output_file, indent=4)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.name == other.name  # noqa: W503
                and self.url == other.url  # noqa: W503
                and self.regions == other.regions  # noqa: W503
                and self.description == other.description  # noqa: W503
                and self.project_url == other.project_url  # noqa: W503
            )

    @staticmethod
    def _find_locus_by_name(tx, name):
        result = tx.run("MATCH (locus) -[:LOCATED_AT]-> (location:Location) "
                        "WHERE ((locus:Gene or locus:PseudoGene) and locus.uniquename = $name) "
                        " or (locus:RRna and locus.name = $name) RETURN locus, location", name=name)
        return result.single()

    @classmethod
    def locus_list_to_locations(
        cls, graph: Driver, locus_df: pd.DataFrame, column_name: str
    ):
        """locus_list_to_locations - lookup H37Rv coordinates of a list of gene/pseudogene/rrnas
        graph - neo4j Driver object (from GraphDatabase.driver())
        locus_df - pandas DataFrame with names of loci
        column_name - name of column in locus_df to use for locus name
        """
        with graph.session() as session:

            locations = []
            for i, row in locus_df.iterrows():
                locus = row[column_name]
                result = session.read_transaction(RegionList._find_locus_by_name, locus)
                locations.append(
                    Location(
                        locus=result["locus"]["uniquename"],
                        start=result["location"]["fmin"],
                        end=result["location"]["fmax"],
                        strand=result["location"]["strand"],
                    )
                )
            return locations

    def to_dict(self):
        # this picks up all class attributes that
        # don't start with _ (like _ hidden attributes and __ builtin attributes
        # and aren't functions (i.e. methods)
        self_to_dict = dict(
            [
                (k, getattr(self, k))
                for k in self.__class__.__dict__.keys()
                if not k.startswith("_")
                and not isinstance(getattr(self, k), types.FunctionType)
            ]
        )
        self_to_dict["regions"] = [loc.to_dict() for loc in self.regions]
        return self_to_dict

    @abstractmethod
    def load_from_web_and_db(self, bolt_url: str):
        """load region list from class url and COMBAT TB eXplorer DB
        :param str bolt_url: bolt URL to connect to COMBAT TB eXplorer DB"""
        pass
