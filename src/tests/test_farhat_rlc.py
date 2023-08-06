from tb_variant_filter.masks.farhat_rlc import FarhatLab_RLC_Regions

expected = 773
def test_farhat_rlc_region_count():
    farhat_rlc = FarhatLab_RLC_Regions()
    assert (
        len(farhat_rlc.regions) == expected
    ), f"expected {expected} RLC regions, got {len(farhat_rlc.regions)}"


def test_farhat_rlc_region_count_web():
    farhat_rlc = FarhatLab_RLC_Regions()
    farhat_rlc.load_from_web_and_db()
    assert (
        len(farhat_rlc.regions) == expected
    ), f"expected {expected} RLC regions, got {len(farhat_rlc.regions)}"
