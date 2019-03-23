from typing import List

from intervaltree import Interval, IntervalTree
from vcfpy import record

import argparse
import sys
from tb_variant_filter.masks import MTBseqRegions, PE_PPE_Regions, TBProfilerRegions, UVPRegions

from . import Filter

REGIONS = {
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
        attr = option_string.lstrip('-')
        if hasattr(namespace, attr) and getattr(namespace, attr):
            region_names.update(getattr(namespace, attr))
        setattr(namespace, attr, list(region_names))


class RegionFilter(Filter):
    intervaltree = None

    @classmethod
    def customize_parser(cls, parser: argparse.ArgumentParser):
        parser.add_argument("--region_filter", action=RegionArgParser, default=[])

    def __init__(self, args: argparse.Namespace) -> 'RegionFilter':
        super().__init__()
        self.intervaltree = IntervalTree()
        for name in args.region_filter:
            regions = REGIONS[name].regions
            for location in regions:
                # convert to 0-based, half open coordinates
                self.intervaltree.add(Interval(location.start - 1, location.end))

    def __call__(self, record: record) -> bool:
        # this logic added so that it easier to add debug code
        mask = False
        if record.affected_end < record.affected_start:
            # this is a insert - 0 length feature
            mask = self.intervaltree.overlaps_point(record.affected_start)
        else:
            # SNV or MNV (del) - size 1 and above
            mask = self.intervaltree.overlaps(record.affected_start, record.affected_end)
        if mask:
            if record.affected_start < record.affected_end:
                print("FILTER:", record)
        return mask
