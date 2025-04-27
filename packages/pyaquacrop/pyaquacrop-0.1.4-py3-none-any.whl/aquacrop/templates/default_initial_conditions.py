from aquacrop import InitialConditions

# Default initial conditions with AquaCrop defaults
default_initial_conditions = InitialConditions(
    name="DefaultInitialConditions",
    description="Default initial conditions with AquaCrop calculated defaults",
    params={
        'initial_canopy_cover': -9.00,  # Default calculated by AquaCrop
        'initial_biomass': 0.000,
        'initial_rooting_depth': -9.00,  # Default calculated by AquaCrop
        'water_layer': 0.0,
        'water_layer_ec': 0.00,
        'soil_water_content_type': 0,  # For specific layers
        'soil_data': []  # Empty list means AquaCrop will use default soil water content
    }
)

# Field capacity soil water content
field_capacity_initial = InitialConditions(
    name="FieldCapacityInitial",
    description="Initial soil water content at field capacity",
    params={
        'initial_canopy_cover': -9.00,  # Default calculated by AquaCrop
        'initial_biomass': 0.000,
        'initial_rooting_depth': -9.00,  # Default calculated by AquaCrop
        'water_layer': 0.0,
        'water_layer_ec': 0.00,
        'soil_water_content_type': 1,  # For specific depths
        'soil_data': [
            {'depth': 0.10, 'water_content': 29.0, 'ec': 0.00},
            {'depth': 0.30, 'water_content': 29.0, 'ec': 0.00},
            {'depth': 0.60, 'water_content': 29.0, 'ec': 0.00},
            {'depth': 1.00, 'water_content': 29.0, 'ec': 0.00},
            {'depth': 1.50, 'water_content': 29.0, 'ec': 0.00}
        ]
    }
)

# Dry soil water content
dry_initial = InitialConditions(
    name="DryInitial",
    description="Initial soil water content at 50% of available water",
    params={
        'initial_canopy_cover': -9.00,  # Default calculated by AquaCrop
        'initial_biomass': 0.000,
        'initial_rooting_depth': -9.00,  # Default calculated by AquaCrop
        'water_layer': 0.0,
        'water_layer_ec': 0.00,
        'soil_water_content_type': 1,  # For specific depths
        'soil_data': [
            {'depth': 0.10, 'water_content': 21.0, 'ec': 0.00},
            {'depth': 0.30, 'water_content': 21.0, 'ec': 0.00},
            {'depth': 0.60, 'water_content': 21.0, 'ec': 0.00},
            {'depth': 1.00, 'water_content': 21.0, 'ec': 0.00},
            {'depth': 1.50, 'water_content': 21.0, 'ec': 0.00}
        ]
    }
)

# Very dry soil water content
very_dry_initial = InitialConditions(
    name="VeryDryInitial",
    description="Initial soil water content close to wilting point",
    params={
        'initial_canopy_cover': -9.00,  # Default calculated by AquaCrop
        'initial_biomass': 0.000,
        'initial_rooting_depth': -9.00,  # Default calculated by AquaCrop
        'water_layer': 0.0,
        'water_layer_ec': 0.00,
        'soil_water_content_type': 1,  # For specific depths
        'soil_data': [
            {'depth': 0.10, 'water_content': 14.0, 'ec': 0.00},
            {'depth': 0.30, 'water_content': 14.0, 'ec': 0.00},
            {'depth': 0.60, 'water_content': 14.0, 'ec': 0.00},
            {'depth': 1.00, 'water_content': 14.0, 'ec': 0.00},
            {'depth': 1.50, 'water_content': 14.0, 'ec': 0.00}
        ]
    }
)

# Wet soil with water layer on surface (flooded conditions)
flooded_initial = InitialConditions(
    name="FloodedInitial",
    description="Initial soil water content at saturation with water layer on surface",
    params={
        'initial_canopy_cover': -9.00,  # Default calculated by AquaCrop
        'initial_biomass': 0.000,
        'initial_rooting_depth': -9.00,  # Default calculated by AquaCrop
        'water_layer': 50.0,  # 50mm water layer on surface
        'water_layer_ec': 0.20,  # Slight salinity in water layer
        'soil_water_content_type': 1,  # For specific depths
        'soil_data': [
            {'depth': 0.10, 'water_content': 46.0, 'ec': 0.00},
            {'depth': 0.30, 'water_content': 46.0, 'ec': 0.00},
            {'depth': 0.60, 'water_content': 46.0, 'ec': 0.00},
            {'depth': 1.00, 'water_content': 46.0, 'ec': 0.00},
            {'depth': 1.50, 'water_content': 46.0, 'ec': 0.00}
        ]
    }
)

# Initial conditions with existing crop canopy
established_crop_initial = InitialConditions(
    name="EstablishedCropInitial",
    description="Initial conditions with already established crop canopy",
    params={
        'initial_canopy_cover': 30.00,  # 30% initial canopy cover
        'initial_biomass': 0.500,  # 0.5 ton/ha initial biomass
        'initial_rooting_depth': 0.30,  # 30cm initial rooting depth
        'water_layer': 0.0,
        'water_layer_ec': 0.00,
        'soil_water_content_type': 1,  # For specific depths
        'soil_data': [
            {'depth': 0.10, 'water_content': 25.0, 'ec': 0.00},
            {'depth': 0.30, 'water_content': 27.0, 'ec': 0.00},
            {'depth': 0.60, 'water_content': 28.0, 'ec': 0.00},
            {'depth': 1.00, 'water_content': 28.0, 'ec': 0.00},
            {'depth': 1.50, 'water_content': 28.0, 'ec': 0.00}
        ]
    }
)

# Soil with salinity gradient
saline_soil_initial = InitialConditions(
    name="SalineSoilInitial",
    description="Initial conditions with salinity gradient in soil profile",
    params={
        'initial_canopy_cover': -9.00,  # Default calculated by AquaCrop
        'initial_biomass': 0.000,
        'initial_rooting_depth': -9.00,  # Default calculated by AquaCrop
        'water_layer': 0.0,
        'water_layer_ec': 0.00,
        'soil_water_content_type': 1,  # For specific depths
        'soil_data': [
            {'depth': 0.10, 'water_content': 25.0, 'ec': 2.00},
            {'depth': 0.30, 'water_content': 25.0, 'ec': 3.00},
            {'depth': 0.60, 'water_content': 25.0, 'ec': 4.00},
            {'depth': 1.00, 'water_content': 25.0, 'ec': 5.00},
            {'depth': 1.50, 'water_content': 25.0, 'ec': 6.00}
        ]
    }
)