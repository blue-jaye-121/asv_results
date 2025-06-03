import numpy as np
import xarray as xr

import metpy.calc as mpcalc; 
from metpy.units import units

def index_xarray_data():
     """Create data for testing that index calculations work with xarray data."""
     pressure = xr.DataArray([850., 700., 500.], dims=('isobaric',), attrs={'units': 'hPa'})
     temp = xr.DataArray([[[[296., 295., 294.], [293., 292., 291.]],
                           [[286., 285., 284.], [283., 282., 281.]],
                           [[276., 275., 274.], [273., 272., 271.]]]] * units.K,
                         dims=('time', 'isobaric', 'y', 'x'))
     
     mixingRatio = xr.DataArray([[[[9., 9., 9.], [10., 10., 10.]],
                           [[11., 11., 11.], [11., 11., 11.]],
                           [[12., 12., 270.], [12., 12., 12.]]]],
                         dims=('time', 'isobaric', 'y', 'x'))
     
     vaporPressure = xr.DataArray([[[[30., 30., 30.], [28.,28.,28.]], 
                                     [[27., 26., 27.], [25., 24., 24.]],
                                     [[23., 19., 23.], [18., 16., .20]]]] * units.hPa,
                                   dims=('time', 'isobaric', 'y', 'x'))
     rh = xr.DataArray([[[[30., 30., 30.], [28.,28.,28.]], 
                                     [[27., 26., 27.], [25., 24., 24.]],
                                     [[23., 19., 23.], [18., 16., .20]]]] * units.percent,
                                   dims=('time', 'isobaric', 'y', 'x'))
     
     dewpoint = xr.DataArray([[[[250., 250., 250.], [240., 240., 240.]],
                           [[260., 260., 260.], [240., 240., 240.]],
                           [[250., 250., 250.], [260., 260., 260.]]]] * units.K,
                         dims=('time', 'isobaric', 'y', 'x'))
     
     return xr.Dataset({'temperature': temp,  'mixingRatio': mixingRatio, 'vaporPressure': vaporPressure,
                        'pressure': pressure, 'relativeHumidity': rh, 'dewpoint':dewpoint},
                       coords={'isobaric': pressure, 'time': ['2020-01-01T00:00Z']}); 

class TimeSuite: 
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.03"; 
    
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
        
        self.u, self.v = mpcalc.wind_components(self.windspd_denver05282019, self.winddir_denver05282019); 
        
        self.ds = index_xarray_data()
        self.slice = self.ds.isel(isobaric=0)
        
    def time_bulk_shear(self): 
        """Benchmarking calculating the bulk shear of a profile"""
        mpcalc.bulk_shear(self.pressure_denver05282019, self.u, self.v); 
        
    def time_ccl(self): 
        """Benchmarking calculating the convective condensation level of a profile"""
        mpcalc.ccl(self.pressure_denver05282019, self.temperature_denver05282019, self.dewpoint_denver05282019); 
        
    def time_parcel_profile_with_lcl(self): 
        """Benchmarking the atmospheric parcel profile with the lcl"""
        mpcalc.parcel_profile_with_lcl(self.pressure_denver05282019, self.temperature_denver05282019, self.dewpoint_denver05282019);
        
    def time_most_unstable_parcel(self): 
        """Benchmarking the calculation to find the most unstable parcel"""
        mpcalc.most_unstable_parcel(self.pressure_denver05282019, self.temperature_denver05282019, self.dewpoint_denver05282019); 
    
        
        
    