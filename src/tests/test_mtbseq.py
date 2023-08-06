from tb_variant_filter.masks.mtbseq import MTBseqRegions
from .utils import skip_if_no_bolt, get_bolt_url


def test_mtbseq_region_count():
    mtbseq = MTBseqRegions()
    expected = 28
    assert (
        len(mtbseq.regions) == expected
    ), f"expected {expected} regions, got {len(mtbseq.regions)}"


@skip_if_no_bolt
def test_mtbseq_web_region_count():
    mtbseq = MTBseqRegions()
    saved_region_count = len(mtbseq.regions)
    bolt_url = get_bolt_url()
    mtbseq.load_from_web_and_db(bolt_url)
    expected = saved_region_count
    assert (
        len(mtbseq.regions) == expected
    ), f"expected {expected} regions, got {len(mtbseq.regions)}"
