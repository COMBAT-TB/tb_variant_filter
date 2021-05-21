from tb_variant_filter.masks import farhat_rlc
from tb_variant_filter.masks.farhat_rlc import FarhatLab_RLC_Regions


def test_farhat_rlc_region_count():
    farhat_rlc = FarhatLab_RLC_Regions()
    expected = 773
    assert len(farhat_rlc.regions) == expected, f'expected {expected} RLC regions, got {len(farhat_rlc.regions)}'


def test_farhat_rlc_region_count():
    farhat_rlc = FarhatLab_RLC_Regions()
    farhat_rlc.load_from_web_and_db()
    expected = 773
    assert len(farhat_rlc.regions) == expected, f'expected {expected} RLC regions, got {len(farhat_rlc.regions)}'
