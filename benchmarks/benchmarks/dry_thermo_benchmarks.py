import os
import xarray as xr

import metpy.calc as mpcalc; 

 
class TimeSuite:
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.09"; 
    
    def setup_cache(self):
       base_path = os.path.dirname(__file__) # path to current file
       file_path = os.path.join(base_path, "..", "data_array.nc"); 
       ds = xr.open_dataset(file_path)
       return ds; 
   
    def setup(self, ds):
       self.pressureSlice = ds.isel(pressure = 0, time = 0)
       self.timeSlice = ds.isel(time = 0)
        
    def time_density(self, pressureSlice): 
        """Benchmarking density calculation on a 2d surface"""
        mpcalc.density(self.pressureSlice.pressure, self.pressureSlice.temperature, self.pressureSlice.mixing_ratio); 
        
    def time_height_to_geopotential(self, timeSlice): 
        """Benchmarking the height to geopotenial calculation on a 3d cube"""
        mpcalc.height_to_geopotential(self.timeSlice.height); 
        
    def time_potential_temperature(self):
        """Benchmarking the potential temperature calculation on a 3d cube"""
        mpcalc.potential_temperature(self.timeSlice.pressure, self.timeSlice.temperature); 
        
    def time_static_stability(self): 
        """Benchmarking static stability calculation on a 3d cube"""
        mpcalc.static_stability(self.timeSlice.pressure, self.timeSlice.temperature); 
        
    def time_thickness_hydrostatic(self): 
        """Benchmarking hydrostatic thickness calculation on a 3d cube"""
        mpcalc.thickness_hydrostatic(self.timeSlice.pressure, self.timeSlice.temperature, self.timeSlice.mixing_ratio); 
        
    def time_dry_lapse(self):
        """Benchmarking the dry lapse calculation on a 3d cube"""
        mpcalc.dry_lapse(self.timeSlice.pressure, self.timeSlice.temperature); 