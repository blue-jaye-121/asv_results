import os
import xarray as xr 

import metpy.calc as mpcalc
from metpy.units import units


class TimeSuite: 
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.12"; 
    
    
    def setup_cache(self):
       base_path = os.path.dirname(__file__) # path to current file
       file_path = os.path.join(base_path, "..", "data_array_compressed.nc");
       file_path = os.path.abspath(file_path)
       ds = xr.open_dataset(file_path)
       return ds; 
    
    def setup(self, ds):
       self.pressureSlice = ds.isel(pressure = 0, time = 0)
       self.timeSlice = ds.isel(time = 0)
       self.profileSlice = ds.isel(time = 0, lat = 0, lon = 0)
       
    
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
        
    def time_shear_vorticity(self, pressureSlice):
        """Benchmarking shear vorticity on a 2d slice"""
        mpcalc.shear_vorticity(self.pressureSlice.uwind, self.pressureSlice.vwind); 
        
    # def time_absolute_momentum(self, pressureSlice): 
    #     """Benchmarking absolute momentum calculation on a 3d cube"""
    #     mpcalc.absolute_momentum(self.timeSlice.uwind, self.timeSlice.vwind); 
    
    def time_potential_vorticity_baroclinic(self, timeSlice):
        """Benchmarking potential vorticity baroclinic on a 3d cube"""
        mpcalc.potential_vorticity_baroclinic(self.timeSlice.theta, self.timeSlice.pressure, 
                                              self.timeSlice.uwind, self.timeSlice.vwind); 
        
    def time_inertal_advective_wind(self, timeSlice):
        """Benchmarking inertal advective wind calculation on a 3d cube"""
        mpcalc.inertial_advective_wind(self.timeSlice.uwind, self.timeSlice.vwind,
                                       self.timeSlice.uwind, self.timeSlice.vwind)
        
    def time_curvature_vorticity(self, timeSlice): 
        """Benchmarking the curvature vorticity calculation on a 3d cube"""
        mpcalc.curvature_vorticity(self.timeSlice.uwind, self.timeSlice.vwind); 
        
    def time_montgomery_streamfunction(self, pressureSlice):
        """Benchmarking the montgomery streamfunction calculation on a 2d grid"""
        mpcalc.montgomery_streamfunction(self.pressureSlice.height, self.pressureSlice.temperature);
        
    def time_wind_direction(self, timeSlice): 
        """Benchmarking the wind direction calculation on a 3d cube"""
        mpcalc.wind_direction(self.timeSlice.uwind, self.timeSlice.vwind); 
        
    def time_wind_components(self, timeSlice):
        """Benchmarking the wind components calculation on a 3d cube"""
        mpcalc.wind_components(self.timeSlice.windspeed, self.timeSlice.winddir)