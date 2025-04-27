from aquacrop import Irrigation

# No irrigation (rainfed conditions)
rainfed = None  # Just use None for rainfed conditions

# Sprinkler irrigation with fixed schedule
sprinkler_fixed_schedule = Irrigation(
    name="Sprinkler Fixed Schedule",
    description="Sprinkler irrigation with fixed schedule every 10 days",
    params={
        'irrigation_method': 1,  # Sprinkler
        'surface_wetted': 100,
        'irrigation_mode': 1,  # Specification of events
        'reference_day': -9,  # Reference day is onset of growing period
        'irrigation_events': [
            {'day': 10, 'depth': 30, 'ec': 0.0},
            {'day': 20, 'depth': 30, 'ec': 0.0},
            {'day': 30, 'depth': 30, 'ec': 0.0},
            {'day': 40, 'depth': 30, 'ec': 0.0},
            {'day': 50, 'depth': 30, 'ec': 0.0},
            {'day': 60, 'depth': 30, 'ec': 0.0},
            {'day': 70, 'depth': 30, 'ec': 0.0},
            {'day': 80, 'depth': 30, 'ec': 0.0},
            {'day': 90, 'depth': 30, 'ec': 0.0},
        ]
    }
)

# Drip irrigation with fixed schedule
drip_fixed_schedule = Irrigation(
    name="Drip Fixed Schedule",
    description="Drip irrigation with fixed schedule every 7 days",
    params={
        'irrigation_method': 5,  # Drip
        'surface_wetted': 30,
        'irrigation_mode': 1,  # Specification of events
        'reference_day': -9,  # Reference day is onset of growing period
        'irrigation_events': [
            {'day': 7, 'depth': 15, 'ec': 0.0},
            {'day': 14, 'depth': 15, 'ec': 0.0},
            {'day': 21, 'depth': 15, 'ec': 0.0},
            {'day': 28, 'depth': 15, 'ec': 0.0},
            {'day': 35, 'depth': 15, 'ec': 0.0},
            {'day': 42, 'depth': 15, 'ec': 0.0},
            {'day': 49, 'depth': 15, 'ec': 0.0},
            {'day': 56, 'depth': 15, 'ec': 0.0},
            {'day': 63, 'depth': 15, 'ec': 0.0},
            {'day': 70, 'depth': 15, 'ec': 0.0},
            {'day': 77, 'depth': 15, 'ec': 0.0},
            {'day': 84, 'depth': 15, 'ec': 0.0},
            {'day': 91, 'depth': 15, 'ec': 0.0},
        ]
    }
)

# Sprinkler irrigation with automatic schedule based on depletion
sprinkler_auto_schedule = Irrigation(
    name="Sprinkler Auto Schedule",
    description="Sprinkler irrigation with automatic schedule based on 50% depletion of RAW",
    params={
        'irrigation_method': 1,  # Sprinkler
        'surface_wetted': 100,
        'irrigation_mode': 2,  # Generate schedule
        'time_criterion': 3,  # % of RAW
        'depth_criterion': 1,  # Back to Field Capacity
        'generation_rules': [
            {'from_day': 1, 'time_value': 50, 'depth_value': 0, 'ec': 0.0}  # 50% of RAW
        ]
    }
)

# Basin irrigation with automatic schedule
basin_auto_schedule = Irrigation(
    name="Basin Auto Schedule",
    description="Basin irrigation with automatic schedule based on 60% depletion of RAW",
    params={
        'irrigation_method': 2,  # Basin
        'surface_wetted': 100,
        'irrigation_mode': 2,  # Generate schedule
        'time_criterion': 3,  # % of RAW
        'depth_criterion': 1,  # Back to Field Capacity
        'generation_rules': [
            {'from_day': 1, 'time_value': 60, 'depth_value': 0, 'ec': 0.0}  # 60% of RAW
        ]
    }
)

# Furrow irrigation with automatic schedule
furrow_auto_schedule = Irrigation(
    name="Furrow Auto Schedule",
    description="Furrow irrigation with automatic schedule based on 70% depletion of RAW",
    params={
        'irrigation_method': 4,  # Furrow
        'surface_wetted': 60,
        'irrigation_mode': 2,  # Generate schedule
        'time_criterion': 3,  # % of RAW
        'depth_criterion': 1,  # Back to Field Capacity
        'generation_rules': [
            {'from_day': 1, 'time_value': 70, 'depth_value': 0, 'ec': 0.0}  # 70% of RAW
        ]
    }
)

# Drip irrigation with automatic schedule (frequent but small amounts)
drip_auto_schedule = Irrigation(
    name="Drip Auto Schedule",
    description="Drip irrigation with automatic schedule based on 40% depletion of RAW",
    params={
        'irrigation_method': 5,  # Drip
        'surface_wetted': 30,
        'irrigation_mode': 2,  # Generate schedule
        'time_criterion': 3,  # % of RAW
        'depth_criterion': 1,  # Back to Field Capacity
        'generation_rules': [
            {'from_day': 1, 'time_value': 40, 'depth_value': 0, 'ec': 0.0}  # 40% of RAW
        ]
    }
)

# Net irrigation requirement determination
net_irrigation_requirement = Irrigation(
    name="Net Irrigation Requirement",
    description="Determination of net irrigation requirement",
    params={
        'irrigation_method': 1,  # Sprinkler
        'surface_wetted': 100,
        'irrigation_mode': 3,  # Determine net irrigation requirement
        'depletion_threshold': 50  # % RAW below which soil water may not drop
    }
)

# Saline irrigation (with EC of 2.0 dS/m)
saline_irrigation = Irrigation(
    name="Saline Irrigation",
    description="Irrigation with saline water (EC = 2.0 dS/m)",
    params={
        'irrigation_method': 1,  # Sprinkler
        'surface_wetted': 100,
        'irrigation_mode': 1,  # Specification of events
        'reference_day': -9,  # Reference day is onset of growing period
        'irrigation_events': [
            {'day': 10, 'depth': 30, 'ec': 2.0},
            {'day': 20, 'depth': 30, 'ec': 2.0},
            {'day': 30, 'depth': 30, 'ec': 2.0},
            {'day': 40, 'depth': 30, 'ec': 2.0},
            {'day': 50, 'depth': 30, 'ec': 2.0},
            {'day': 60, 'depth': 30, 'ec': 2.0},
            {'day': 70, 'depth': 30, 'ec': 2.0},
            {'day': 80, 'depth': 30, 'ec': 2.0},
            {'day': 90, 'depth': 30, 'ec': 2.0},
        ]
    }
)