import os
import xarray as xr


import metpy.calc as mpcalc; 


class TimeSuite: 
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.06";
    
    def setup_cache(self):
       base_path = os.path.dirname(__file__) # path to current file
       file_path = os.path.join(base_path, "..", "data_array_compressed.nc");
       file_path = os.path.abspath(file_path)
       ds = xr.open_dataset(file_path)
       return ds; 
   
    def setup(self, ds):
       self.timeSlice = ds.isel(time = 0)
    
        
    def time_brunt_vaisala_frequency(self, timeSlice): 
        """Benchmark Brunt Vaisala frequency calculation - on a grid"""
        mpcalc.brunt_vaisala_frequency(self.timeSlice.height, self.timeSlice.theta); 
        
    def time_gradient_richardson_number(self, timeSlice): 
        """Benchmark Gradient Richardson Number on a grid"""
        mpcalc.gradient_richardson_number(self.timeSlice.height, self.timeSlice.theta,
                                         self.timeSlice.uwind, self.timeSlice.vwind)