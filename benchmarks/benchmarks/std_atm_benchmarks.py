import os
import xarray as xr

import metpy.calc as mpcalc; 
 
class TimeSuite:
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.11"; 
    
    def setup_cache(self):
       base_path = os.path.dirname(__file__) # path to current file
       file_path = os.path.join(base_path, "..", "data_array_compressed.nc");
       file_path = os.path.abspath(file_path)
       ds = xr.open_dataset(file_path)
       return ds; 
   
    def setup(self, ds):
       self.pressureSlice = ds.isel(pressure = 0, time = 0)
       self.timeSlice = ds.isel(time = 0)
       
    def time_height_to_pressure_std(self, timeSlice): 
        """Benchmarking the height to pressure calculation in a standard atmosphere on a 3d cube"""
        mpcalc.height_to_pressure_std(self.timeSlice.height)
      
    def time_pressure_to_height_std(self, timeSlice): 
        """Benchmarking the pressure to height calculation in a standard atmosphere on a 3d cube"""
        mpcalc.pressure_to_height_std(self.timeSlice.pressure)
