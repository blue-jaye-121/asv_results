import numpy as np
import xarray as xr

import metpy.calc as mpcalc
from metpy.units import units
import metpy.constants as mpconst

def createXArray():
    """Create a sample xarray Dataset with 2D variables."""
    """Originally from cbook, modified by sjnorman for 3D"""




    # Make lat/lon data over the mid-latitudes
    lats = np.linspace(30, 40, 99)
    lons = np.linspace(360 - 100, 360 - 90, 99)
    pressure = np.linspace(250, 1000, 50) * units.hPa
    p_3d = pressure[:, np.newaxis, np.newaxis]
    coords = {"lat" :lats, "lon" : lons, "pressure": pressure.magnitude}; 

    # make data based on Matplotlib example data for wind barbs
    x, y = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
    z = (1 - x / 2 + x**5 + y**3) * np.exp(-x**2 - y**2)


    # make u and v out of the z equation
    u = -np.diff(z[:, 1:], axis=0) * 100 + 10
    v = np.diff(z[1:, :], axis=1) * 100 + 10
    w = np.full([99, 99], 1)

    #Make them 3D
    u_3d = np.repeat(u[np.newaxis, :, :], len(pressure), axis=0)
    v_3d = np.repeat(v[np.newaxis, :, :], len(pressure), axis=0)
    w_3d = np.repeat(w[np.newaxis, :, :], len(pressure), axis=0)



    # make t as colder air to the north and 3d
    t_sfc = (np.linspace(15, 5, 99) * np.ones((99, 99))).T
    t = np.zeros((len(pressure), 99, 99)) # (pressure, lat, lon) 
    for i, p in enumerate(pressure):
        t[i, :, :] = t_sfc * (p/1000) * mpconst.R / mpconst.Cp_d
        
    t = (t + 273.15) * units.K

    #Adding height
    z = mpcalc.pressure_to_height_std(p_3d); 
    z= np.tile(z, (1, len(lats), len(lons)))

    theta = mpcalc.potential_temperature(p_3d, t); 

    # place data into an xarray dataset object
    lat_da = xr.DataArray(lats, dims = 'lat', attrs={'standard_name': 'latitude', 'units': 'degrees_north'})
    lon_da = xr.DataArray(lons, dims = 'lon',  attrs={'standard_name': 'longitude', 'units': 'degrees_east'})
    pressure_level = xr.DataArray(pressure.magnitude, dims = 'pressure', attrs={'standard_name': 'pressure', 'units': 'hPa'})

    coords = {"lat" :lat_da, "lon" : lon_da, "pressure": pressure_level}; 


    uwind = xr.DataArray(u_3d, coords=coords, dims=['pressure', 'lat', 'lon'],
                         attrs={'standard_name': 'u-component_of_wind', 'units': 'm s-1'})
    vwind = xr.DataArray(v_3d, coords=coords, dims=['pressure', 'lat', 'lon'],
                         attrs={'standard_name': 'v-component_of_wind', 'units': 'm s-1'})
    wwind = xr.DataArray(w_3d, coords=coords, dims=['pressure', 'lat', 'lon'],
                         attrs={'standard_name': 'w-component_of_wind', 'units': 'm s-1'})
    temperature = xr.DataArray(t, coords=coords, dims=['pressure', 'lat', 'lon'],
                               attrs={'standard_name': 'temperature', 'units': 'K'})
    height = xr.DataArray(z, coords = coords, dims=['pressure', 'lat', 'lon'], 
                         attrs={'standard_name': 'z dimension', 'units': 'km'})
    theta = xr.DataArray(theta, coords = coords, dims=['pressure', 'lat', 'lon'],
                         attrs={'standard_name' : 'Potential temperature', 'units' : 'K'})
    return xr.Dataset({'uwind': uwind,
                       'vwind': vwind,
                       'wwind': wwind,
                       'temperature': temperature, 
                       'height':height, 
                       'theta':theta})

class TimeSuite: 
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.03"; 
    
    
    def setup(self): 
        self.ds = createXArray(); 
        self.slice = self.ds.isel(pressure = 0)
    
    def time_brunt_vaisala_frequency(self):
        """Benchmarking the brunt vaisala frequency calculation"""
        mpcalc.brunt_vaisala_frequency(self.ds.height, self.ds.theta); 
        
    def time_gradient_richardson_number(self): 
        """Benchmarking the gradient richardson number calculation"""
        mpcalc.gradient_richardson_number(self.ds.height, self.ds.theta, self.ds.uwind, self.ds.vwind); 
    
    def time_tke(self): 
        """Benchmarking the turbulence kinetic energy calculation"""
        mpcalc.tke(self.ds.uwind, self.ds.vwind, self.ds.wwind); 