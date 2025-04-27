from aquacrop import FieldManagement

# Ottawa management settings from test reference
ottawa_management = FieldManagement(
    name="Ottawa Alfalfa",
    description="Ottawa, Canada alfalfa field management with multiple cuttings",
    params={
        'fertility_stress': 50,
        'mulch_cover': 0,
        'mulch_effect': 50,
        'bund_height': 0.00,
        'surface_runoff_affected': 0,
        'runoff_adjustment': 0,
        'weed_cover_initial': 0,
        'weed_cover_increase': 0,
        'weed_shape_factor': 100.00,
        'weed_replacement': 100,
        'multiple_cuttings': True,
        'canopy_after_cutting': 25,
        'cgc_increase_after_cutting': 20,
        'cutting_window_start_day': 1,
        'cutting_window_length': -9,
        'cutting_schedule_type': 0,
        'cutting_time_criterion': 0,
        'final_harvest_at_maturity': 0,
        'day_nr_base': 41274,
        'harvest_days': [194, 243, 536, 572, 607, 897, 932, 972]
    }
)

# Default management with no fertility stress
optimal_management = FieldManagement(
    name="Optimal Field Management",
    description="Optimal field management with no fertility stress",
    params={
        'fertility_stress': 0,
        'mulch_cover': 0,
        'mulch_effect': 50,
        'bund_height': 0.00,
        'surface_runoff_affected': 0,
        'runoff_adjustment': 0,
        'weed_cover_initial': 0,
        'weed_cover_increase': 0,
        'weed_shape_factor': 100.00,
        'weed_replacement': 100,
        'multiple_cuttings': False,
    }
)

# Management with moderate fertility stress
moderate_fertility_stress = FieldManagement(
    name="Moderate Fertility Stress",
    description="Field management with moderate fertility stress",
    params={
        'fertility_stress': 30,
        'mulch_cover': 0,
        'mulch_effect': 50,
        'bund_height': 0.00,
        'surface_runoff_affected': 0,
        'runoff_adjustment': 0,
        'weed_cover_initial': 0,
        'weed_cover_increase': 0,
        'weed_shape_factor': 100.00,
        'weed_replacement': 100,
        'multiple_cuttings': False,
    }
)

# Management with high fertility stress
high_fertility_stress = FieldManagement(
    name="High Fertility Stress",
    description="Field management with high fertility stress",
    params={
        'fertility_stress': 80,
        'mulch_cover': 0,
        'mulch_effect': 50,
        'bund_height': 0.00,
        'surface_runoff_affected': 0,
        'runoff_adjustment': 0,
        'weed_cover_initial': 0,
        'weed_cover_increase': 0,
        'weed_shape_factor': 100.00,
        'weed_replacement': 100,
        'multiple_cuttings': False,
    }
)

# Management with mulch cover
mulched_management = FieldManagement(
    name="Mulched Field Management",
    description="Field management with mulch cover",
    params={
        'fertility_stress': 20,
        'mulch_cover': 70,
        'mulch_effect': 80,
        'bund_height': 0.00,
        'surface_runoff_affected': 0,
        'runoff_adjustment': 0,
        'weed_cover_initial': 0,
        'weed_cover_increase': 0,
        'weed_shape_factor': 100.00,
        'weed_replacement': 100,
        'multiple_cuttings': False,
    }
)

# Management with weed presence
weedy_management = FieldManagement(
    name="Weedy Field Management",
    description="Field management with weed presence",
    params={
        'fertility_stress': 30,
        'mulch_cover': 0,
        'mulch_effect': 50,
        'bund_height': 0.00,
        'surface_runoff_affected': 0,
        'runoff_adjustment': 0,
        'weed_cover_initial': 20,
        'weed_cover_increase': 15,
        'weed_shape_factor': 100.00,
        'weed_replacement': 100,
        'multiple_cuttings': False,
    }
)