import argparse

import vcfpy
from intervaltree import IntervalTree

from . import Filter


class CloseToIndelFilter(Filter):
    intervaltree = None
    dist = 0

    def __init__(self, args: argparse.Namespace) -> 'CloseToIndelFilter':
        super().__init__(args)
        self.intervaltree = IntervalTree()
        if hasattr(args, 'close_to_indel_filter') and args.close_to_indel_filter:
            reader = vcfpy.Reader(args.input_file)
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

    def __call__(self, record: vcfpy.Record) -> bool:
        mask = False
        if record.is_snv():
            # we are masking SNVs, only the affected_start is relevant since this is a size 1 feature
            mask = self.intervaltree.overlaps_point(record.affected_start)
        return mask
