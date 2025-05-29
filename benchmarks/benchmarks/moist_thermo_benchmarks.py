import numpy as np
import xarray as xr

from metpy.calc import (virtual_temperature, dewpoint, relative_humidity_from_mixing_ratio, 
                        dewpoint_from_relative_humidity, moist_lapse, precipitable_water, wet_bulb_temperature, scale_height); 
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
    
    
    def setup(self): 
        self.mixingRatio = np.array([8, 7, 9, 10, 11, 12, 13, 14, 15, 16]); #dimensionless
        self.t = np.array([22.2, 14.6, 12., 9.4, 7., -38., 13.3, 12.7, 2.3, 23.4]) * units.celsius
        self.randomT = np.random.uniform(low=0.0, high=24.0, size=100) * units.celsius; 
        self.randomMixingRatio = np.random.uniform(low = 0.0, high = 40.0, size=100); #dimensionless
        self.pressure = np.linspace(1000, 1, 100) * units.hPa; 
        self.randomTd = np.random.uniform(low = 0.0, high = 20.0, size=100) * units.degC
        self.ds = index_xarray_data()
        self.slice = self.ds.isel(isobaric=0)
        
    def time_virtual_temperature(self): 
        """Benchmark virtual temperature for one value."""
        virtual_temperature(self.t[0], self.mixingRatio[0] * units("g/kg"));
        
        
    def time_virtual_temperature_100_values(self): 
        """Benchmarking the virtual temperature for 100 array values"""
        virtual_temperature(self.randomT, self.randomMixingRatio * units("g/kg")); 
    
    def time_virtual_temperature_grid(self): 
        """Benchmark virtual temperature on a grid"""
        virtual_temperature(self.slice.temperature, self.slice.mixingRatio * units("g/kg")); 
        
    def time_dewpoint_grid(self): 
        """Benchmarking dewpoint from vapor pressure on a grid"""
        dewpoint(self.slice.vaporPressure); 
        
    def time_rh_from_mixing_ratio_grid(self):
        """Benchmarking relative humidity from mixing ratio on a grid"""
        relative_humidity_from_mixing_ratio(self.slice.pressure, self.slice.temperature, self.slice.mixingRatio); 
    
    def time_dewpoint_from_rh_grid(self):
        """Benchmarking relative humidity from calculated rh on a grid"""
        dewpoint_from_relative_humidity(self.slice.temperature, self.slice.relativeHumidity);
        
    def time_precipitable_water(self): 
        """Benchmarking precipitable water calculation"""
        precipitable_water(self.pressure, self.randomTd);
        
    def time_wet_bulb_temperature_grid(self):
        """Benchmarking wet bulb temperature calculation"""
        wet_bulb_temperature(self.pressure[0], self.t[0], self.randomTd[0]); 
        
        
    def time_scale_height(self): 
        """Benchmarking the calculation for the scale height of a layer"""
        scale_height(self.t[0], self.t[5]); 