from tb_variant_filter.masks.pe_ppe import PE_PPE_Regions
from .utils import skip_if_no_bolt, get_bolt_url


def test_pe_ppe_region_count():
    pe_ppe = PE_PPE_Regions()
    expected = 168
    assert (
        len(pe_ppe.regions) == expected
    ), f"expected {expected} PE/PPE regions, got {len(pe_ppe.regions)}"


@skip_if_no_bolt
def test_pe_ppe_web_region_count():
    pe_ppe = PE_PPE_Regions()
    saved_region_count = len(pe_ppe.regions)
    bolt_url = get_bolt_url()
    pe_ppe.load_from_web_and_db(bolt_url)
    expected = saved_region_count
    assert (
        len(pe_ppe.regions) == expected
    ), f"expected {expected} PE/PPE regions, got {len(pe_ppe.regions)}"
