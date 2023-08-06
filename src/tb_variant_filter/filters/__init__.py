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
#
# these filter modules are very closely tied to the command line interface (tb_variant_filter.cli),
# in effect they simply extend the command line interface, allowing for the cli.py
# to remain simpler at the cost of making this code less general
from abc import abstractmethod
import argparse
from typing import List, Union, Type

from vcfpy import Record, Header


class Filter(object):
    def __init__(self, args: argparse.Namespace, header: Header):
        self.active = False
        self.header = header

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def customize_parser(cls, parser: argparse.ArgumentParser):
        pass

    @abstractmethod
    def __call__(self, record: Record) -> Union[Record, None]:
        """Returns None if the record fails the Filter test, else the (possibly transformed) Record"""
        pass


class UnionFilter(Filter):
    def __init__(self, filters: List[Filter]):
        self.filters = filters

    def __repr__(self) -> str:
        name = f"{self.__class__.__name__} on "
        name += ", ".join(repr(variant_filter) for variant_filter in self.filters)
        return name

    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        pass

    def __call__(self, record: Record) -> Union[Record, None]:
        for filter in self.filters:
            record = filter(record)
            if not record:
                # don't continue the chain
                # info = str(orig_record.INFO["DP"])
                # info += " AO: " + str(orig_record.INFO["AO"]) if "AO" in orig_record.INFO else ""
                # info += " AF: " + str(orig_record.INFO["AF"]) if "AF" in orig_record.INFO else ""
                # print("REMOVING", info)
                return None
        return record  # return the record, perhaps after some transformation


from .region_filter import RegionFilter  # noqa: E402
from .close_to_indel_filter import CloseToIndelFilter  # noqa: E402
from .alt_percentage_filter import AltPercentageDepthFilter  # noqa: E402
from .min_depth_filter import MinDepthFilter  # noqa: 402
from .snv_only_filter import SnvOnly  # noqa: 402


def get_filters() -> List[Type[Filter]]:
    return [
        RegionFilter,
        CloseToIndelFilter,
        AltPercentageDepthFilter,
        MinDepthFilter,
        SnvOnly,
    ]


__all__ = [variant_filter.__name__ for variant_filter in get_filters()] + [
    "UnionFilter",
    "get_filters",
]
