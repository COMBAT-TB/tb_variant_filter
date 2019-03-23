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

import vcfpy

from .filters import get_filters, IntersectFilter


def filter_vcf_file(args: argparse.ArgumentParser):
    """filter_vcf_file: taking parameters from args, apply filters to VCF file, generating filtered VCF file"""
    variant_filters = []
    for filter_class in get_filters():
        variant_filters.append(filter_class(args))

    variant_filter = IntersectFilter(variant_filters)

    reader = vcfpy.Reader(args.input_file)
    writer = vcfpy.Writer(args.output_file, header=reader.header)
    masked_records = 0
    for record in reader:
        if variant_filter(record):
            masked_records += 1
        else:
            writer.write_record(record)
    return masked_records


def main():
    parser = argparse.ArgumentParser(description="Filter H37Rv SNVs")
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

    for filter_class in get_filters():
        filter_class.customize_parser(parser)

    args = parser.parse_args()

    masked_records = filter_vcf_file(args)
    print(masked_records)


if __name__ == "__main__":
    main()
