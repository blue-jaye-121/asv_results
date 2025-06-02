import numpy as np
import xarray as xr

from metpy.calc import (brunt_vaisala_frequency, potential_temperature) 
from metpy.units import units

def createXArray():
    """Create a sample xarray Dataset with 2D variables."""
    """Originally from cbook, modified by sjnorman"""
    
    # make data based on Matplotlib example data for wind barbs
    x, y = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
    z = (1 - x / 2 + x**5 + y**3) * np.exp(-x**2 - y**2)
    
    # make u and v out of the z equation
    u = -np.diff(z[:, 1:], axis=0) * 100 + 10
    v = np.diff(z[1:, :], axis=1) * 100 + 10
    
    # make t as colder air to the north
    t = (np.linspace(15, 5, 99) * np.ones((99, 99))).T
    
    # Make lat/lon data over the mid-latitudes
    lats = np.linspace(30, 40, 99)
    lons = np.linspace(360 - 100, 360 - 90, 99)
    
    #Making it so the dimensions are the same
    z = np.delete(z, 99, axis=1); 
    z = np.delete(z, 99, axis=0); 
    
    theta = potential_temperature(1000 * units.hPa, t * units.degC); 
    
    # place data into an xarray dataset object
    lat = xr.DataArray(lats, attrs={'standard_name': 'latitude', 'units': 'degrees_north'})
    lon = xr.DataArray(lons, attrs={'standard_name': 'longitude', 'units': 'degrees_east'})
    uwind = xr.DataArray(u, coords=(lat, lon), dims=['lat', 'lon'],
                         attrs={'standard_name': 'u-component_of_wind', 'units': 'm s-1'})
    vwind = xr.DataArray(v, coords=(lat, lon), dims=['lat', 'lon'],
                         attrs={'standard_name': 'u-component_of_wind', 'units': 'm s-1'})
    temperature = xr.DataArray(t, coords=(lat, lon), dims=['lat', 'lon'],
                               attrs={'standard_name': 'temperature', 'units': 'degC'})
    z_dim = xr.DataArray(z, coords = (lat, lon), dims=['lat', 'lon'], 
                         attrs={'standard_name': 'z dimension', 'units': 'km'})
    theta = xr.DataArray(theta, coords = (lat, lon), dims=['lat', 'lon'],
                         attrs={'standard_name' : 'Potential temperature', 'units' : 'degC'})
    return xr.Dataset({'uwind': uwind,
                       'vwind': vwind,
                       'temperature': temperature, 
                       'z_dim':z_dim, 
                       'theta':theta})

class TimeSuite: 
    
    
    
    def setup(self): 
        self.ds = createXArray(); 
        self.slice = self.ds.isel()
    
    def time_brunt_vaisala_frequency(self):
        """Benchmarking the brunt vaisala frequency calculation"""
        brunt_vaisala_frequency(self.ds.z_dim, self.ds.theta); 
        