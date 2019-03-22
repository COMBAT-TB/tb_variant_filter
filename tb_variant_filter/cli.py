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
import argparse
import sys
from typing import List, Any, Union
from tb_variant_filter.masks import *

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
    ):
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


def main():
    parser = argparse.ArgumentParser(description="Filter H37Rv SNVs")
    parser.add_argument("--region_filter", action=RegionArgParser)
    parser.add_argument(
        "input_file",
        type=argparse.FileType(),
        help="VCF input file (relative to H37Rv)",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="Output file (VCF format)",
    )
    args = parser.parse_args()
    print(args.region_filter)


if __name__ == "__main__":
    main()
