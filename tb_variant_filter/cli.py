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
from .filters import get_filters


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
    print(args.region_filter)


if __name__ == "__main__":
    main()
