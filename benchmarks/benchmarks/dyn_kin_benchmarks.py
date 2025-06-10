import os
import xarray as xr 

import metpy.calc as mpcalc
from metpy.units import units


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
       
    
    def time_absolute_vorticity(self, pressureSlice): 
        """benchmarking absolute momentum calculation on a 2d surface"""
        mpcalc.absolute_vorticity(self.pressureSlice.uwind, self.pressureSlice.vwind); 
        
    def time_advection(self, timeSlice): 
        """Benchmarking the advection calculation of t on a 3d cube"""
        mpcalc.advection(self.timeSlice.temperature, self.timeSlice.uwind, self.timeSlice.vwind);
        
    def time_ageostrophic_wind(self, pressureSlice): 
        """Benchmarking ageostrophic wind calculation on a 2d surface"""
        mpcalc.ageostrophic_wind(self.pressureSlice.height, self.pressureSlice.uwind, self.pressureSlice.vwind); 
    
    def time_frontogenesis(self, pressureSlice):
        """Benchmarking the calculation of frontogenesis of a 2d field"""
        mpcalc.frontogenesis(self.pressureSlice.theta, self.pressureSlice.uwind, self.pressureSlice.vwind); 
    
    def time_potential_vorticity_barotropic(self, timeSlice):
        """Benchmarking the barotropic potential vorticity calculation on a cube"""
        mpcalc.potential_vorticity_barotropic(self.timeSlice.height, self.timeSlice.uwind, self.timeSlice.vwind); 
        
    def time_q_vector(self, pressureSlice): 
        """Benchmarking q vector calculation on a 2d slice"""
        mpcalc.q_vector(self.pressureSlice.uwind, self.pressureSlice.vwind, 
                        self.pressureSlice.temperature, self.pressureSlice.pressure); 
        
    def time_total_deformation(self, pressureSlice): 
        """Benchmarking total deformation calculation on a 2d slice"""
        mpcalc.total_deformation(self.pressureSlice.uwind, self.pressureSlice.vwind); 
        
    def time_vorticity(self, pressureSlice): 
        """Benchmarking vorticity calculation on a 2d slice"""
        mpcalc.vorticity(self.pressureSlice.uwind, self.pressureSlice.vwind); 