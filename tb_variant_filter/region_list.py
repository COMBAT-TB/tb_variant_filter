from abc import ABC, abstractmethod
import json

import pandas as pd
from py2neo import Graph, NodeMatcher

from . import Location


class RegionList(ABC):
    url = ""
    name = ""
    regions = []

    def __init__(self):
        """RegionList - a list of regions to mask out"""
        pass

    @classmethod
    def load_from_json(cls, filename):
        """load region list from json"""
        self = cls()
        data = json.load(open(filename), object_hook=Location.from_dict)
        self.url = data["url"]
        self.name = data["name"]
        self.regions = data["regions"]
        return self

    def save_to_json(self, filename):
        """save object contents to filename"""
        json.dump(
            self.regions,
            open(filename, "w"),
            indent=4,
            default=RegionList.encode_location,
        )

    @classmethod
    def locus_list_to_locations(
        cls, graph: Graph, locus_df: pd.DataFrame, column_name: str
    ):
        """locus_list_to_locations - lookup H37Rv coordinates of a list of gene/pseudogene/rrnas
        graph - py2neo Graph object
        locus_df - pandas DataFrame with names of loci
        column_name - name of column in locus_df to use for locus name
        """
        matcher = NodeMatcher(graph)
        info = []
        for i, row in locus_df.iterrows():
            locus = row[column_name]
            gene_match = matcher.match("Gene", uniquename=locus)
            pseudogene_match = matcher.match("PseudoGene", uniquename=locus)
            rrna_match = matcher.match("RRna", name=locus)
            if gene_match:
                info.append(gene_match.first())
            elif pseudogene_match:
                info.append(pseudogene_match.first())
            elif rrna_match:
                info.append(rrna_match.first())
            else:
                print("not found", locus)
        assert len(info) == len(
            locus_df
        ), "Failed to find all the loci in question {} vs {}".format(
            len(locus_df), len(info)
        )

        locations = []
        for item in info:
            location_r = graph.match_one((item,), r_type="LOCATED_AT")
            location = location_r.end_node
            locations.append(
                Location(
                    locus=item["uniquename"],
                    start=location["fmin"],
                    end=location["fmax"],
                    strand=location["strand"],
                )
            )
        return locations

    @classmethod
    def encode_location(cls, location: Location):
        return dict(
            locus=location.locus,
            start=location.start,
            end=location.end,
            strand=location.strand,
        )

    @abstractmethod
    def load_from_web_and_db(self, bolt_url: str):
        """load region list from class url and COMBAT TB eXplorer DB
        :param str bolt_url: bolt URL to connect to COMBAT TB eXplorer DB"""
        pass

