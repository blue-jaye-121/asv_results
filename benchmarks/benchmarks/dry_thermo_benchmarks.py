import numpy as np
import xarray as xr

import metpy.calc as mpcalc; 
from metpy.units import units

def index_xarray_data():
     """Create data for testing that index calculations work with xarray data."""
     pressure = xr.DataArray([850., 700., 500.], dims=('isobaric',), attrs={'units': 'hPa'})
     temp = xr.DataArray([[[[296., 295., 294.], [293., 292., 291.]],
                           [[286., 285., 284.], [283., 282., 281.]],
                           [[276., 275., 274.], [273., 272., 271.]]]] * units.K,
                         dims=('time', 'isobaric', 'y', 'x'))
     
     mixingRatio = xr.DataArray([[[[9., 9., 9.], [10., 10., 10.]],
                           [[11., 11., 11.], [11., 11., 11.]],
                           [[12., 12., 270.], [12., 12., 12.]]]],
                         dims=('time', 'isobaric', 'y', 'x'))
     
     vaporPressure = xr.DataArray([[[[30., 30., 30.], [28.,28.,28.]], 
                                     [[27., 26., 27.], [25., 24., 24.]],
                                     [[23., 19., 23.], [18., 16., .20]]]] * units.hPa,
                                   dims=('time', 'isobaric', 'y', 'x'))
     rh = xr.DataArray([[[[30., 30., 30.], [28.,28.,28.]], 
                                     [[27., 26., 27.], [25., 24., 24.]],
                                     [[23., 19., 23.], [18., 16., .20]]]] * units.percent,
                                   dims=('time', 'isobaric', 'y', 'x'))
     
     dewpoint = xr.DataArray([[[[250., 250., 250.], [240., 240., 240.]],
                           [[260., 260., 260.], [240., 240., 240.]],
                           [[250., 250., 250.], [260., 260., 260.]]]] * units.K,
                         dims=('time', 'isobaric', 'y', 'x'))
     
     return xr.Dataset({'temperature': temp,  'mixingRatio': mixingRatio, 'vaporPressure': vaporPressure,
                        'pressure': pressure, 'relativeHumidity': rh, 'dewpoint':dewpoint},
                       coords={'isobaric': pressure, 'time': ['2020-01-01T00:00Z']});
 
class TimeSuite:
        #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.03"; 
    
    
    def setup(self): 
        self.mixingRatio = np.array([8, 7, 9, 10, 11, 12, 13, 14, 15, 16]); #dimensionless
        self.t = np.array([22.2, 14.6, 12., 9.4, 7., -38., 13.3, 12.7, 2.3, 23.4]) * units.celsius
        self.randomT = np.random.uniform(low=0.0, high=24.0, size=100) * units.celsius; 
        self.randomMixingRatio = np.random.uniform(low = 0.0, high = 40.0, size=100); #dimensionless
        self.pressure = np.linspace(1000, 1, 100) * units.hPa; 
        self.height = np.linspace(0, 10000, 10000) * units.m; 
        self.randomTd = np.random.uniform(low = 0.0, high = 20.0, size=100) * units.degC
        self.ds = index_xarray_data()
        self.slice = self.ds.isel(isobaric=0)
        
    def time_density_grid(self): 
        """Benchmarking density calculation on a grid"""
        mpcalc.density(self.slice.pressure, self.slice.temperature, self.slice.mixingRatio); 
        
    def time_height_to_geopotential(self): 
        """Benchmarking the height to geopotenial calculation with 10000 steps"""
        mpcalc.height_to_geopotential(self.height); 
        
    def time_potential_temperature_grid(self):
        """Benchmarking the potential temperature calculation on a grid"""
        mpcalc.potential_temperature(self.slice.pressure, self.slice.temperature); 
        
    def time_static_stability_grid(self): 
        """Benchmarking static stability calculation on a grid"""
        mpcalc.static_stability(self.pressure, self.randomT); 
        
    def time_thickness_hydrostatic(self): 
        """Benchmarking hydrostatic thickness calculation"""
        mpcalc.thickness_hydrostatic(self.pressure, self.randomT, self.randomMixingRatio); 
        
    def time_dry_lapse(self):
        """Benchmarking the dry lapse calculation"""
        mpcalc.dry_lapse(self.pressure, self.randomT[0]); 