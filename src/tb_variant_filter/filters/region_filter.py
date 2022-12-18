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
from typing import List, Union

from intervaltree import Interval, IntervalTree
from vcfpy import Record

import argparse
import sys
from tb_variant_filter.masks import (
    FarhatLab_RLC_Regions,
    FarhatLab_RLC_LowMap_Regions,
    MTBseqRegions,
    PE_PPE_Regions,
    TBProfilerRegions,
    UVPRegions,
)

from . import Filter

REGIONS = {
    "farhat_rlc": FarhatLab_RLC_Regions(),
    "farhat_rlc_lowmap": FarhatLab_RLC_LowMap_Regions(),
    "mtbseq": MTBseqRegions(),
    "pe_ppe": PE_PPE_Regions(),
    "tbprofiler": TBProfilerRegions(),
    "uvp": UVPRegions(),
}


class RegionArgParser(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: List[str],
        option_string: str,
    ) -> None:
        region_names = set(values.strip().split(","))
        for region_name in region_names:
            if region_name not in REGIONS:
                # this is an ugly error but I don't know a cleaner way to do this
                raise sys.exit(
                    f"{region_name} is an unknown region name, should be one of {list(REGIONS.keys())}"
                )
        # if user supplies short option (e.g. '-R') default to 'region_filter" name
        attr = option_string.lstrip("-") if len(option_string) > 2 else "region_filter"
        if hasattr(namespace, attr) and getattr(namespace, attr):
            region_names.update(getattr(namespace, attr))
        setattr(namespace, attr, list(region_names))


class RegionFilter(Filter):
    intervaltree = None
    region_names = []

    @classmethod
    def customize_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument("--region_filter", "-R", action=RegionArgParser, default=[])

    def __init__(self, args: argparse.Namespace) -> "RegionFilter":
        super().__init__(args)
        self.intervaltree = IntervalTree()
        if hasattr(args, "region_filter"):
            self.region_names = args.region_filter
            for name in args.region_filter:
                regions = REGIONS[name].regions
                for location in regions:
                    # convert to 0-based, half open coordinates
                    self.intervaltree.add(Interval(location.start - 1, location.end))

    def __repr__(self):
        name = f"{self.__class__.__name__}"
        if self.region_names:
            name += " on " + ", ".join(self.region_names)
        else:
            name += " (inactive)"
        return name

    def __call__(self, record: Record) -> Union[Record, None]:
        # this logic added so that it easier to add debug code
        retain = True
        if record.affected_end < record.affected_start:
            # this is a insert - 0 length feature
            retain = not self.intervaltree.overlaps_point(record.affected_start)
        else:
            # SNV or MNV (del) - size 1 and above
            retain = not self.intervaltree.overlaps(
                record.affected_start, record.affected_end
            )
        if retain:
            return record
        else:
            return None
