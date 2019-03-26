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

from vcfpy import Record, Reader
from intervaltree import IntervalTree

from . import Filter


class CloseToIndelFilter(Filter):
    intervaltree = None
    dist = 0

    def __init__(self, args: argparse.Namespace) -> 'CloseToIndelFilter':
        super().__init__(args)
        self.intervaltree = IntervalTree()
        if hasattr(args, 'close_to_indel_filter') and args.close_to_indel_filter:
            reader = Reader(args.input_file)
            dist = args.indel_window_size
            self.dist = dist
            for record in reader:
                if not record.is_snv():
                    if record.affected_end < record.affected_start:
                        # this is an insertion, we only have the start site
                        self.intervaltree.addi(begin=record.affected_start - dist, end=record.affected_start + dist)
                    else:
                        self.intervaltree.addi(begin=record.affected_start - dist, end=record.affected_end + dist)
            args.input_file.seek(0)

    def __repr__(self) -> str:

        name = f'{self.__class__.__name__}'
        if self.dist:
            name += f' (Window {self.dist})'
        else:
            name += ' (inactive)'
        return name

    @classmethod
    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--close_to_indel_filter",
            "-I",
            action="store_true",
            default=False,
            help="Mask out single nucleotide variants that are too close to indels",
        )
        parser.add_argument(
            "--indel_window_size",
            type=int,
            default=5,
            help="Window around indel to mask out (mask this number of bases upstream/downstream from the indel. Requires -I option to selected)",
        )

    def __call__(self, record: Record) -> Union[Record, None]:
        retain = True
        if record.is_snv():
            # we are masking SNVs, only the affected_start is relevant since this is a size 1 feature
            retain = not self.intervaltree.overlaps_point(record.affected_start)
        return record if retain else None
