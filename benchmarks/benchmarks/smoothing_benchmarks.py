import os
import xarray as xr

import metpy.calc as mpcalc; 
import numpy as np; 
 
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
       
    def time_smooth_gaussian(self, pressureSlice): 
        """Benchmarking the gaussian smoothing of a 2d grid"""
        mpcalc.smooth_gaussian(self.pressureSlice.relative_humidity, 5); 
        
    def time_smooth_window(self, pressureSlice):
        """Benchmarking the window smoothing of a 2d grid"""
        mpcalc.smooth_window(self.pressureSlice.relative_humidity, np.diag(np.ones(5)))
        
    def time_smooth_rectangular(self, pressureSlice): 
        """Benchmarking the rectangular smoothing of a 2d grid"""
        mpcalc.smooth_rectangular(self.pressureSlice.relative_humidity, (3, 7)); 
        
    def time_smooth_circular(self, pressureSlice): 
        """Benchmarking the circular smoothing of a 2d grid"""
        mpcalc.smooth_circular(self.pressureSlice.relative_humidity, 2);
        
    def time_smooth_n_point(self, pressureSlice): 
        """Benchmarking the 5 point smoothing of a 2d grid"""
        mpcalc.smooth_n_point(self.pressureSlice.relative_humidity); 
