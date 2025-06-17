import os
import xarray as xr

import metpy.calc as mpcalc; 
import metpy.interpolate as mpinter; 

 
class TimeSuite:
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.17"; 
    
    def setup_cache(self):
       base_path = os.path.dirname(__file__) # path to current file
       file_path = os.path.join(base_path, "..", "data_array_compressed.nc");
       file_path = os.path.abspath(file_path)
       ds = xr.open_dataset(file_path)
       ds = ds.metpy.parse_cf()
       return ds; 
   
    def setup(self, ds):
       self.pressureSlice = ds.isel(pressure = 0, time = 0)
       self.timeSlice = ds.isel(time = 0)
       start = (30., 260.)
       end = (40., 270.)
       self.cross = mpinter.cross_section(self.timeSlice, start, end).set_coords(('lat', 'lon'))
       
    def time_geospatial_gradient(self, pressureSlice):
        """Benchmarking calculating the geospatial gradient of temp on a 2d array"""
        mpcalc.geospatial_gradient(self.pressureSlice.temperature); 
        
    def time_geospatial_laplacian(self, pressureSlice): 
        """Benchmarking calculating the geospatial laplacian of temp on a 2d array"""
        mpcalc.geospatial_laplacian(self.pressureSlice.temperature); 
        
    def time_gradient(self, timeSlice): 
        """Benchmarking calculating the gradient of temp on a 3d cube"""
        mpcalc.gradient(self.timeSlice.temperature); 
        
    def time_vector_derivative(self, pressureSlice): 
        """Benchmarking calculating the vector derivative of wind on a 2d slice"""
        mpcalc.vector_derivative(self.pressureSlice.uwind, self.pressureSlice.vwind); 
        
    def time_tangential_component(self, cross):
        """Benchmarking calculation of the tangential component of wind on a slice"""
        mpcalc.tangential_component(self.cross.uwind, self.cross.vwind); 
    
    def time_cross_section_components(self, cross):
        """Benchmarking the cross section components of a wind grid"""
        mpcalc.cross_section_components(self.cross.uwind, self.cross.vwind)
    
    