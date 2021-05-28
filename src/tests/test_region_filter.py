from argparse import Namespace
from io import StringIO
import os.path

from tb_variant_filter.cli import filter_vcf_file


def test_region_filter():
    test_dir = os.path.dirname(__file__)
    args = Namespace()
    # prepare the args to tell filter_vcf_file how to proceed
    setattr(args, "region_filter", ["pe_ppe", "tbprofiler", "uvp"])
    input_file = open(os.path.join(test_dir, "data/test_input1.vcf"))
    setattr(args, "input_file", input_file)
    output_file = StringIO()
    setattr(args, "output_file", output_file)
    expected_content = open(os.path.join(test_dir, "data/test_output1.vcf")).read()
    expected_masked_variants_count = 8
    masked_variants_count = filter_vcf_file(args)
    assert (
        masked_variants_count == expected_masked_variants_count
    ), f"expected {expected_masked_variants_count} got {masked_variants_count}"
    assert output_file.getvalue() == expected_content


def test_farhatlab_rlc_filter():
    test_dir = os.path.dirname(__file__)
    args = Namespace()
    # prepare the args to tell filter_vcf_file how to proceed
    setattr(args, "region_filter", ["farhat_rlc"])
    input_file = open(os.path.join(test_dir, "data/test_input1.vcf"))
    setattr(args, "input_file", input_file)
    output_file = StringIO()
    setattr(args, "output_file", output_file)
    expected_content = open(os.path.join(test_dir, "data/test_output8.vcf")).read()
    expected_masked_variants_count = 2
    masked_variants_count = filter_vcf_file(args)
    assert (
        masked_variants_count == expected_masked_variants_count
    ), f"expected {expected_masked_variants_count} got {masked_variants_count}"
    assert output_file.getvalue() == expected_content
