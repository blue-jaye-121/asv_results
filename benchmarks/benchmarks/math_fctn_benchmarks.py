import os
import xarray as xr

import metpy.calc as mpcalc; 

 
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