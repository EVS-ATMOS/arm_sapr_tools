

def ingest_xsapr2(radar):
    """NEED TO ADD DOCUMENTS
    HERE
    """
    # page 44 of https://github.com/scollis/CfRadial/blob/master/docs/CfRadialDoc.v2.0.draft.pdf
    z_name = 'equivalent_reflectivity_factor'
    v_name = 'radial_velocity_of_scatterers_away_from_instrument'
    wth_name = 'doppler_spectrum_width'
    zdr_name = 'log_differential_reflectivity_hv'
    ldr_name = 'log_linear_depolarization_ratio_hv'
    phidp_name = 'differential_phase_hv'
    kdp_name = 'specific_differential_phase_hv'
    rhv_name = 'cross_correlation_ratio_hv'
    power_name = 'log_power'
    sqi_name = 'normalized_coherent_power'
    zc_name = 'corrected_equivalent_reflectivity_factor'
    vc_name = 'corrected_radial_velocity_of_scatterers_away_from_instrument'
    zdrc_name = 'corrected_log_differential_reflectivity_hv'
    class_name = 'radar_echo_classification'
    snr_name = 'signal_to_noise_ratio'
    pow_name = 'log_power'

    trans_table = {'Z': {'standard_name': z_name, 'name': 'reflectivity'},
                   'UZ': {'standard_name': z_name, 'name': 'uncorrected_reflectivity'},
                   'UZDR1': {'standard_name': zdr_name, 'name': 'uncorrected_differential_reflectivity_1'},
                   'ZDR1': {'standard_name': zdr_name, 'name': 'differential_reflectivity_1'},
                   'CWv': {'standard_name': wth_name, 'name': 'corrected_spectral_width_vertical'},
                   'AZh': {'standard_name': z_name, 'name': 'attenuation_corrected_reflectivity_horizontal'},
                   'Wh': {'standard_name': wth_name, 'name': 'spectral_width_horizontal'},
                   'UWh': {'standard_name': wth_name, 'name': 'un_spectral_width_horizontal'},
                   'UWv': {'standard_name': wth_name, 'name': 'un_spectral_width_vertical'},
                   'UnVh': {'standard_name': vc_name, 'name': 'unfolded_radial_velocity_horizontal'},
                   'SNRv': {'standard_name': snr_name, 'name': 'signal_to_noise_ratio_vertical'},
                   'SIGPOWh': {'standard_name': pow_name, 'name': 'log_power_horizontal'},
                   'SIGPOWv': {'standard_name': pow_name, 'name': 'log_power_vertical'},
                   'UPHIDP': {'standard_name': phidp_name, 'name': 'unfolded_differential_phase'},
                   'KDP': {'standard_name': kdp_name, 'name': 'specific_differential_phase'},
                   'AZDR': {'standard_name': zdrc_name, 'name': 'attenuation_corrected_differential_reflectivity'},
                   'RHOHV': {'standard_name': rhv_name, 'name': 'cross_correlation_ratio_hv', 'units': 'unitless'},
                   'ZDR': {'standard_name': zdr_name, 'name': 'differential_reflectivity'},
                   'Wv': {'standard_name': wth_name, 'name': 'spectral_width_vertical'},
                   'Vv': {'standard_name': v_name, 'name': 'radial_velocity_vertical'},
                   'UZv': {'standard_name': z_name, 'name': 'uncorrected_reflectivity_vertical'},
                   'SQIh': {'standard_name': sqi_name, 'name': 'normalized_coherent_power_horizontal',
                            'units': 'unitless'},
                   'PHIDP': {'standard_name': phidp_name, 'name': 'differential_phase'},
                   'CMAP': {'standard_name': class_name, 'name': 'clutter_map', 'units': 'unitless'},
                   'SNRh': {'standard_name': snr_name, 'name': 'signal_to_noise_ratio_horizontal'},
                   'Vh': {'standard_name': v_name, 'name': 'radial_velocity_horizontal'},
                   'CWh': {'standard_name': wth_name, 'name': 'corrected_spectral_width_horizontal'},
                   'AZDR1': {'standard_name': zdrc_name, 'name': 'attenuation_corrected_differential_reflectivity_1'},
                   'UZh': {'standard_name': z_name, 'name': 'uncorrected_refelctivity_horizontal'},
                   'Zv': {'standard_name': z_name, 'name': 'reflectivity_horizontal_vertical'},
                   'URHOHV': {'standard_name': rhv_name, 'name': 'uncorrected_cross_correlation_ratio_hv',
                              'units': 'unitless'},
                   'Zh': {'standard_name': z_name, 'name': 'reflectivity_horizontal'},
                   'CLASS': {'standard_name': class_name, 'name': 'echo_id', 'units': 'unitless'},
                   'UZDR': {'standard_name': zdr_name, 'name': 'uncorrected_differential_reflectivity'},
                   'UnVv': {'standard_name': vc_name, 'name': 'unfolded_radial_velocity_vertical'},
                   'SQIv': {'standard_name': sqi_name, 'name': 'normalized_coherent_power_vertical',
                            'units': 'unitless'}}

    for field_name in list(radar.fields.keys()):
        for transfer_item in list(trans_table[field_name].keys()):
            if transfer_item != 'name':
                radar.fields[field_name][transfer_item] = trans_table[field_name][transfer_item]
        radar.fields[field_name]['HDF_name'] = field_name
        radar.fields[trans_table[field_name]['name']] = radar.fields.pop(field_name)

    return radar

