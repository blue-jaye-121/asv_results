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
       self.pressureSlice = ds.isel(pressure = 0, time = 0)
       self.timeSlice = ds.isel(time = 0)
       self.upperSlice = ds.isel(pressure = 49, time = 0)
       self.profileSlice = ds.isel(time = 0, lat = 25, lon = 25)
    
    def time_virtual_temperature(self, timeSlice): 
        """Benchmark virtual temperature on a 3d cube."""
        mpcalc.virtual_temperature(self.timeSlice.temperature, self.timeSlice.mixing_ratio);
        
    def time_dewpoint(self, timeSlice): 
        """Benchmarking dewpoint from vapor pressure on a 3d cube"""
        mpcalc.dewpoint(self.timeSlice.vapor_pressure); 
        
    def time_rh_from_mixing_ratio(self, timeSlice):
        """Benchmarking relative humidity from mixing ratio on a 3d cube"""
        mpcalc.relative_humidity_from_mixing_ratio(self.timeSlice.pressure, self.timeSlice.temperature, self.timeSlice.mixing_ratio); 
    
    def time_dewpoint_from_rh(self, timeSlice):
        """Benchmarking dewpoint from calculated on a 3d cube"""
        mpcalc.dewpoint_from_relative_humidity(self.timeSlice.temperature, self.timeSlice.relative_humidity);
        
    def time_precipitable_water(self, timeSlice): 
        """Benchmarking precipitable water calculation for one column"""
        mpcalc.precipitable_water(self.timeSlice.pressure, self.timeSlice.dewpoint[0][0]);
        
    def time_wet_bulb_temperature(self, pressureSlice):
        """Benchmarking wet bulb temperature calculation on on a slice"""
        mpcalc.wet_bulb_temperature(self.pressureSlice.pressure, self.pressureSlice.temperature, self.pressureSlice.dewpoint); 
        
    def time_scale_height(self, pressureSlice): 
        """Benchmarking the calculation for the scale height of a layer for 2 surfaces"""
        mpcalc.scale_height(self.upperSlice.temperature, self.pressureSlice.temperature); 
        
    def time_moist_lapse(self, profileSlice): 
        """Benchmarking the calculation for the moist lapse rate for one profile"""
        mpcalc.moist_lapse(self.profileSlice.pressure.values * units('hPa'), self.profileSlice.temperature[0].values * units('K'));  
        
    def time_saturation_vapor_pressure(self, timeSlice): 
        """Benchmarking the saturation vapor pressure calculation for a 3d cube"""
        mpcalc.saturation_vapor_pressure(self.timeSlice.temperature); 
        
    def time_water_latent_heat_vaporization(self, timeSlice):
        """Benchmarking the vaporization latent heat calculation on a 3d cube"""
        mpcalc.water_latent_heat_vaporization(self.timeSlice.temperature); 
        
    def time_water_latent_heat_sublimation(self, timeSlice):
        """Benchmarking the sublimation latent heat calcultion on a 3d cube"""
        mpcalc.water_latent_heat_sublimation(self.timeSlice.temperature); 
        
    def time_water_latent_heat_melting(self, timeSlice):
        """Benchmarking the melting latent heat calculation on a 3d cube"""
        mpcalc.water_latent_heat_melting(self.timeSlice.temperature); 
        
    def time_specific_humidity_from_dewpoint(self, timeSlice):
        """Benchmarking specific humidity from dewpoint calculation on a 3d cube"""
        mpcalc.specific_humidity_from_dewpoint(self.timeSlice.pressure, self.timeSlice.temperature); 
        
    def time_relative_humidity_from_dewpoint(self, timeSlice):
        """Benchmarking relative humidity from dewpoint calculation on a 3d cube"""
        mpcalc.relative_humidity_from_dewpoint(self.timeSlice.temperature, self.timeSlice.dewpoint); 
        
    def time_moist_static_energy(self, timeSlice):
        """Benchmarking moist static energy calculation on a 3d cube"""
        mpcalc.moist_static_energy(self.timeSlice.height, self.timeSlice.temperature, self.timeSlice.specific_humidity); 
        
    def time_dewpoint_from_specific_humidity(self, timeSlice):
        """Benchmarking dewpoint from specific humidity calculation on a 3d cube"""
        mpcalc.dewpoint_from_specific_humidity(self.timeSlice.pressure, self.timeSlice.temperature, 
                                               self.timeSlice.specific_humidity); 
        
    def time_moist_air_specific_heat_pressure(self, timeSlice):
        """Benchmarking moist air specific heat pressure calculation on a 3d cube"""
        mpcalc.moist_air_specific_heat_pressure(self.timeSlice.specific_humidity);
        
    def time_moist_air_poisson_exponent(self, timeSlice):
        """Benchmarking moist air poisson exponent calculation on a cube"""
        mpcalc.moist_air_poisson_exponent(self.timeSlice.specific_humidity); 
        
    def time_relative_humidity_wet_psychrometric(self, timeSlice):
        """Benchmarking the relative humidity from psychometric calculation on a cube"""
        mpcalc.relative_humidity_wet_psychrometric(self.timeSlice.pressure, self.timeSlice.temperature,
                                                   self.timeSlice.wet_bulb_temperature); 
        
    def time_thickness_hydrostatic_from_relative_humidity(self, profileSlice):
        """Benchmarking thickness hydrostatic calculation from relative humidity on one profile"""
        mpcalc.thickness_hydrostatic_from_relative_humidity(self.profileSlice.pressure, self.profileSlice.temperature,
                                                            self.profileSlice.relative_humidity); 
        
    def time_relative_humidity_from_specific_humidity(self, timeSlice): 
        """Benchmarking relative humidity from specific humidity calculation on a 3d cube"""
        mpcalc.relative_humidity_from_specific_humidity(self.timeSlice.pressure, self.timeSlice.temperature,
                                                        self.timeSlice.specific_humidity); 
        
    def time_wet_bulb_potential_temperature(self, timeSlice):
        """Benchmarking the wet bulb potential temperature calculation on a 3d cube"""
        mpcalc.wet_bulb_potential_temperature(self.timeSlice.pressure, self.timeSlice.temperature, 
                                              self.timeSlice.dewpoint); 
        
    def time_vertical_velocity_pressure(self, timeSlice): 
        """Benchmarking vertical velocity wrt pressure calculation on a 3d cube"""
        mpcalc.vertical_velocity_pressure(self.timeSlice.wwind, self.timeSlice.pressure, self.timeSlice.temperature, 
                                          self.timeSlice.mixing_ratio); 
        
    def time_vertical_velocity(self, timeSlice):
        """Benchmarking vertical velocity calculation on a 3d cube"""
        mpcalc.vertical_velocity(self.timeSlice.omega, self.timeSlice.pressure, self.timeSlice.temperature, 
                                 self.timeSlice.mixing_ratio); 
        
    def time_saturation_equivalent_potential_temperature(self, timeSlice):
        """Benchmarking saturation equivalent potential temperature on 3d cube"""
        mpcalc.saturation_equivalent_potential_temperature(self.timeSlice.pressure, self.timeSlice.temperature); 
        
    def time_virtual_potential_temperature(self, timeSlice):
        """Benchmarking virtual potential temperature calculation on a 3d cube"""
        mpcalc.virtual_potential_temperature(self.timeSlice.pressure, self.timeSlice.temperature,
                                             self.timeSlice.mixing_ratio); 
        
    def time_psychrometric_vapor_pressure_wet(self, timeSlice):
        """Benchmarking psychrometric vapor pressure calculation on a 3d cube"""
        mpcalc.psychrometric_vapor_pressure_wet(self.timeSlice.pressure, self.timeSlice.temperature,
                                            self.timeSlice.wet_bulb_temperature); 
        
    def time_mixing_ratio_from_relative_humidity(self, timeSlice):
        """Benchmarking mixing ratio from relative humidity calculation on a 3d cube"""
        mpcalc.mixing_ratio_from_relative_humidity(self.timeSlice.pressure, self.timeSlice.temperature,
                                                   self.timeSlice.relative_humidity); 
        
    def time_mixing_ratio_from_specific_humidity(self, timeSlice):
        """Benchmarking calculating mixing rato from specific humidity on a 3d cube"""
        mpcalc.mixing_ratio_from_specific_humidity(self.timeSlice.specific_humidity); 
        
    def time_relative_humidity_from_mixing_ratio(self, timeSlice):
        """Benchmarking relative humidity from mixing ratio calculation on a 3d cube"""
        mpcalc.relative_humidity_from_mixing_ratio(self.timeSlice.pressure, self.timeSlice.temperature,
                                                   self.timeSlice.mixing_ratio); 
        
    def time_equivalent_potential_temperature(self, timeSlice):
        """Benchmarking equivalent potential temperature calculation on 3d cube"""
        mpcalc.equivalent_potential_temperature(self.timeSlice.pressure, self.timeSlice.temperature,
                                                self.timeSlice.dewpoint)
        
    def time_virtual_temperature_from_dewpoint(self, timeSlice):
        """Benchmarking virtual temperature from dewpoint calculation on 3d cube"""
        mpcalc.virtual_temperature_from_dewpoint(self.timeSlice.pressure, self.timeSlice.temperature,
                                                 self.timeSlice.dewpoint);