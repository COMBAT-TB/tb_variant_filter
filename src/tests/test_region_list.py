from tempfile import NamedTemporaryFile

from tb_variant_filter.masks.pe_ppe import PE_PPE_Regions


def test_region_load_save():
    pe_ppe = PE_PPE_Regions()
    temp = NamedTemporaryFile(delete=False)
    pe_ppe.save_to_json(temp.name)
    reloaded_pe_ppe = pe_ppe.load_from_json(temp.name)
    # os.remove(temp.name)
    assert pe_ppe == reloaded_pe_ppe
