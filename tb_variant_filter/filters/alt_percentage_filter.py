import argparse

import vcfpy

from . import Filter

class AltPercentageDepthFilter(Filter):
    min_percentage = 0
    def __init__(self, args: argparse.Namespace) -> 'AltPercentageDepthFilter':
        if hasattr(args, 'min_percentage_alt'):
            self.min_percentage = args.min_percentage_alt

    @classmethod
    def customize_parser(cls, parser: argparse.ArgumentParser) -> None:
        parser.add_argument('--min_percentage_alt_filter', '-P', action='store_true', default=False, help='Mask out variants with less than a % variant allele at this side')
        parser.add_argument('--min_percentage_alt', type=float, default=90.0, help='Variants with less than this % variants at a site will be masked out')

    def __repr__(self) -> str:
        name = f'{self.__class__.__name__}'
        if self.min_percentage:
            name += f' (minimum {self.min_percentage:.2f}% alt allele'
        else:
            name += ' (inactive)'
        return name

    def __call__(self, record: vcfpy.Record):
        assert len(record.ALT) == 1, "can only process records with a single alt record"
        if not('AO' in record.INFO and 'DP' in record.INFO):
            return False
        alt_percentage = float(record.INFO['AO'][0]) / float(record.INFO['DP']) * 100.0
        # print(alt_percentage, record)
        return alt_percentage < self.min_percentage
