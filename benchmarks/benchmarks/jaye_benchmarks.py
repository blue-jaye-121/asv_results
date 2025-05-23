import numpy as np
import xarray as xr

from metpy.calc import virtual_temperature
from metpy.units import units

class TimeSuite: 
    
    def setup(self): 
        self.mixingRatio = np.array([9, 10, 11, 12, 13, 14]); #dimensionless
        self.t = np.array([22.2, 14.6, 12., 9.4, 7., -38.]) * units.celsius
        
    def time_virtual_temperature(self): 
        """Benchmark mixing ratio from relative humidity calculation."""
        virtual_temperature(self.t[0], self.mixingRatio[0] * units("g/kg"));
        
        