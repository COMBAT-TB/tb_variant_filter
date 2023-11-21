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
import sys
from typing import Union
import vcfpy

from . import Filter


class AltPercentageDepthFilter(Filter):
    min_percentage = 0

    def __init__(
        self, args: argparse.Namespace, header: vcfpy.Header
    ) -> "AltPercentageDepthFilter":
        super().__init__(args, header)
        if (
            hasattr(args, "min_percentage_alt_filter")
            and args.min_percentage_alt_filter  # noqa W503
            and hasattr(args, "min_percentage_alt")  # noqa W503
        ):
            self.active = True
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
        # VCF records have 1 (or 0?) or more ALT records supported by calls from 1 or more samples
        # and (sometimes) AO INFO fields with dimension matching the ALT dimensions. Or AF1 or DP4
        # or... there really is not standard way of representing ALT allele frequency in
        # VCF - see this discussion: https://github.com/samtools/hts-specs/issues/78
        # This Transform type Filter retains only those ALTs and corresponding INFO matching the
        # criteria of the filter
        # It does not modify the calls which might cause problems of calls not matching ALT
        retain = []
        alt_percentage = None
        # bcftools call adds AF1 INFO, but only for first allele
        if self.header.has_header_line("INFO", "AF1"):
            alt_percentage = record.INFO["AF1"] * 100
        elif self.header.has_header_line("INFO", "DP4"):
            (fwd_ref, rev_ref, fwd_alt, rev_alt) = record.INFO["DP4"]
            alt_percentage = (
                (fwd_alt + rev_alt) / (fwd_ref + rev_ref + fwd_alt + rev_alt) * 100
            )
        if alt_percentage is not None:
            retain.append(not alt_percentage < self.min_percentage)
        elif self.header.has_header_line("INFO", "AF") or (
            self.header.has_header_line("INFO", "AO")
            and self.header.has_header_line("INFO", "DP")  # noqa: W503
        ):
            for i, _ in enumerate(record.ALT):
                if self.header.has_header_line("INFO", "AF"):
                    alt_percentage = record.INFO["AF"][i] * 100
                elif self.header.has_header_line(
                    "INFO", "AO"
                ) and self.header.has_header_line("INFO", "DP"):
                    alt_percentage = (
                        float(record.INFO["AO"][i]) / float(record.INFO["DP"]) * 100
                    )
                retain.append(not alt_percentage < self.min_percentage)
        else:
            # we've got nothing to add to retain - leave it as an empty list
            print(
                "No alt allele depth information found in VCF, disabling alt allele percentage filter",
                file=sys.stderr,
            )
        if not any(retain):
            return None

        new_ALT = [alt for i, alt in enumerate(record.ALT) if retain[i]]
        new_INFO = OrderedDict()
        # these are produced by snpEff and keys occur once per implicated gene
        # the simplest solution is to copy them all across
        for key in record.INFO:
            if self.header.get_info_field_info(key).number == "A":
                # 'A' fields have one entry for each alternative allele - copy only those for retained alleles
                field_len = len(record.INFO[key])
                retain_len = len(retain)
                assert (
                    field_len == retain_len
                ), f"Length of array-type INFO field ({field_len}) does not match length of retain ({retain_len})"
                new_INFO[key] = [
                    # retain all ANN records and the only those other records that correspond to alts that we retain
                    el
                    for i, el in enumerate(record.INFO[key])
                    if retain[i]
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
