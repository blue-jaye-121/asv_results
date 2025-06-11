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
       self.ds = ds; 
       self.pressureSlice = ds.isel(pressure = 0, time = 0)
       self.timeSlice = ds.isel(time = 0)
       self.lineSlice = ds.isel(pressure = 0, time = 0, lat = 0); 
       self.profileSlice = ds.isel(time = 0, lat = 0, lon = 0)
       
    def time_find_intersections(self, lineSlice): 
        """benchmarking finding intersections calculation"""
        mpcalc.find_intersections(self.lineSlice.lon, self.lineSlice.temperature, self.lineSlice.dewpoint); 
        
    def time_find_peaks(self, pressureSlice):
        """Benchmarking finding peaks of 2d dewpoint slice"""
        mpcalc.find_peaks(self.pressureSlice.dewpoint); 
        
    def time_get_perturbation(self, ds): 
        """Benchmarking getting the perturbation of a time series"""
        mpcalc.get_perturbation(self.ds.temperature)
        
    def time_peak_persistence(self, pressureSlice): 
        """Benchmarking calculating persistence of of maxima point in 3d"""
        mpcalc.peak_persistence(self.pressureSlice.dewpoint); 
