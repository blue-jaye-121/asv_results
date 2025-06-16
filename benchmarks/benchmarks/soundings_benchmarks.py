import os
import xarray as xr

import metpy.calc as mpcalc; 
from metpy.units import units; 

class TimeSuite: 
    #NOTE: I'm using CalVer https://calver.org/ YYYY.MM.DD
    version = "2025.06.16"; 
    
    def setup_cache(self):
       base_path = os.path.dirname(__file__) # path to current file
       file_path = os.path.join(base_path, "..", "data_array_compressed.nc");
       file_path = os.path.abspath(file_path)
       ds = xr.open_dataset(file_path)
       return ds; 
   
    def setup(self, ds):
        self.timeSlice = ds.isel(time = 0)
        self.profileSlice = ds.isel(lat = 25, lon = 25, time = 0)
        self.parcelProfile = mpcalc.parcel_profile(self.profileSlice.pressure, 
                                                  self.profileSlice.temperature[0], 
                                                  self.profileSlice.dewpoint[0]); 
        self.sbcape = mpcalc.surface_based_cape_cin(self.profileSlice.pressure,
                                                    self.profileSlice.temperature,
                                                    self.profileSlice.dewpoint)  
        self.sblcl = mpcalc.lcl(self.profileSlice.pressure,
                                self.profileSlice.temperature,
                                self.profileSlice.dewpoint) 
        self.relhel = mpcalc.storm_relative_helicity(self.profileSlice.height, 
                                                     self.profileSlice.uwind,
                                                     self.profileSlice.vwind, 
                                                     1 * units('km'))
        self.shear = mpcalc.bulk_shear(self.profileSlice.pressure,
                                       self.profileSlice.uwind,
                                       self.profileSlice.vwind); 
    def time_bulk_shear(self, profileSlice): 
        """Benchmarking calculating the bulk shear of a profile"""
        mpcalc.bulk_shear(self.profileSlice.pressure, self.profileSlice.uwind, self.profileSlice.vwind); 
        
    def time_ccl(self, profileSlice): 
        """Benchmarking calculating the convective condensation level of a profile"""
        mpcalc.ccl(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint); 
        
    def time_parcel_profile(self, profileSlice): 
        """Benchmarking the atmospheric parcel profile for one profile"""
        mpcalc.parcel_profile(self.profileSlice.pressure, self.profileSlice.temperature[0], self.profileSlice.dewpoint[0]);
        
    def time_most_unstable_parcel(self, profileSlice): 
        """Benchmarking the calculation to find the most unstable parcel for one profile"""
        mpcalc.most_unstable_parcel(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint); 
        
    def time_cape_cin(self, profileSlice): 
        """Benchmarking cape_cin calculation for one profile"""
        mpcalc.cape_cin(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint, self.parcelProfile); 
    
    def time_lcl(self, timeSlice):
        """Benchmarks lcl on a 3d cube - many profiles"""
        mpcalc.lcl(self.timeSlice.pressure, self.timeSlice.temperature, self.timeSlice.dewpoint); 
    
    def time_el(self, profileSlice): 
        """Benchmarks el calculation on one profile"""
        mpcalc.el(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint); 
        
    def time_storm_relative_helicity(self, profileSlice):
        """Benchmarks storm relative helicity over one profile"""
        mpcalc.storm_relative_helicity(self.profileSlice.height, self.profileSlice.uwind,
                                       self.profileSlice.vwind, 1 * units('km'))
        
    def time_vertical_totals(self, timeSlice):
        """Benchmarking vertical totals for many profiles"""
        mpcalc.vertical_totals(self.timeSlice.pressure, self.timeSlice.temperature); 
        mpcalc.storm_relative_helicity(self.profileSlice.height, self.profileSlice.uwind, self.profileSlice.vwind, depth = 1 * units('km'))
        
    def time_supercell_composite(self, profileSlice):
        """Benchmarks supercell composite calculation for one calculation"""
        mpcalc.supercell_composite(2500 * units('J/kg'), 125 * units('m^2/s^2'), 50 * units.knot)
    
    def time_critical_angle(self, profileSlice):
        """Benchmarking critical angle on one profile"""
        mpcalc.critical_angle(self.profileSlice.pressure, self.profileSlice.uwind, 
                              self.profileSlice.vwind, self.profileSlice.height,
                              0 * units('m/s'), 0 * units('m/s')); 
        
    def time_bunkers_storm_motion(self, profileSlice):
        """Benchmarking bunkers storm motion on one profile"""
        mpcalc.bunkers_storm_motion(self.profileSlice.pressure, self.profileSlice.uwind,
                                    self.profileSlice.vwind, self.profileSlice.height)
        
    def time_corfidi_storm_motion(self, profileSlice):
        """Benchmarking corfidi storm motion on one profile"""
        mpcalc.corfidi_storm_motion(self.profileSlice.pressure, self.profileSlice.uwind,
                                    self.profileSlice.vwind);
        
    def time_sweat_index(self, timeSlice):
        """Benchmarking SWEAT index on many profiles"""
        mpcalc.sweat_index(self.timeSlice.pressure, self.timeSlice.temperature, self.timeSlice.dewpoint,
                           self.timeSlice.windspeed, self.timeSlice.winddir); 
        
    def time_most_unstable_cape_cin(self, profileSlice):
        """Benchmarking most unstable cape cin calculation on one profile"""
        mpcalc.most_unstable_cape_cin(self.profileSlice.pressure, self.profileSlice.temperature,
                                      self.profileSlice.dewpoint); 
        
    def time_surface_based_cape_cin(self, profileSlice):
        """Benchmarking surface based cape cin calculation on one profile"""
        mpcalc.surface_based_cape_cin(self.profileSlice.pressure, self.profileSlice.temperature, 
                                      self.profileSlice.dewpoint); 
        
    def time_lifted_index(self, profileSlice):
        """Benchmarking lifted index calculation on one profile"""
        mpcalc.lifted_index(self.profileSlice.pressure, self.profileSlice.temperature,
                            self.parcelProfile); 
        
    def time_k_index(self, timeSlice):
        """Benchmarking k index calculation on many profiles"""
        mpcalc.k_index(self.timeSlice.pressure, self.timeSlice.temperature, self.timeSlice.dewpoint); 
        
    def time_mixed_layer_cape_cin(self, profileSlice):
        """Benchmarking mixed layer cape cin calculation for one profile"""
        mpcalc.mixed_layer_cape_cin(self.profileSlice.pressure, self.profileSlice.temperature,
                                    self.profileSlice.dewpoint); 
        
    def time_cross_totals(self, timeSlice):
        """Benchmarking cross totals calculation on many profiles"""
        mpcalc.cross_totals(self.timeSlice.pressure, self.timeSlice.temperature,
                            self.timeSlice.dewpoint)
        
    def time_downdraft_cape(self, profileSlice):
        """Benchmarking downdraft cape calculation on one profile"""
        mpcalc.downdraft_cape(self.profileSlice.pressure, self.profileSlice.temperature, self.profileSlice.dewpoint); 
        
    def time_parcel_profile_with_lcl_as_dataset(self, profileSlice):
        """Benchmarking parcel profile with lcl as dataset one on profile"""
        mpcalc.parcel_profile_with_lcl_as_dataset(self.profileSlice.pressure, self.profileSlice.temperature, 
                                                  self.profileSlice.dewpoint); 
        
    def time_showalter_index(self, profileSlice): 
        """Benchmarking calculating the showalter index on one profiles"""
        mpcalc.showalter_index(self.profileSlice.pressure, self.profileSlice.temperature,
                               self.profileSlice.dewpoint); 
        
    def time_galvez_davison_index(self, timeSlice):
        """Benchmarking calculating the galvez davison index on many profiles"""
        mpcalc.galvez_davison_index(self.timeSlice.pressure, self.timeSlice.temperature,
                                    self.timeSlice.mixing_ratio, self.timeSlice.pressure[0])
        
    # def time_significant_tornado(self, profileSlice):
    #     """Benchmarking significant tornado param for one profile"""
    #     mpcalc.significant_tornado(self.sbcape * units('J/kg'), self.sblcl * units('km'), self.relhel * units('m^2/s^2'), self.shear * units('m/s')); 