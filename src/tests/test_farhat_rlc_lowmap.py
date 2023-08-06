from tb_variant_filter.masks.farhat_rlc_lowmap import FarhatLab_RLC_LowMap_Regions

expected = 1324
def test_farhat_rlc_region_count():
    farhat_rlc_lowmap = FarhatLab_RLC_LowMap_Regions
    assert (
        len(farhat_rlc_lowmap.regions) == expected
    ), f"expected {expected} RLC and LowMap regions, got {len(farhat_rlc_lowmap.regions)}"


def test_farhat_rlc_region_count_web():
    farhat_rlc_lowmap = FarhatLab_RLC_LowMap_Regions()
    farhat_rlc_lowmap.load_from_web_and_db()
    assert (
        len(farhat_rlc_lowmap.regions) == expected
    ), f"expected {expected} RLC and LowMap regions, got {len(farhat_rlc_lowmap.regions)}"
