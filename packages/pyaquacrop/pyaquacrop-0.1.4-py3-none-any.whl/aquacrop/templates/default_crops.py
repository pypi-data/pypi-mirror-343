from aquacrop import Crop

ottawa_alfalfa = Crop(
        name="AlfalfaOttawa",
        description="Ottawa variety - Alfalfa - Louvain-La-Neuve (Belgium) -  adjusted for Ottawa - calibrated for Soil Fertility",
        params={
            # Basic classifications
            'crop_type': 4,  # forage crop
            'is_sown': True,
            'cycle_determination': 0,  # by growing degree-days
            'adjust_for_eto': True,
            
            # Temperature parameters
            'base_temp': 5.0,
            'upper_temp': 30.0,
            'gdd_cycle_length': 1920,
            'dormancy_eto_threshold': 600,
            
            # Crop water stress parameters
            'p_upper_canopy': 0.15,
            'p_lower_canopy': 0.55,
            'shape_canopy': 3.0,
            'p_upper_stomata': 0.60,
            'shape_stomata': 3.0,
            'p_upper_senescence': 0.70,
            'shape_senescence': 3.0,
            'p_upper_pollination': 0.90,
            'aeration_stress_threshold': 2,
            
            # Soil fertility stress parameters
            'fertility_stress_calibration': 50,
            'shape_fertility_canopy_expansion': 2.35,
            'shape_fertility_max_canopy': 0.79,
            'shape_fertility_water_productivity': -0.16,
            'shape_fertility_decline': 6.26,
            
            # Temperature stress parameters
            'cold_stress_for_pollination': 8,
            'heat_stress_for_pollination': 40,
            'minimum_growing_degrees_pollination': 8.0,
            
            # Salinity stress parameters
            'salinity_threshold_ece': 2,
            'salinity_max_ece': 16,
            'salinity_shape_factor': -9,
            'salinity_stress_cc': 25,
            'salinity_stress_stomata': 100,
            
            # Transpiration parameters
            'kc_max': 1.15,
            'kc_decline': 0.050,
            
            # Rooting parameters
            'min_rooting_depth': 0.30,
            'max_rooting_depth': 3.00,
            'root_expansion_shape': 15,
            'max_water_extraction_top': 0.020,
            'max_water_extraction_bottom': 0.010,
            'soil_evaporation_reduction': 60,
            
            # Canopy development parameters
            'canopy_cover_per_seedling': 2.50,
            'canopy_regrowth_size': 19.38,
            'plant_density': 2000000,
            'max_canopy_cover': 0.95,
            'canopy_growth_coefficient': 0.17713,
            'canopy_thinning_years': 9,
            'canopy_thinning_shape': 0.50,
            'canopy_decline_coefficient': 0.03636,
            
            # Crop cycle parameters (Calendar days)
            'days_emergence': 2,
            'days_max_rooting': 178,
            'days_senescence': 180,
            'days_maturity': 180,
            'days_flowering': 0,
            'days_flowering_length': 0,
            'days_crop_determinancy': 0,
            'days_hi_start': 17,
            
            # Crop cycle parameters (Growing degree days)
            'gdd_emergence': 5,
            'gdd_max_rooting': 1920,
            'gdd_senescence': 1920,
            'gdd_maturity': 1920,
            'gdd_flowering': 0,
            'gdd_flowering_length': 0,
            'cgc_gdd': 0.012,
            'cdc_gdd': 0.006,
            'gdd_hi_start': 118,
            
            # Biomass and yield parameters
            'water_productivity': 15.0,
            'water_productivity_yield_formation': 100,
            'co2_response_strength': 50,
            'harvest_index': 1.00,
            'water_stress_hi_increase': -9,
            'veg_growth_impact_hi': -9.0,
            'stomatal_closure_impact_hi': -9.0,
            'max_hi_increase': -9,
            'dry_matter_content': 20,
            
            # Perennial crop parameters
            'is_perennial': True,
            'first_year_min_rooting': 0.30,
            'assimilate_transfer': 1,
            'assimilate_storage_days': 100,
            'assimilate_transfer_percent': 65,
            'root_to_shoot_transfer_percent': 60,
            
            # Crop calendar for perennials
            'restart_type': 13,
            'restart_window_day': 1,
            'restart_window_month': 4,
            'restart_window_length': 120,
            'restart_gdd_threshold': 20.0,
            'restart_days_required': 8,
            'restart_occurrences': 2,
            'end_type': 63,
            'end_window_day': 31,
            'end_window_month': 10,
            'end_window_years_offset': 0,
            'end_window_length': 60,
            'end_gdd_threshold': 10.0,
            'end_days_required': 8,
            'end_occurrences': 1
        }
    )