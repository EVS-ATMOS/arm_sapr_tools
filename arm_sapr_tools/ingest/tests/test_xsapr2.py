from pyart.testing import make_single_ray_radar
from arm_sapr_tools.ingest import ingest_xsapr2

def test_ingest_xsapr2():
    test_radar = make_single_ray_radar()
    old_keys = test_radar.fields.keys()
    refl = test_radar.fields['reflectivity']
    for key in list(old_keys):
        _ = test_radar.fields.pop(key)
    test_radar.add_field('Zh', refl)

    ingestable = ingest_xsapr2(test_radar)
    assert(list(ingestable.fields.keys())[0] == 'reflectivity_horizontal')