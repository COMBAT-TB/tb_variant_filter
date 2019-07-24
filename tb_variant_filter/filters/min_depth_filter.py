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
from typing import Union
import vcfpy

from . import Filter


class MinDepthFilter(Filter):
    min_depth = 0

    def __init__(self, args: argparse.Namespace) -> "MinDepthFilter":
        super().__init__(args)
        if (
            hasattr(args, "min_depth_filter")
            and args.min_depth_filter  # noqa W503
            and hasattr(args, "min_depth")  # noqa W503
        ):
            self.min_depth = args.min_depth

    @classmethod
    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--min_depth_filter",
            "-D",
            action="store_true",
            default=False,
            help="Mask out variants with less than a given depth of reads",
        )
        parser.add_argument(
            "--min_depth",
            type=int,
            default=30,
            help="Variants at sites with less than this depth of reads will be masked out",
        )

    def __repr__(self) -> str:
        name = f"{self.__class__.__name__}"
        if self.min_depth:
            name += f" (minimum {self.min_depth} depth)"
        else:
            name += " (inactive)"
        return name

    def __call__(self, record: vcfpy.Record) -> Union[vcfpy.Record, None]:
        if not ("DP" in record.INFO):
            return None
        return record if record.INFO["DP"] >= self.min_depth else None
