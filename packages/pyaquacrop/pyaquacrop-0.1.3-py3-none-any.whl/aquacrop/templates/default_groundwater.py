from aquacrop import GroundWater

# No groundwater table
no_groundwater = GroundWater(
    name="NoGroundwater",
    description="No groundwater table influence",
    params={
        'groundwater_type': 0  # No groundwater table
    }
)

# Fixed shallow groundwater table at 1.0 m
shallow_groundwater = GroundWater(
    name="ShallowGroundwater",
    description="Fixed shallow groundwater table at 1.0 m depth",
    params={
        'groundwater_type': 1,  # Fixed groundwater table
        'groundwater_observations': [
            {'day': 1, 'depth': 1.0, 'ec': 0.5}  # Day 1, depth 1.0 m, EC 0.5 dS/m
        ]
    }
)

# Fixed deep groundwater table at 3.0 m
deep_groundwater = GroundWater(
    name="DeepGroundwater",
    description="Fixed deep groundwater table at 3.0 m depth",
    params={
        'groundwater_type': 1,  # Fixed groundwater table
        'groundwater_observations': [
            {'day': 1, 'depth': 3.0, 'ec': 0.5}  # Day 1, depth 3.0 m, EC 0.5 dS/m
        ]
    }
)

# Variable groundwater table (rising over time)
rising_groundwater = GroundWater(
    name="RisingGroundwater",
    description="Groundwater table rising over time",
    params={
        'groundwater_type': 2,  # Variable groundwater table
        'first_day': 1,
        'first_month': 1,
        'first_year': 2014,
        'groundwater_observations': [
            {'day': 1, 'depth': 3.0, 'ec': 0.5},     # Day 1, depth 3.0 m
            {'day': 30, 'depth': 2.8, 'ec': 0.5},    # Day 30, depth 2.8 m
            {'day': 60, 'depth': 2.5, 'ec': 0.5},    # Day 60, depth 2.5 m
            {'day': 90, 'depth': 2.2, 'ec': 0.5},    # Day 90, depth 2.2 m
            {'day': 120, 'depth': 2.0, 'ec': 0.5},   # Day 120, depth 2.0 m
            {'day': 150, 'depth': 1.8, 'ec': 0.5},   # Day 150, depth 1.8 m
            {'day': 180, 'depth': 1.5, 'ec': 0.5},   # Day 180, depth 1.5 m
        ]
    }
)

# Variable groundwater table (dropping over time)
dropping_groundwater = GroundWater(
    name="DroppingGroundwater",
    description="Groundwater table dropping over time",
    params={
        'groundwater_type': 2,  # Variable groundwater table
        'first_day': 1,
        'first_month': 1,
        'first_year': 2014,
        'groundwater_observations': [
            {'day': 1, 'depth': 1.5, 'ec': 0.5},     # Day 1, depth 1.5 m
            {'day': 30, 'depth': 1.8, 'ec': 0.5},    # Day 30, depth 1.8 m
            {'day': 60, 'depth': 2.0, 'ec': 0.5},    # Day 60, depth 2.0 m
            {'day': 90, 'depth': 2.2, 'ec': 0.5},    # Day 90, depth 2.2 m
            {'day': 120, 'depth': 2.5, 'ec': 0.5},   # Day 120, depth 2.5 m
            {'day': 150, 'depth': 2.8, 'ec': 0.5},   # Day 150, depth 2.8 m
            {'day': 180, 'depth': 3.0, 'ec': 0.5},   # Day 180, depth 3.0 m
        ]
    }
)

# Variable saline groundwater table
saline_groundwater = GroundWater(
    name="SalineGroundwater",
    description="Variable saline groundwater table",
    params={
        'groundwater_type': 2,  # Variable groundwater table
        'first_day': 1,
        'first_month': 1,
        'first_year': 2014,
        'groundwater_observations': [
            {'day': 1, 'depth': 2.0, 'ec': 3.0},     # Day 1, depth 2.0 m, EC 3.0 dS/m
            {'day': 60, 'depth': 1.8, 'ec': 3.5},    # Day 60, depth 1.8 m, EC 3.5 dS/m
            {'day': 120, 'depth': 1.5, 'ec': 4.0},   # Day 120, depth 1.5 m, EC 4.0 dS/m
            {'day': 180, 'depth': 1.8, 'ec': 3.5},   # Day 180, depth 1.8 m, EC 3.5 dS/m
        ]
    }
)