from arm_sapr_tools.synthesize import gaussian_iso_storm_with_sclw

def test_center_of_storm():
    assert gaussian_iso_storm_with_sclw(0., 0., 0., Nmax=1) == 1.0

def test_above_storm():
    assert gaussian_iso_storm_with_sclw(0., 0., 10000., fzl=100., sclw_depth=100.) == 0.0