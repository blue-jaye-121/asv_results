import numpy as np
import xarray as xr

from metpy.calc import (wind_components, absolute_vorticity, advection, 
pressure_to_height_std, ageostrophic_wind,
potential_temperature, frontogenesis, potential_vorticity_barotropic,
 q_vector, total_deformation, vorticity) 
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
        self.pressure_denver05282019 = [831, 809, 779.2, 750.7, 734, 722.9, 700, 669.8, 669, 645, 644.4, 619.8, 606,
                                   601, 597, 596, 591, 555, 550.5, 527, 518, 516, 512, 501, 500, 489, 487.2, 482,
                                   467.1, 447.9, 433, 422, 400, 399, 377.2, 356, 302, 300, 297, 250, 240.3, 236, 
                                   229.3, 227, 200, 190, 181.9, 165.9, 161, 158.4, 150, 137.5, 125, 119.2, 113.7, 108.4,
                                   103, 101, 100, 89.5, 89.3, 85.1, 73.6, 70.1, 70, 66.8, 63.6, 60.6, 55, 54.7, 52.4,
                                   50, 49.8, 47.5, 45.3, 39.2, 37.3, 33.9, 30.8, 30, 28, 22.1, 21.9, 21, 20, 19.3, 17.4, 17.2,
                                   15.9, 15.3, 13.7, 13.2, 11, 10.4, 10] * units.hPa;

        self.temperature_denver05282019 = [6.8, 5.7, 4.2, 2.7, 1.8, 1.1, -0.5, -3, -3.1, -5.1, -5.2, -7.3, -8.5, -7.5, -9.1,
                                      -9.1, -8.9, -14.3, -14.4, -14.7, -16.1, -19.1, -20.1, -21.3, -21.3, -22.1, -22.4,
                                      -23.1, -24.5, -26.4, -27.9, -28.7, -31.3, -31.5, -34.5, -37.5, -41.5, -41.7, 
                                      -41.9, -49.1, -50.6, -51.3, -50.5, -50.2, -46.7, -45.5, -45.9, -46.6, -46.9, 
                                      -47.5, -49.7, -52.2, -54.8, -56.2, -57.5, -58.9, -60.3, -60.3, -59.3, -57.3, 
                                      -57.3, -57.8, -59.1, -59.5, -59.5, -59.2, -58.8, -58.4, -57.7, -57.7, -58.8, 
                                      -59.9, -60.3, -59.8, -59.4, -57.9, -57.5, -56.5, -55.5, -55.3, -54.5, -52, 
                                      -51.9, -52.3, -52.9, -52.9, -49.9, -49.5, -49.9, -50.1, -43.7, -43.7, -43.7, 
                                      -43.7, -42.9] * units.degC; 
        
        self.dewpoint_denver05282019 = [5.7, 4.6, 3.1, 1.6, 0.7, -0.1, -1.9, -5.8, -5.9, -6, -6.1, -8.6, -10.1, -8.9, -10.6,
                                   -10.6, -10.4, -16.7, -16.7, -16.6, -18, -22.7, -27.1, -30.3, -30.3, -30.1, -31.7, 
                                   -36.1, -37.8, -40.1, -41.9, -38.7, -49.3, -49.5, -51, -52.5, -62.3, -62.7, -62.9, 
                                   -69.1, -68.6, -68.3, -68.7, -68.9, -70.7, -69.5, -69.9, -70.6, -70.9, -71.3, -72.7,
                                   -74.2, -75.9, -76.7, -77.6, -78.4, -79.3, -79.3, -78.3, -77.3, -77.3, -77.3, -77.5,
                                   -77.5, -77.5, -77.2, -76.8, -76.4, -75.7, -75.7, -75.3, -74.9, -75.3, -75, -74.7,
                                   -73.9, -73.6, -73, -72.4, -72.3, -71.5, -69, -68.9, -68.5, -67.9, -68.9, -66.8, 
                                   -66.5, -66.9, -67.1, -63.7, -63.8, -64.5, -64.7, -63.9] * units.degC; 

        self.winddir_denver05282019 = [340, 5, 5, 170, 167, 165, 170, 190, 189, 170, 170, 130, 133, 134, 135, 135, 138, 
                                  157, 160, 176, 182, 184, 186, 194, 195, 204, 205, 204, 200, 200, 203, 205, 210, 210,
                                  205, 205, 205, 205, 205, 200, 200, 200, 205, 205, 225, 233, 240, 235, 196, 175, 180,
                                  195, 210, 250, 225, 225, 240, 243, 245, 260, 260, 240, 265, 310, 310, 355, 35, 115,
                                  115, 109, 55, 55, 55, 60, 65, 80, 105, 80, 90, 75, 55, 95, 91, 70, 65, 68, 75, 77,
                                  90, 90, 90, 90, 110, 113, 115] * units.degrees; 


        self.windspd_denver05282019 = [ 3.6, 6.2, 4.6, 2.1, 3.3, 4.1, 4.1, 3.6, 3.6, 3.6, 3.6, 3.1, 4.0, 4.3, 4.6, 4.6, 4.6, 4.6, 4.6, 8.6,
            10.2, 10.5, 11.2, 13.2, 13.4, 13.8, 13.9, 13.6, 12.9, 14.9, 19.1, 22.2, 28.8, 29.1, 34.5, 35.7, 39.1, 39.1,
            39.3, 41.7, 40.7, 40.7, 43.2, 43.2, 28.8, 23.0, 18.0, 8.2, 5.9, 4.6, 6.2, 10.3, 8.2, 5.7, 5.2, 5.2, 10.3,
            9.6, 9.3, 12.3, 12.4, 4.1, 4.1, 2.6, 1.0, 2.6, 4.1, 4.6, 0.5, 1.0, 5.2, 5.7, 6.0, 10.3, 9.3, 7.7, 10.3,
            10.8, 7.2, 7.2, 6.2, 8.8, 8.3, 5.7, 9.8, 11.1, 14.9, 14.8, 13.9, 13.4, 11.8, 11.3, 7.2, 7.2, 7.2] * (units.m / units.s);
        
        self.u, self.v = wind_components(self.windspd_denver05282019, self.winddir_denver05282019); 
        
        self.height_denver05282019 = pressure_to_height_std(self.pressure_denver05282019) * units.km;
        
        self.ds = createXArray(); 
        self.slice = self.ds.isel()
    
    def time_absolute_vorticity(self): 
        """benchmarking absolute momentum calculation"""
        absolute_vorticity(self.slice.uwind, self.slice.vwind); 
        
    def time_advection(self): 
        """Benchmarking the advection calculation"""
        advection(self.ds.temperature, self.ds.uwind, self.ds.vwind);
        
    def time_ageostrophic_wind(self): 
        """Benchmarking ageostrophic wind calculation"""
        ageostrophic_wind(self.ds.z_dim, self.ds.uwind, self.ds.vwind); 
    
    def time_frontogenesis(self):
        """Benchmarking the calculation of frontogenesis of a t field"""
        frontogenesis(self.ds.theta, self.ds.uwind, self.ds.vwind); 
    
    def time_potential_vorticity_barotropic(self):
        """Benchmarking the barotropic potential vorticity calculation"""
        potential_vorticity_barotropic(self.ds.z_dim, self.ds.uwind, self.ds.vwind); 
        
    def time_q_vector(self): 
        """Benchmarking q vector calculation"""
        q_vector(self.ds.uwind, self.ds.vwind, self.ds.temperature, 1000 * units.hPa); 
        
    def time_total_deformation(self): 
        """Benchmarking total deformation calculation"""
        total_deformation(self.ds.uwind, self.ds.vwind); 
        
    def time_vorticity(self): 
        """Benchmarking vorticity calculation"""
        vorticity(self.ds.uwind, self.ds.vwind); 