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

import vcfpy

from . import Filter


class AltPercentageDepthFilter(Filter):
    min_percentage = 0

    def __init__(self, args: argparse.Namespace) -> "AltPercentageDepthFilter":
        super().__init__(args)
        if hasattr(args, "min_percentage_alt"):
            self.min_percentage = args.min_percentage_alt

    @classmethod
    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--min_percentage_alt_filter",
            "-P",
            action="store_true",
            default=False,
            help="Mask out variants with less than a given percentage variant allele at this side",
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

    def __call__(self, record: vcfpy.Record):
        assert len(record.ALT) == 1, "can only process records with a single alt record"
        if not ("AO" in record.INFO and "DP" in record.INFO):
            return False
        alt_percentage = float(record.INFO["AO"][0]) / float(record.INFO["DP"]) * 100.0
        # print(alt_percentage, record)
        return alt_percentage < self.min_percentage
