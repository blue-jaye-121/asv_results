# Copyright (c) 2017,2019 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""Test the `indices` module."""

from datetime import datetime

import numpy as np
import pytest
import xarray as xr

from metpy.calc import (bulk_shear, bunkers_storm_motion, corfidi_storm_motion, critical_angle,
                        mean_pressure_weighted, precipitable_water, significant_tornado,
                        supercell_composite, weighted_continuous_average)
from metpy.testing import (assert_almost_equal, assert_array_almost_equal, get_upper_air_data,
                           version_check)
from metpy.units import concatenate, units


def test_precipitable_water():
    """Test precipitable water with observed sounding."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    pw = precipitable_water(data['pressure'], data['dewpoint'], top=400 * units.hPa)
    truth = 22.58809193 * units.millimeters
    assert_array_almost_equal(pw, truth, 4)


def test_precipitable_water_no_bounds():
    """Test precipitable water with observed sounding and no bounds given."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    dewpoint = data['dewpoint']
    pressure = data['pressure']
    inds = pressure >= 400 * units.hPa
    pw = precipitable_water(pressure[inds], dewpoint[inds])
    truth = 22.58809193 * units.millimeters
    assert_array_almost_equal(pw, truth, 4)


def test_precipitable_water_bound_error():
    """Test with no top bound given and data that produced floating point issue #596."""
    pressure = np.array([993., 978., 960.5, 927.6, 925., 895.8, 892., 876., 45.9, 39.9, 36.,
                         36., 34.3]) * units.hPa
    dewpoint = np.array([25.5, 24.1, 23.1, 21.2, 21.1, 19.4, 19.2, 19.2, -87.1, -86.5, -86.5,
                         -86.5, -88.1]) * units.degC
    pw = precipitable_water(pressure, dewpoint)
    truth = 89.78451311253484 * units('millimeters')
    assert_almost_equal(pw, truth, 5)


def test_precipitable_water_nans():
    """Test that PW returns appropriate number if NaNs are present."""
    pressure = np.array([1001, 1000, 997, 977.9, 977, 957, 937.8, 925, 906, 899.3, 887, 862.5,
                         854, 850, 800, 793.9, 785, 777, 771, 762, 731.8, 726, 703, 700, 655,
                         630, 621.2, 602, 570.7, 548, 546.8, 539, 513, 511, 485, 481, 468,
                         448, 439, 424, 420, 412]) * units.hPa
    dewpoint = np.array([-25.1, -26.1, -26.8, np.nan, -27.3, -28.2, np.nan, -27.2, -26.6,
                        np.nan, -27.4, np.nan, -23.5, -23.5, -25.1, np.nan, -22.9, -17.8,
                        -16.6, np.nan, np.nan, -16.4, np.nan, -18.5, -21., -23.7, np.nan,
                        -28.3, np.nan, -32.6, np.nan, -33.8, -35., -35.1, -38.1, -40.,
                        -43.3, -44.6, -46.4, -47., -49.2, -50.7]) * units.degC
    pw = precipitable_water(pressure, dewpoint)
    truth = 3.997385016573651 * units.mm
    assert_almost_equal(pw, truth, 5)


def test_precipitable_water_descriptive_bound_error():
    """Test that error is raised when bound is outside profile after nan have been removed."""
    pressure = np.array([1001, 1000, 997, 977.9, 977, 957, 937.8, 925, 906, 899.3, 887, 862.5,
                         854, 850, 800, 793.9, 785, 777, 771, 762, 731.8, 726, 703, 700, 655,
                         630, 621.2, 602, 570.7, 548, 546.8, 539, 513, 511, 485, 481, 468,
                         448, 439, 424, 420, 412]) * units.hPa
    dewpoint = np.array([np.nan, np.nan, -26.8, np.nan, -27.3, -28.2, np.nan, -27.2, -26.6,
                        np.nan, -27.4, np.nan, -23.5, -23.5, -25.1, np.nan, -22.9, -17.8,
                        -16.6, np.nan, np.nan, -16.4, np.nan, -18.5, -21., -23.7, np.nan,
                        -28.3, np.nan, -32.6, np.nan, -33.8, -35., -35.1, -38.1, -40.,
                        -43.3, -44.6, -46.4, np.nan, np.nan, np.nan]) * units.degC

    # Top bound is above highest pressure in profile
    with pytest.raises(ValueError, match='The pressure and dewpoint profile ranges from'):
        precipitable_water(pressure, dewpoint, top=units.Quantity(415, 'hPa'))

    # Bottom bound is below lowest pressure in profile
    with pytest.raises(ValueError, match='The pressure and dewpoint profile ranges from'):
        precipitable_water(pressure, dewpoint, bottom=units.Quantity(999, 'hPa'))


def test_mean_pressure_weighted():
    """Test pressure-weighted mean wind function with vertical interpolation."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u, v = mean_pressure_weighted(data['pressure'],
                                  data['u_wind'],
                                  data['v_wind'],
                                  height=data['height'],
                                  depth=6000 * units('meter'))
    assert_almost_equal(u, 6.0208700094534775 * units('m/s'), 7)
    assert_almost_equal(v, 7.966031839967931 * units('m/s'), 7)


def test_mean_pressure_weighted_temperature():
    """Test pressure-weighted mean temperature function with vertical interpolation."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    t, = mean_pressure_weighted(data['pressure'],
                                data['temperature'],
                                height=data['height'],
                                depth=6000 * units('meter'))
    assert_almost_equal(t, 281.535035296836 * units('kelvin'), 7)


def test_mean_pressure_weighted_elevated():
    """Test pressure-weighted mean wind function with a base above the surface."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u, v = mean_pressure_weighted(data['pressure'],
                                  data['u_wind'],
                                  data['v_wind'],
                                  height=data['height'],
                                  depth=3000 * units('meter'),
                                  bottom=data['height'][0] + 3000 * units('meter'))
    assert_almost_equal(u, 8.270829843626476 * units('m/s'), 7)
    assert_almost_equal(v, 1.7392601775853547 * units('m/s'), 7)


def test_weighted_continuous_average():
    """Test pressure-weighted mean wind function with vertical interpolation."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u, v = weighted_continuous_average(data['pressure'],
                                       data['u_wind'],
                                       data['v_wind'],
                                       height=data['height'],
                                       depth=6000 * units('meter'))
    assert_almost_equal(u, 6.644137766806087 * units('m/s'), 7)
    assert_almost_equal(v, 6.900543760612305 * units('m/s'), 7)


@pytest.mark.xfail(condition=version_check('pint<0.21'), reason='hgrecco/pint#1593')
def test_weighted_continuous_average_temperature():
    """Test pressure-weighted mean temperature function with vertical interpolation."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    t, = weighted_continuous_average(data['pressure'],
                                     data['temperature'],
                                     height=data['height'],
                                     depth=6000 * units('meter'))
    assert_almost_equal(t, 279.07450928270185 * units('kelvin'), 7)


def test_weighted_continuous_average_elevated():
    """Test pressure-weighted mean wind function with a base above the surface."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u, v = weighted_continuous_average(data['pressure'],
                                       data['u_wind'],
                                       data['v_wind'],
                                       height=data['height'],
                                       depth=3000 * units('meter'),
                                       bottom=data['height'][0] + 3000 * units('meter'))
    assert_almost_equal(u, 8.279561625494285 * units('m/s'), 7)
    assert_almost_equal(v, 1.616638856115755 * units('m/s'), 7)


def test_precipitable_water_xarray():
    """Test precipitable water with xarray input."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    press = xr.DataArray(data['pressure'].m, attrs={'units': str(data['pressure'].units)})
    dewp = xr.DataArray(data['dewpoint'], dims=('press',), coords=(press,))
    pw = precipitable_water(press, dewp, top=400 * units.hPa)
    truth = 22.58809193 * units.millimeters
    assert_almost_equal(pw, truth)


def test_bunkers_motion():
    """Test Bunkers storm motion with observed sounding."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    motion = concatenate(bunkers_storm_motion(data['pressure'],
                         data['u_wind'], data['v_wind'],
                         data['height']))
    truth = [2.062733, 0.96246913, 11.22554254, 12.83861839, 6.64413777,
             6.90054376] * units('m/s')
    assert_almost_equal(motion.flatten(), truth, 8)


def test_corfidi_motion():
    """Test corfidi MCS motion with observed sounding."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    motion_full = concatenate(corfidi_storm_motion(data['pressure'],
                                                   data['u_wind'], data['v_wind']))
    truth_full = [20.60174457, -22.38741441,
                  38.32734963, -11.90040377] * units('kt')
    assert_almost_equal(motion_full.flatten(), truth_full, 8)


def test_corfidi_motion_override_llj():
    """Test corfidi MCS motion with overridden LLJ."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    motion_override = concatenate(corfidi_storm_motion(data['pressure'],
                                                       data['u_wind'], data['v_wind'],
                                                       u_llj=0 * units('kt'),
                                                       v_llj=0 * units('kt')))
    truth_override = [17.72560506, 10.48701063,
                      35.45121012, 20.97402126] * units('kt')
    assert_almost_equal(motion_override.flatten(), truth_override, 8)

    with pytest.raises(ValueError):
        corfidi_storm_motion(data['pressure'], data['u_wind'],
                             data['v_wind'], u_llj=10 * units('kt'))

    with pytest.raises(ValueError):
        corfidi_storm_motion(data['pressure'], data['u_wind'],
                             data['v_wind'], v_llj=10 * units('kt'))


def test_corfidi_corfidi_llj_unaivalable():
    """Test corfidi MCS motion where the LLJ is unailable."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    with pytest.raises(ValueError):
        corfidi_storm_motion(data['pressure'][6:], data['u_wind'][6:], data['v_wind'][6:])


def test_corfidi_corfidi_cloudlayer_trimmed():
    """Test corfidi MCS motion where sounding does not include the entire cloud layer."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    motion_no_top = concatenate(corfidi_storm_motion(data['pressure'][:37],
                                                     data['u_wind'][:37], data['v_wind'][:37]))
    truth_no_top = [20.40419260, -21.43467629,
                    37.93224569, -9.99492754] * units('kt')
    assert_almost_equal(motion_no_top.flatten(), truth_no_top, 8)


def test_corfidi_motion_with_nans():
    """Test corfidi MCS motion with observed sounding with nans."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u_with_nans = data['u_wind']
    u_with_nans[6:10] = np.nan
    v_with_nans = data['v_wind']
    v_with_nans[6:10] = np.nan
    motion_with_nans = concatenate(corfidi_storm_motion(data['pressure'],
                                                        u_with_nans, v_with_nans))
    truth_with_nans = [20.01078763, -22.65208606,
                       37.14543575, -12.42974709] * units('kt')
    assert_almost_equal(motion_with_nans.flatten(), truth_with_nans, 8)


def test_bunkers_motion_with_nans():
    """Test Bunkers storm motion with observed sounding."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u_with_nan = data['u_wind']
    u_with_nan[24:26] = np.nan
    v_with_nan = data['v_wind']
    v_with_nan[24:26] = np.nan
    motion = concatenate(bunkers_storm_motion(data['pressure'],
                         u_with_nan, v_with_nan,
                         data['height']))
    truth = [2.09232447, 0.97612357, 11.25513401, 12.85227283, 6.67372924,
             6.9141982] * units('m/s')
    assert_almost_equal(motion.flatten(), truth, 8)


def test_bulk_shear():
    """Test bulk shear with observed sounding."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u, v = bulk_shear(data['pressure'], data['u_wind'],
                      data['v_wind'], height=data['height'],
                      depth=6000 * units('meter'))
    truth = [29.899581266946115, -14.389225800205509] * units('knots')
    assert_almost_equal(u.to('knots'), truth[0], 8)
    assert_almost_equal(v.to('knots'), truth[1], 8)


def test_bulk_shear_no_depth():
    """Test bulk shear with observed sounding and no depth given. Issue #568."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u, v = bulk_shear(data['pressure'], data['u_wind'],
                      data['v_wind'], height=data['height'])
    truth = [20.225018939, 22.602359692] * units('knots')
    assert_almost_equal(u.to('knots'), truth[0], 8)
    assert_almost_equal(v.to('knots'), truth[1], 8)


def test_bulk_shear_elevated():
    """Test bulk shear with observed sounding and a base above the surface."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    u, v = bulk_shear(data['pressure'], data['u_wind'],
                      data['v_wind'], height=data['height'],
                      bottom=data['height'][0] + 3000 * units('meter'),
                      depth=3000 * units('meter'))
    truth = [0.9655943923302139, -3.8405428777944466] * units('m/s')
    assert_almost_equal(u, truth[0], 8)
    assert_almost_equal(v, truth[1], 8)


def test_supercell_composite():
    """Test supercell composite function."""
    mucape = [2000., 1000., 500., 2000.] * units('J/kg')
    esrh = [400., 150., 45., 45.] * units('m^2/s^2')
    ebwd = [30., 15., 5., 5.] * units('m/s')
    truth = [16., 2.25, 0., 0.]
    supercell_comp = supercell_composite(mucape, esrh, ebwd)
    assert_array_almost_equal(supercell_comp, truth, 5)


def test_supercell_composite_scalar():
    """Test supercell composite function with a single value."""
    mucape = 2000. * units('J/kg')
    esrh = 400. * units('m^2/s^2')
    ebwd = 30. * units('m/s')
    truth = 16.
    supercell_comp = supercell_composite(mucape, esrh, ebwd)
    assert_almost_equal(supercell_comp, truth, 6)


def test_sigtor():
    """Test significant tornado parameter function."""
    sbcape = [2000., 2000., 2000., 2000., 3000, 4000] * units('J/kg')
    sblcl = [3000., 1500., 500., 1500., 1500, 800] * units('meter')
    srh1 = [200., 200., 200., 200., 300, 400] * units('m^2/s^2')
    shr6 = [20., 5., 20., 35., 20., 35] * units('m/s')
    truth = [0., 0, 1.777778, 1.333333, 2., 10.666667]
    sigtor = significant_tornado(sbcape, sblcl, srh1, shr6)
    assert_almost_equal(sigtor, truth, 6)


def test_sigtor_scalar():
    """Test significant tornado parameter function with a single value."""
    sbcape = 4000 * units('J/kg')
    sblcl = 800 * units('meter')
    srh1 = 400 * units('m^2/s^2')
    shr6 = 35 * units('m/s')
    truth = 10.666667
    sigtor = significant_tornado(sbcape, sblcl, srh1, shr6)
    assert_almost_equal(sigtor, truth, 6)


def test_critical_angle():
    """Test critical angle with observed sounding."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    ca = critical_angle(data['pressure'], data['u_wind'],
                        data['v_wind'], data['height'],
                        u_storm=0 * units('m/s'), v_storm=0 * units('m/s'))
    truth = [140.0626637513269] * units('degrees')
    assert_almost_equal(ca, truth, 8)


def test_critical_angle_units():
    """Test critical angle with observed sounding and different storm motion units."""
    data = get_upper_air_data(datetime(2016, 5, 22, 0), 'DDC')
    # Set storm motion in m/s
    ca_ms = critical_angle(data['pressure'], data['u_wind'],
                           data['v_wind'], data['height'],
                           u_storm=10 * units('m/s'), v_storm=10 * units('m/s'))
    # Set same storm motion in kt and m/s
    ca_kt_ms = critical_angle(data['pressure'], data['u_wind'],
                              data['v_wind'], data['height'],
                              u_storm=10 * units('m/s'), v_storm=19.4384449244 * units('kt'))
    # Make sure the resulting critical angles are equal
    assert_almost_equal(ca_ms, ca_kt_ms, 8)
