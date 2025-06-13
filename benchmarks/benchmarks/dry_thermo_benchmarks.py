import os
import xarray as xr

import metpy.calc as mpcalc; 
from metpy.units import units; 

 
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
        
    def time_density(self, pressureSlice): 
        """Benchmarking density calculation on a 2d surface"""
        mpcalc.density(self.pressureSlice.pressure, self.pressureSlice.temperature, self.pressureSlice.mixing_ratio); 
        
    def time_height_to_geopotential(self, timeSlice): 
        """Benchmarking the height to geopotenial calculation on a 3d cube"""
        mpcalc.height_to_geopotential(self.timeSlice.height); 
        
    def time_potential_temperature(self, timeSlice):
        """Benchmarking the potential temperature calculation on a 3d cube"""
        mpcalc.potential_temperature(self.timeSlice.pressure, self.timeSlice.temperature); 
        
    def time_static_stability(self, timeSlice): 
        """Benchmarking static stability calculation on a 3d cube"""
        mpcalc.static_stability(self.timeSlice.pressure, self.timeSlice.temperature); 
        
    def time_thickness_hydrostatic(self, timeSlice): 
        """Benchmarking hydrostatic thickness calculation on a 3d cube"""
        mpcalc.thickness_hydrostatic(self.timeSlice.pressure, self.timeSlice.temperature, self.timeSlice.mixing_ratio); 
        
    def time_dry_lapse(self, timeSlice):
        """Benchmarking the dry lapse calculation on a 3d cube"""
        mpcalc.dry_lapse(self.timeSlice.pressure, self.timeSlice.temperature); 
        
    def time_sigma_to_pressure(self, timeSlice):
        """Benchmarking the sigma to pressure calculation on a 3d cube"""
        mpcalc.sigma_to_pressure(self.timeSlice.sigma, self.timeSlice.pressure[0], self.timeSlice.pressure[49])
        
    def time_geopotential_to_height(self, timeSlice): 
        """Benchmarking the geopotential to height calculation on a 3d cube"""
        mpcalc.geopotential_to_height(self.timeSlice.geopotential); 
        
    def time_add_pressure_to_height(self, timeSlice): 
        """Benchmarking adding pressure to height on a 3d cube"""
        mpcalc.add_pressure_to_height(self.timeSlice.height, self.timeSlice.pressure)
        
    def time_add_height_to_pressure(self, timeSlice): 
        """Benchmarking adding height to pressure on a 3d cube"""
        mpcalc.add_height_to_pressure(self.timeSlice.pressure.values * units('hPa'), 
                                      self.timeSlice.height.values * units('km')); 