import argparse
import sys
from typing import TextIO

from tb_variant_filter.filters.region_filter import REGIONS


def print_region_list_as_bed(
    region_list_name: str, chromosome_name: str, output_file: TextIO
) -> None:
    if region_list_name not in REGIONS:
        print(f'Unknown region list name "{region_list_name}"', file=sys.stderr)
    else:
        for region in REGIONS[region_list_name].regions:
            print(
                chromosome_name,
                region.start,
                region.end,
                region.locus,
                sep="\t",
                file=output_file,
            )


def main():
    region_list_names = REGIONS.keys()
    parser = argparse.ArgumentParser(description="Output region filter in BED format")
    parser.add_argument(
        "--chromosome_name", help="Chromosome name to use in BED", default="NC_000962.3"
    )
    parser.add_argument(
        "region_list_name", help="Name of region list", choices=region_list_names
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        type=argparse.FileType("w"),
        help="File to write output to",
        default=sys.stdout,
    )
    args = parser.parse_args()

    print_region_list_as_bed(
        args.region_list_name, args.chromosome_name, args.output_file
    )


if __name__ == "__main__":
    main()
