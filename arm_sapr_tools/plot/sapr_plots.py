from matplotlib import pyplot as plt
import numpy as np
import pyart
from netCDF4 import num2date
import pytz
import cartopy
import os


def plot_xsapr2(radar, field='reflectivity', cmap=None,
                vmin=None, vmax=None, sweep=None, fig=None):
    if sweep is None:
        sweep = 0

    # Lets get some geographical context
    lats = radar.gate_latitude
    lons = radar.gate_longitude

    min_lon = lons['data'].min()
    min_lat = lats['data'].min()
    max_lat = lats['data'].max()
    max_lon = lons['data'].max()

    print('min_lat:', min_lat, ' min_lon:', min_lon,
          ' max_lat:', max_lat, ' max_lon:', max_lon)

    index_at_start = radar.sweep_start_ray_index['data'][sweep]
    time_at_start_of_radar = num2date(radar.time['data'][index_at_start],
                                      radar.time['units'])
    GMT = pytz.timezone('GMT')
    local_time = GMT.fromutc(time_at_start_of_radar)
    fancy_date_string = local_time.strftime('%A %B %d at %I:%M %p %Z')
    print(fancy_date_string)
    if fig is None:
        fig = plt.figure(figsize=[15, 10])
    display = pyart.graph.RadarMapDisplayCartopy(radar)
    lat_0 = display.loc[0]
    lon_0 = display.loc[1]

    # Main difference! Cartopy forces you to select a projection first!
    projection = cartopy.crs.Mercator(
        central_longitude=lon_0,
        min_latitude=min_lat, max_latitude=max_lat)

    start = radar.sweep_start_ray_index['data'][sweep]
    end = radar.sweep_end_ray_index['data'][sweep]
    nrays = end - start
    mid = int(start + nrays / 2.)
    print(mid)
    title = str(radar.elevation['data'][mid]) + \
            ' deg X-SAPR2 ' + field.replace('_', ' ') + ' \n' + fancy_date_string

    display.plot_ppi_map(
        field, sweep, colorbar_flag=False,
        title=title,
        projection=projection,
        min_lon=min_lon, max_lon=max_lon, min_lat=min_lat, max_lat=max_lat,
        vmin=vmin, vmax=vmax, cmap=cmap)

    lb = display._get_colorbar_label(field)
    cb = plt.colorbar(display.plots[0], shrink=.7, aspect=30, pad=0.01)
    cb.set_label(lb)

    # Mark the radar
    display.plot_point(lon_0, lat_0, label_text='X-SAPR2')

    # Plot some lat and lon lines
    gl = display.ax.gridlines(draw_labels=True,
                              linewidth=2, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False

def gen_name(odir, radar, field, postfix=None):
    if postfix is None:
        postfix = '.png'
    rad_start_date = num2date(radar.time['data'][0], radar.time['units'])
    dstr = rad_start_date.strftime('%Y%d%m_%H%M')
    fname = 'xsapr2_ena_quicklook_' + field + '_' + dstr + postfix
    fqn = os.path.join(odir, fname)
    return fqn

def xsapr2_auto_plot(quicklook_directory, radar, field, param_table, sweep=None, postfix=None):
    fig = plt.figure(figsize = [15,10])
    plot_xsapr2(radar, field = field, cmap=param_table[field]['cmap'],
               vmin=param_table[field]['vmin'],
                vmax=param_table[field]['vmax'], sweep = sweep, fig=fig)
    plt.savefig(gen_name(quicklook_directory, radar, field, postfix), dpi=300)
    plt.close(fig)

def make_plotting_paramaters(radar):
    maps = pyart.graph.cm
    nyq = radar.instrument_parameters['nyquist_velocity']['data'][0]

    standard_z = {'vmin' : -40, 'vmax' : 40, 'cmap': maps.NWSRef}
    standard_zdr = {'vmin' : -1, 'vmax' : 2, 'cmap': maps.LangRainbow12}
    standard_width = {'vmin' : 0, 'vmax' : nyq/2.0, 'cmap': maps.LangRainbow12}
    standard_snr = {'vmin' : -30, 'vmax' : 30, 'cmap': maps.NWSRef}
    standard_vel = {'vmin' : -nyq, 'vmax' : nyq, 'cmap': maps.NWSVel}
    standard_zto = {'vmin' : 0, 'vmax' : 1, 'cmap': maps.LangRainbow12}
    standard_phidp_180 = {'vmin' : -180, 'vmax' : 180, 'cmap': maps.LangRainbow12}
    standard_snr = {'vmin' : -80, 'vmax' : 10, 'cmap': maps.NWSRef}
    standard_pow = {'vmin' : -5, 'vmax' : 20, 'cmap': maps.NWSRef}


    plotting_table = {'reflectivity': standard_z,
                  'uncorrected_reflectivity': standard_z,
                  'uncorrected_differential_reflectivity_1': standard_zdr,
                  'differential_reflectivity_1': standard_zdr,
                  'corrected_spectral_width_vertical': standard_width,
                  'attenuation_corrected_reflectivity_horizontal': standard_z,
                  'spectral_width_horizontal': standard_width,
                  'unfolded_radial_velocity_horizontal': {'vmin' : -nyq*2.0, 'vmax' : nyq*2.0, 'cmap': maps.NWSVel},
                  'signal_to_noise_ratio_vertical': standard_snr,
                  'unfolded_differential_phase': {'vmin' : 0, 'vmax' : 180, 'cmap': maps.LangRainbow12},
                  'specific_differential_phase': {'vmin' : -1, 'vmax' : 8, 'cmap': maps.LangRainbow12},
                  'attenuation_corrected_differential_reflectivity': standard_zdr,
                  'cross_correlation_ratio_hv': {'vmin' : 0.5, 'vmax' : 1, 'cmap': maps.LangRainbow12},
                  'differential_reflectivity': standard_zdr,
                  'spectral_width_vertical': standard_width,
                  'radial_velocity_vertical': standard_vel,
                  'uncorrected_reflectivity_vertical': standard_z,
                  'normalized_coherent_power_horizontal': standard_zto,
                  'differential_phase': standard_phidp_180,
                  'clutter_map': {'vmin' : 0, 'vmax' : 10, 'cmap': maps.LangRainbow12},
                  'signal_to_noise_ratio_horizontal': standard_snr,
                  'radial_velocity_horizontal': standard_vel,
                  'corrected_spectral_width_horizontal': standard_width,
                  'attenuation_corrected_differential_reflectivity_1': standard_zdr,
                  'uncorrected_refelctivity_horizontal': standard_z,
                  'reflectivity_horizontal': standard_z,
                  'uncorrected_cross_correlation_ratio_hv':  {'vmin' : 0.5, 'vmax' : 1, 'cmap': maps.LangRainbow12},
                  'reflectivity_horizontal_vertical': standard_z,
                  'echo_id': {'vmin' : 0, 'vmax' : 10, 'cmap': maps.LangRainbow12},
                  'uncorrected_differential_reflectivity': standard_zdr,
                  'unfolded_radial_velocity_vertical': standard_vel,
                  'normalized_coherent_power_vertical': standard_zto,
                  'log_power_horizontal' : standard_pow,
                  'log_power_vertical' : standard_pow }
    return plotting_table