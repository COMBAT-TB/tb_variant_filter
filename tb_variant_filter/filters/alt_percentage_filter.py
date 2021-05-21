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
from collections import OrderedDict
from typing import Union
import vcfpy

from . import Filter


class AltPercentageDepthFilter(Filter):
    min_percentage = 0

    def __init__(self, args: argparse.Namespace) -> "AltPercentageDepthFilter":
        super().__init__(args)
        if (
            hasattr(args, "min_percentage_alt_filter")
            and args.min_percentage_alt_filter  # noqa W503
            and hasattr(args, "min_percentage_alt")  # noqa W503
        ):
            self.min_percentage = args.min_percentage_alt

    @classmethod
    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--min_percentage_alt_filter",
            "-P",
            action="store_true",
            default=False,
            help="Mask out variants with less than a given percentage variant allele at this site",
        )
        parser.add_argument(
            "--min_percentage_alt",
            type=float,
            default=90.0,
            help="Variants with less than this percentage variants at a site will be masked out",
        )

    def __repr__(self) -> str:
        name = f"{self.__class__.__name__}"
        if self.min_percentage:
            name += f" (minimum {self.min_percentage:.2f}% alt allele)"
        else:
            name += " (inactive)"
        return name

    def __call__(self, record: vcfpy.Record) -> Union[vcfpy.Record, None]:
        if not ("AO" in record.INFO and "DP" in record.INFO):
            return None
        # VCF records have 1 (or 0?) or more ALT records supported by calls from 1 or more samples
        # and AO INFO fields with dimension matching the ALT dimensions
        # This Transform type Filter retains only those ALTs and corresponding INFO matching the
        # criteria of the filter
        # It does not modify the calls which might cause problems of calls not matching ALT
        retain = []
        for i, alt in enumerate(record.ALT):
            alt_percentage = (
                float(record.INFO["AO"][i]) / float(record.INFO["DP"]) * 100.0
            )
            retain.append(not alt_percentage < self.min_percentage)
        if not any(retain):
            return None
        new_ALT = [alt for i, alt in enumerate(record.ALT) if retain[i]]
        new_INFO = OrderedDict()
        # these are produced by snpEff and keys occur once per implicated gene
        # the simplest solution is to copy them all across
        snpeff_keys = set(["ANN", "LOF", "NMD"])
        for key in record.INFO:
            if type(record.INFO[key]) == list:
                new_INFO[key] = [
                    # retain all ANN records and the only those other records that correspond to alts that we retain
                    el
                    for i, el in enumerate(record.INFO[key])
                    if key in snpeff_keys or retain[i]
                ]
            else:
                new_INFO[key] = record.INFO[key]
        new_record = vcfpy.Record(
            record.CHROM,
            record.POS,
            record.ID,
            record.REF,
            new_ALT,
            record.QUAL,
            record.FILTER,
            new_INFO,
            record.FORMAT,
            record.calls,
        )
        return new_record
