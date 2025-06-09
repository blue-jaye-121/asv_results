import os
import xarray as xr

import metpy.calc as mpcalc;  


class TimeSuite: 
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.09"; 
    
    def setup_cache(self):
       base_path = os.path.dirname(__file__) # path to current file
       file_path = os.path.join(base_path, "..", "data_array_compressed.nc");
       file_path = os.path.abspath(file_path)
       ds = xr.open_dataset(file_path)
       return ds; 
   
    def setup(self, ds):
       self.pressureSlice = ds.isel(pressure = 0, time = 0)
       self.timeSlice = ds.isel(time = 0)
       self.upperSlice = ds.isel(pressure = 49, time = 0)
        
    def time_virtual_temperature(self, timeSlice): 
        """Benchmark virtual temperature on a 3d cube."""
        mpcalc.virtual_temperature(self.timeSlice.temperature, self.timeSlice.mixing_ratio);
        
    def time_dewpoint(self, timeSlice): 
        """Benchmarking dewpoint from vapor pressure on a 3d cube"""
        mpcalc.dewpoint(self.timeSlice.vapor_pressure); 
        
    def time_rh_from_mixing_ratio(self, timeSlice):
        """Benchmarking relative humidity from mixing ratio on a 3d cube"""
        mpcalc.relative_humidity_from_mixing_ratio(self.timeSlice.pressure, self.timeSlice.temperature, self.timeSlice.mixing_ratio); 
    
    def time_dewpoint_from_rh(self, timeSlice):
        """Benchmarking dewpoint from calculated on a 3d cube"""
        mpcalc.dewpoint_from_relative_humidity(self.timeSlice.temperature, self.timeSlice.relative_humidity);
        
    def time_precipitable_water(self, timeSlice): 
        """Benchmarking precipitable water calculation for one column"""
        mpcalc.precipitable_water(self.timeSlice.pressure, self.timeSlice.dewpoint[0][0]);
        
    def time_wet_bulb_temperature(self, pressureSlice):
        """Benchmarking wet bulb temperature calculation on on a cube"""
        mpcalc.wet_bulb_temperature(self.pressureSlice.pressure, self.pressureSlice.temperature, self.pressureSlice.dewpoint); 
        
        
    def time_scale_height(self, pressureSlice): 
        """Benchmarking the calculation for the scale height of a layer for 2 surfaces"""
        mpcalc.scale_height(self.upperSlice.temperature, self.pressureSlice.temperature); 