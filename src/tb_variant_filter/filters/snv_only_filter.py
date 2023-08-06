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


class SnvOnly(Filter):
    snv_only = False

    def __init__(self, args: argparse.Namespace, header: vcfpy.Header) -> "SnvOnly":
        super().__init__(args, header)
        if hasattr(args, "snv_only_filter") and args.snv_only_filter:
            self.snv_only = True

    @classmethod
    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--snv_only_filter",
            action="store_true",
            default=False,
            help="Mask out variants that are not SNVs",
        )

    def __repr__(self) -> str:
        name = f"{self.__class__.__name__}"
        if self.snv_only:
            name += " (active)"
        else:
            name += " (inactive)"
        return name

    def __call__(self, record: vcfpy.Record) -> Union[vcfpy.Record, None]:
        if self.snv_only:
            return record if record.is_snv() else None
        else:
            return record
