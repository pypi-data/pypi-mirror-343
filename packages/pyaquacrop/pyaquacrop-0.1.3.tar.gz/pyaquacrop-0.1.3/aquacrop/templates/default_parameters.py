from aquacrop import Parameter

# Ottawa parameters from test reference
ottawa_parameters = Parameter(
    name="Ottawa Parameters",
    params={
        'evaporation_decline_factor': 4,
        'kex': 1.10,
        'cc_threshold_for_hi': 5,
        'root_expansion_start_depth': 70,
        'max_root_expansion': 5.00,
        'shape_root_water_stress': -6,
        'germination_soil_water': 20,
        'fao_adjustment_factor': 1.0,
        'aeration_days': 3,
        'senescence_factor': 1.00,
        'senescence_reduction': 12,
        'top_soil_thickness': 10,
        'evaporation_depth': 30,
        'cn_depth': 0.30,
        'cn_adjustment': 1,
        'salt_diffusion_factor': 20,
        'salt_solubility': 100,
        'soil_water_gradient_factor': 16,
        'default_min_temp': 12.0,
        'default_max_temp': 28.0,
        'gdd_method': 3,
        'rainfall_estimation': 1,
        'effective_rainfall_pct': 70,
        'showers_per_decade': 2,
        'soil_evaporation_reduction': 5
    }
)

# Default parameters with modified evaporation settings
high_evaporation_parameters = Parameter(
    name="High Evaporation Parameters",
    params={
        'evaporation_decline_factor': 6,
        'kex': 1.20,
        'cc_threshold_for_hi': 5,
        'root_expansion_start_depth': 70,
        'max_root_expansion': 5.00,
        'shape_root_water_stress': -6,
        'germination_soil_water': 20,
        'fao_adjustment_factor': 1.0,
        'aeration_days': 3,
        'senescence_factor': 1.00,
        'senescence_reduction': 12,
        'top_soil_thickness': 10,
        'evaporation_depth': 40,
        'cn_depth': 0.30,
        'cn_adjustment': 1,
        'salt_diffusion_factor': 20,
        'salt_solubility': 100,
        'soil_water_gradient_factor': 16,
        'default_min_temp': 12.0,
        'default_max_temp': 28.0,
        'gdd_method': 3,
        'rainfall_estimation': 1,
        'effective_rainfall_pct': 70,
        'showers_per_decade': 2,
        'soil_evaporation_reduction': 5
    }
)

# Parameters with modified root expansion settings
deep_rooting_parameters = Parameter(
    name="Deep Rooting Parameters",
    params={
        'evaporation_decline_factor': 4,
        'kex': 1.10,
        'cc_threshold_for_hi': 5,
        'root_expansion_start_depth': 80,
        'max_root_expansion': 6.00,
        'shape_root_water_stress': -4,
        'germination_soil_water': 20,
        'fao_adjustment_factor': 1.0,
        'aeration_days': 3,
        'senescence_factor': 1.00,
        'senescence_reduction': 12,
        'top_soil_thickness': 10,
        'evaporation_depth': 30,
        'cn_depth': 0.30,
        'cn_adjustment': 1,
        'salt_diffusion_factor': 20,
        'salt_solubility': 100,
        'soil_water_gradient_factor': 16,
        'default_min_temp': 12.0,
        'default_max_temp': 28.0,
        'gdd_method': 3,
        'rainfall_estimation': 1,
        'effective_rainfall_pct': 70,
        'showers_per_decade': 2,
        'soil_evaporation_reduction': 5
    }
)

# Parameters for hot climate
hot_climate_parameters = Parameter(
    name="Hot Climate Parameters",
    params={
        'evaporation_decline_factor': 4,
        'kex': 1.10,
        'cc_threshold_for_hi': 5,
        'root_expansion_start_depth': 70,
        'max_root_expansion': 5.00,
        'shape_root_water_stress': -6,
        'germination_soil_water': 20,
        'fao_adjustment_factor': 1.0,
        'aeration_days': 3,
        'senescence_factor': 1.00,
        'senescence_reduction': 12,
        'top_soil_thickness': 10,
        'evaporation_depth': 30,
        'cn_depth': 0.30,
        'cn_adjustment': 1,
        'salt_diffusion_factor': 20,
        'salt_solubility': 100,
        'soil_water_gradient_factor': 16,
        'default_min_temp': 18.0,
        'default_max_temp': 35.0,
        'gdd_method': 3,
        'rainfall_estimation': 1,
        'effective_rainfall_pct': 70,
        'showers_per_decade': 2,
        'soil_evaporation_reduction': 5
    }
)