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
        self.timeSlice = ds.isel(time = 0)
        self.profileSlice = ds.isel(lat = 25, lon = 25, time = 0)
        self.parcelProfile = mpcalc.parcel_profile(self.profileSlice.pressure, 
                                                  self.profileSlice.temperature[0], 
                                                  self.profileSlice.dewpoint[0]); 
        
    def time_bulk_shear(self, profileSlice): 
        """Benchmarking calculating the bulk shear of a profile"""
        mpcalc.bulk_shear(self.profileSlice.pressure, self.profileSlice.uwind, self.profileSlice.vwind); 
        
    def time_ccl(self, profileSlice): 
        """Benchmarking calculating the convective condensation level of a profile"""
        mpcalc.ccl(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint); 
        
    def time_parcel_profile(self, profileSlice): 
        """Benchmarking the atmospheric parcel profile for one profile"""
        mpcalc.parcel_profile(self.profileSlice.pressure, self.profileSlice.temperature[0], self.profileSlice.dewpoint[0]);
        
    def time_most_unstable_parcel(self, profileSlice): 
        """Benchmarking the calculation to find the most unstable parcel"""
        mpcalc.most_unstable_parcel(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint); 
        
    def time_cape_cin(self, profileSlice): 
        """Benchmarking cape_cin calculation for one profile"""
        mpcalc.cape_cin(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint, self.parcelProfile); 
    
    def time_lcl(self, timeSlice):
        """Benchmarks lcl on a 3d cube - many profiles"""
        mpcalc.lcl(self.timeSlice.pressure, self.timeSlice.temperature, self.timeSlice.dewpoint); 
    
    def time_el(self, profileSlice): 
        """Benchmarks el calculation on one profile"""
        mpcalc.el(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint); 
        
        
        
    