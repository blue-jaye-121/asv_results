# Copyright (c) 2018 MetPy Developers.
# Distributed under the terms of the BSD 3-Clause License.
# SPDX-License-Identifier: BSD-3-Clause
"""Tools to help with mapping/geographic applications.

Currently this includes tools for working with CartoPy projections.

"""
from ..cbook import Registry
from ..plots.cartopy_utils import import_cartopy

ccrs = import_cartopy()


class CFProjection:
    """Handle parsing CF projection metadata."""

    # mapping from Cartopy to CF vocabulary
    _default_attr_mapping = [('false_easting', 'false_easting'),
                             ('false_northing', 'false_northing'),
                             ('central_latitude', 'latitude_of_projection_origin'),
                             ('central_longitude', 'longitude_of_projection_origin')]

    projection_registry = Registry()

    def __init__(self, attrs):
        """Initialize the CF Projection handler with a set of metadata attributes."""
        self._attrs = attrs

    @classmethod
    def register(cls, name):
        """Register a new projection to handle."""
        return cls.projection_registry.register(name)

    @classmethod
    def build_projection_kwargs(cls, source, mapping):
        """Handle mapping a dictionary of metadata to keyword arguments."""
        return cls._map_arg_names(source, cls._default_attr_mapping + mapping)

    @staticmethod
    def _map_arg_names(source, mapping):
        """Map one set of keys to another."""
        return {cartopy_name: source[cf_name] for cartopy_name, cf_name in mapping
                if cf_name in source}

    @property
    def name(self):
        """Return the name of the projection."""
        return self._attrs.get('grid_mapping_name', 'unknown')

    @property
    def cartopy_globe(self):
        """Initialize a `cartopy.crs.Globe` from the metadata."""
        if 'earth_radius' in self._attrs:
            kwargs = {'ellipse': 'sphere', 'semimajor_axis': self._attrs['earth_radius'],
                      'semiminor_axis': self._attrs['earth_radius']}

        else:
            attr_mapping = [('semimajor_axis', 'semi_major_axis'),
                            ('semiminor_axis', 'semi_minor_axis'),
                            ('inverse_flattening', 'inverse_flattening')]
            kwargs = self._map_arg_names(self._attrs, attr_mapping)

            # Override CartoPy's default ellipse setting depending on whether
            # we have any metadata to map about the spheroid.
            kwargs['ellipse'] = None if kwargs else 'sphere'

        # interpret the 0 inverse_flattening as a spherical datum
        # and don't pass the value on.
        if kwargs.get('inverse_flattening') == 0:
            kwargs['ellipse'] = 'sphere'
            kwargs.pop('inverse_flattening', None)

        return ccrs.Globe(**kwargs)

    @property
    def cartopy_geodetic(self):
        """Make a `cartopy.crs.Geodetic` instance from the appropriate `cartopy.crs.Globe`."""
        return ccrs.Geodetic(self.cartopy_globe)

    def to_cartopy(self):
        """Convert to a CartoPy projection."""
        globe = self.cartopy_globe
        try:
            proj_handler = self.projection_registry[self.name]
        except KeyError:
            raise ValueError(f'Unhandled projection: {self.name}') from None

        return proj_handler(self._attrs, globe)

    def to_pyproj(self):
        """Convert to a PyProj CRS."""
        import pyproj

        return pyproj.CRS.from_cf(self._attrs)

    def to_dict(self):
        """Get the dictionary of metadata attributes."""
        return self._attrs.copy()

    def __str__(self):
        """Get a string representation of the projection."""
        return f'Projection: {self.name}'

    def __getitem__(self, item):
        """Return a given attribute."""
        return self._attrs[item]

    def __contains__(self, item):
        """Return whether a given attribute is present."""
        return item in self._attrs

    def __eq__(self, other):
        """Test equality (CFProjection with matching attrs)."""
        return self.__class__ == other.__class__ and self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Test inequality (not equal to)."""
        return not self.__eq__(other)


@CFProjection.register('geostationary')
def make_geo(attrs_dict, globe):
    """Handle geostationary projection."""
    attr_mapping = [('satellite_height', 'perspective_point_height'),
                    ('sweep_axis', 'sweep_angle_axis')]
    kwargs = CFProjection.build_projection_kwargs(attrs_dict, attr_mapping)

    # CartoPy can't handle central latitude for Geostationary (nor should it)
    # Just remove it if it's 0.
    if not kwargs.get('central_latitude'):
        kwargs.pop('central_latitude', None)

    # If sweep_angle_axis is not present, we should look for fixed_angle_axis and adjust
    if 'sweep_axis' not in kwargs:
        kwargs['sweep_axis'] = 'x' if attrs_dict['fixed_angle_axis'] == 'y' else 'y'

    return ccrs.Geostationary(globe=globe, **kwargs)


@CFProjection.register('lambert_conformal_conic')
def make_lcc(attrs_dict, globe):
    """Handle Lambert conformal conic projection."""
    attr_mapping = [('central_longitude', 'longitude_of_central_meridian'),
                    ('standard_parallels', 'standard_parallel')]
    kwargs = CFProjection.build_projection_kwargs(attrs_dict, attr_mapping)
    if 'standard_parallels' in kwargs:
        try:
            len(kwargs['standard_parallels'])
        except TypeError:
            kwargs['standard_parallels'] = [kwargs['standard_parallels']]
    return ccrs.LambertConformal(globe=globe, **kwargs)


@CFProjection.register('albers_conical_equal_area')
def make_aea(attrs_dict, globe):
    """Handle Albers Equal Area."""
    attr_mapping = [('central_longitude', 'longitude_of_central_meridian'),
                    ('standard_parallels', 'standard_parallel')]
    kwargs = CFProjection.build_projection_kwargs(attrs_dict, attr_mapping)
    if 'standard_parallels' in kwargs:
        try:
            len(kwargs['standard_parallels'])
        except TypeError:
            kwargs['standard_parallels'] = [kwargs['standard_parallels']]
    return ccrs.AlbersEqualArea(globe=globe, **kwargs)


@CFProjection.register('latitude_longitude')
def make_latlon(attrs_dict, globe):
    """Handle plain latitude/longitude mapping."""
    # TODO: Really need to use Geodetic to pass the proper globe
    return ccrs.PlateCarree()


@CFProjection.register('mercator')
def make_mercator(attrs_dict, globe):
    """Handle Mercator projection."""
    attr_mapping = [('latitude_true_scale', 'standard_parallel'),
                    ('scale_factor', 'scale_factor_at_projection_origin')]
    kwargs = CFProjection.build_projection_kwargs(attrs_dict, attr_mapping)

    # Work around the fact that in CartoPy <= 0.16 can't handle the easting/northing
    # or central_latitude in Mercator
    if not kwargs.get('false_easting'):
        kwargs.pop('false_easting', None)
    if not kwargs.get('false_northing'):
        kwargs.pop('false_northing', None)
    if not kwargs.get('central_latitude'):
        kwargs.pop('central_latitude', None)

    return ccrs.Mercator(globe=globe, **kwargs)


@CFProjection.register('stereographic')
def make_stereo(attrs_dict, globe):
    """Handle generic stereographic projection."""
    attr_mapping = [('scale_factor', 'scale_factor_at_projection_origin')]
    kwargs = CFProjection.build_projection_kwargs(attrs_dict, attr_mapping)

    return ccrs.Stereographic(globe=globe, **kwargs)


@CFProjection.register('polar_stereographic')
def make_polar_stereo(attrs_dict, globe):
    """Handle polar stereographic projection."""
    attr_mapping = [('central_longitude', 'straight_vertical_longitude_from_pole'),
                    ('true_scale_latitude', 'standard_parallel'),
                    ('scale_factor', 'scale_factor_at_projection_origin')]
    kwargs = CFProjection.build_projection_kwargs(attrs_dict, attr_mapping)

    return ccrs.Stereographic(globe=globe, **kwargs)


@CFProjection.register('rotated_latitude_longitude')
def make_rotated_latlon(attrs_dict, globe):
    """Handle rotated latitude/longitude projection."""
    attr_mapping = [('pole_longitude', 'grid_north_pole_longitude'),
                    ('pole_latitude', 'grid_north_pole_latitude'),
                    ('central_rotated_longitude', 'north_pole_grid_longitude')]
    kwargs = CFProjection.build_projection_kwargs(attrs_dict, attr_mapping)

    return ccrs.RotatedPole(globe=globe, **kwargs)
