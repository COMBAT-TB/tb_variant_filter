from tb_variant_filter.masks.tbprofiler import TBProfilerRegions
from .utils import skip_if_no_bolt, get_bolt_url


def test_tbprofiler_region_count():
    tbprofiler = TBProfilerRegions()
    expected = 58
    assert (
        len(tbprofiler.regions) == expected
    ), f"expected {expected} regions, got {len(tbprofiler.regions)}"


@skip_if_no_bolt
def test_tbprofiler_web_region_count():
    tbprofiler = TBProfilerRegions()
    bolt_url = get_bolt_url()
    tbprofiler.load_from_web_and_db(bolt_url)
    expected = 58
    assert (
        len(tbprofiler.regions) == expected
    ), f"expected {expected} regions, got {len(tbprofiler.regions)}"
