import numpy as np
import xarray as xr
import pandas as pd

import metpy.calc as mpcalc; 
from metpy.units import units
import metpy.constants as mpconst


def makeXArray(): 
    """Create a sample xarray Dataset with 2D variables."""
    """Originally from cbook, modified by sjnorman for 3D"""
    """And then 4D with the fourth dimension as time"""
    # Make lat/lon data over the mid-latitudes
    lats = np.linspace(30, 40, 50)
    lons = np.linspace(360 - 100, 360 - 90, 50)
    pressure = np.linspace(250, 1000, 50) * units.hPa
    p_3d = pressure[:, np.newaxis, np.newaxis]
    
    times = pd.date_range("2024/01/01", "2025/01/01" ,freq='D');
    
    #Adding height
    z = mpcalc.pressure_to_height_std(p_3d); 
    height = np.tile(z, (1, len(lats), len(lons)))
    
    
    # make data based on Matplotlib example data for wind barbs
    x, y = np.meshgrid(np.linspace(-3, 3, 51), np.linspace(-3, 3, 51))
    z = (1 - x / 2 + x**5 + y**3) * np.exp(-x**2 - y**2)
    
    
    # make u and v out of the z equation
    u = -np.diff(z[:, 1:], axis=0) * 100 + 10
    v = np.diff(z[1:, :], axis=1) * 100 + 10
    w = np.full([50, 50], 1)
    
    #Make them 3D
    
    u_3d = np.zeros((len(pressure), 50, 50))
    for i, p in enumerate(pressure):
        u_3d[i, :, :] = u * (1000 - p.magnitude)**.3
        
    v_3d = np.zeros((len(pressure), 50, 50))
    for i, p in enumerate(pressure): 
        v_3d[i, :, :] = v * (1000 - p.magnitude)**.3
        
    w_3d = np.zeros((len(pressure), 50, 50))
    for i, p in enumerate(pressure): 
        w_3d[i, :, :] = w * np.random.rand()
    
    #Then make them 4D
    u_4d = np.zeros((50, 50, 50, len(times))) 
    for i, tm in enumerate(times): 
        u_4d[:, :, :, i] = u_3d * np.random.uniform(-2, 2); 
        
    v_4d = np.zeros((50, 50, 50, len(times)))
    for i, tm in enumerate(times):
        v_4d[:, :, :, i] = v_3d * np.random.uniform(-2, 2); 
    
    w_4d = np.zeros((50, 50, 50, len(times)))
    for i, tm in enumerate(times):
        w_4d[:, :, :, i] = w_3d * np.random.uniform(-2, 2);
        
    
    #setting up for annual temperature cycle    
    days = np.arange(len(times)); 
    annual_cycle = np.sin(2 * np.pi * days / len(times)); 
    
    seasonal_amplitude = 10 #degrees C difference from summer to winter
    seasonal_variation = seasonal_amplitude * annual_cycle; 
    
    
    # make t as colder air to the north and 3d
    t_sfc = (np.linspace(15, 5, 50) * np.ones((50, 50)))
    t_3d = np.zeros((len(pressure), 50, 50)) # (pressure, lat, lon) 
    for i, p in enumerate(pressure):
        t_3d[i, :, :] = t_sfc * (p/1000) * mpconst.R / mpconst.Cp_d
        
            
    #Make t colder in the winter, warmer in the summer         
    t_4d = np.zeros((50, 50, 50, len(times)))
    for i, tm in enumerate(times):
        t_4d[:, :, :, i] = t_3d + seasonal_variation[i];     
        
    t_4d = (t_4d + 273.15) * units.K
    
    
    #Generate potential temperature
    theta_4d = mpcalc.potential_temperature(p, t_4d);
    
    # place data into an xarray dataset object
    lat_da = xr.DataArray(lats, dims = 'lat', attrs={'standard_name': 'latitude', 'units': 'degrees_north'})
    lon_da = xr.DataArray(lons, dims = 'lon',  attrs={'standard_name': 'longitude', 'units': 'degrees_east'})
    pressure_level = xr.DataArray(pressure.magnitude, dims = 'pressure', attrs={'standard_name': 'pressure', 'units': 'hPa'})
    time_da = xr.DataArray(times, dims = 'time', attrs={'standard name': 'time'}); 
    
    coords = {"lat" :lat_da, "lon" : lon_da, "pressure": pressure_level, "time" : time_da}; 
    
    
    uwind = xr.DataArray(u_4d, coords=coords, dims=['pressure', 'lat', 'lon', 'time'],
                         attrs={'standard_name': 'u-component_of_wind', 'units': 'm s-1'})
    vwind = xr.DataArray(v_4d, coords=coords, dims=['pressure', 'lat', 'lon', 'time'],
                         attrs={'standard_name': 'v-component_of_wind', 'units': 'm s-1'})
    wwind = xr.DataArray(w_4d, coords=coords, dims=['pressure', 'lat', 'lon', 'time'],
                         attrs={'standard_name': 'w-component_of_wind', 'units': 'm s-1'})
    temperature = xr.DataArray(t_4d, coords=coords, dims=['pressure', 'lat', 'lon', 'time'],
                               attrs={'standard_name': 'temperature', 'units': 'K'})
    height = xr.DataArray(height, dims=['pressure', 'lat', 'lon'], 
                         attrs={'standard_name': 'z dimension', 'units': 'km'})
    theta = xr.DataArray(theta_4d, coords = coords, dims=['pressure', 'lat', 'lon', 'time'],
                         attrs={'standard_name' : 'Potential temperature', 'units' : 'K'})
    
    return xr.Dataset({'uwind': uwind,
                       'vwind': vwind,
                       'wwind': wwind,
                       'temperature': temperature, 
                       'height':height, 
                       'theta':theta})


class TimeSuite: 
    """Time benchmark class"""
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.06";
    
    def setup(self):
        self.ds = makeXArray(); 
        self.timeSlice = self.ds.isel(time = 0)
        self.pressureSlice = self.ds.isel(pressure = 0)
        
    def time_brunt_vaisala_frequency(self): 
        """Benchmark Brunt Vaisala frequency calculation - on a grid"""
        mpcalc.brunt_vaisala_frequency(self.timeSlice.height, self.timeSlice.theta); 
        
    def time_gradient_richardson_number(self): 
        """Benchmark Graident Richardson Number on a grid"""
        mpcalc.gradient_richardson_number(self.timeSlice.height, self.timeSlice.theta,
                                         self.timeSlice.uwind, self.timeSlice.vwind)