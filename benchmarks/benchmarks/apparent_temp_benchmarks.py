import os
import xarray as xr

import metpy.calc as mpcalc; 

 
class TimeSuite:
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.10"; 
    
    def setup_cache(self):
       base_path = os.path.dirname(__file__) # path to current file
       file_path = os.path.join(base_path, "..", "data_array_compressed.nc");
       file_path = os.path.abspath(file_path)
       ds = xr.open_dataset(file_path)
       return ds; 
   
    def setup(self, ds):
       self.pressureSlice = ds.isel(pressure = 0, time = 0)
       self.timeSlice = ds.isel(time = 0)
       
       
    def time_apparent_temperature(self, pressureSlice): 
        """Benchmarking calculating apparent temperature on a 2d grid"""
        mpcalc.apparent_temperature(self.pressureSlice.temperature, self.pressureSlice.relative_humidity, 
                                    self.pressureSlice.windspeed); 
        
    def time_heat_index(self, timeSlice): 
        """Benchmarking calculating heat index on a 3d cube"""
        mpcalc.heat_index(self.timeSlice.temperature, self.timeSlice.relative_humidity); 
        
    def time_windchill(self, timeSlice): 
        """Benchmarking calculating windchill on a 3d cube"""
        mpcalc.windchill(self.timeSlice.temperature, self.timeSlice.windspeed)