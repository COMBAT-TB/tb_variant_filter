from tb_variant_filter.masks.uvp import UVPRegions
from tb_variant_filter import Location

from .utils import skip_if_no_bolt, get_bolt_url

expected = 220


def test_uvp_region_count():
    uvp = UVPRegions()
    assert (
        len(uvp.regions) == expected
    ), f"expected {expected} regions, got {len(uvp.regions)}"


def test_first_last_region():
    uvp = UVPRegions()
    assert uvp.regions[0] == Location(locus="Rv0031", start=33582, end=33794, strand=1)
    assert uvp.regions[-1] == Location(
        locus="IG877_Rv0861c-Rv0862c", start=960_152, end=960_341, strand=1
    )


@skip_if_no_bolt
def test_web_uvp_region_count():
    uvp = UVPRegions()
    bolt_url = get_bolt_url()
    uvp.load_from_web_and_db(bolt_url)
    assert len(uvp.regions) == expected, f"expected {expected} regions"
