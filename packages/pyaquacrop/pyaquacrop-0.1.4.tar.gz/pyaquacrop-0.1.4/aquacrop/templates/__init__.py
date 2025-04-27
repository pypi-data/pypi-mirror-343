"""
Default entities for AquaCrop simulations including crops, soils, management, and more.
These pre-configured entities can be used directly in simulations.
"""

# Import and re-export all default entities
from aquacrop.templates.default_calendars import (
    early_spring_calendar,
    late_spring_calendar,
    may_21_calendar,
    rainfall_dependent,
    summer_calendar,
    temperature_dependent,
)
from aquacrop.templates.default_crops import ottawa_alfalfa
from aquacrop.templates.default_groundwater import (
    deep_groundwater,
    dropping_groundwater,
    no_groundwater,
    rising_groundwater,
    saline_groundwater,
    shallow_groundwater,
)
from aquacrop.templates.default_initial_conditions import (
    default_initial_conditions,
    dry_initial,
    established_crop_initial,
    field_capacity_initial,
    flooded_initial,
    saline_soil_initial,
    very_dry_initial,
)
from aquacrop.templates.default_irrigation import (
    basin_auto_schedule,
    drip_auto_schedule,
    drip_fixed_schedule,
    furrow_auto_schedule,
    net_irrigation_requirement,
    rainfed,
    saline_irrigation,
    sprinkler_auto_schedule,
    sprinkler_fixed_schedule,
)
from aquacrop.templates.default_management import (
    high_fertility_stress,
    moderate_fertility_stress,
    mulched_management,
    optimal_management,
    ottawa_management,
    weedy_management,
)
from aquacrop.templates.default_off_season import (
    default_off_season,
    full_irrigated_off_season,
    mulched_irrigated_off_season,
    mulched_off_season,
    post_irrigated_off_season,
    pre_irrigated_off_season,
    saline_irrigated_off_season,
)
from aquacrop.templates.default_parameters import (
    deep_rooting_parameters,
    high_evaporation_parameters,
    hot_climate_parameters,
    ottawa_parameters,
)
from aquacrop.templates.default_soils import (
    clay_soil,
    loam_soil,
    ottawa_sandy_loam,
    sandy_soil,
)

from aquacrop.templates.default_climate import (
    ottawa_temperatures,
    ottawa_eto,
    ottawa_rain,
    manuloa_co2_records,
)

# You could also create helpful groupings
default_crops = {"ottawa_alfalfa": ottawa_alfalfa}

default_soils = {
    "ottawa_sandy_loam": ottawa_sandy_loam,
    "sandy_soil": sandy_soil,
    "loam_soil": loam_soil,
    "clay_soil": clay_soil,
}

default_calendars = {
    "may_21_calendar": may_21_calendar,
    "early_spring_calendar": early_spring_calendar,
    "late_spring_calendar": late_spring_calendar,
    "summer_calendar": summer_calendar,
    "rainfall_dependent": rainfall_dependent,
    "temperature_dependent": temperature_dependent,
}

default_groundwater = {
    "no_groundwater": no_groundwater,
    "shallow_groundwater": shallow_groundwater,
    "deep_groundwater": deep_groundwater,
    "rising_groundwater": rising_groundwater,
    "dropping_groundwater": dropping_groundwater,
    "saline_groundwater": saline_groundwater,
}
default_initial_conditions = {
    "default_initial_conditions": default_initial_conditions,
    "dry_initial": dry_initial,
    "established_crop_initial": established_crop_initial,
    "field_capacity_initial": field_capacity_initial,
    "flooded_initial": flooded_initial,
    "saline_soil_initial": saline_soil_initial,
    "very_dry_initial": very_dry_initial,
}
default_irrigation = {
    "rainfed": rainfed,
    "net_irrigation_requirement": net_irrigation_requirement,
    "basin_auto_schedule": basin_auto_schedule,
    "drip_auto_schedule": drip_auto_schedule,
    "drip_fixed_schedule": drip_fixed_schedule,
    "furrow_auto_schedule": furrow_auto_schedule,
    "sprinkler_auto_schedule": sprinkler_auto_schedule,
    "sprinkler_fixed_schedule": sprinkler_fixed_schedule,
    "saline_irrigation": saline_irrigation,
}
default_management = {
    "optimal_management": optimal_management,
    "ottawa_management": ottawa_management,
    "weedy_management": weedy_management,
    "mulched_management": mulched_management,
    "high_fertility_stress": high_fertility_stress,
    "moderate_fertility_stress": moderate_fertility_stress,
}
default_off_season = {
    "default_off_season": default_off_season,
    "full_irrigated_off_season": full_irrigated_off_season,
    "mulched_irrigated_off_season": mulched_irrigated_off_season,
    "mulched_off_season": mulched_off_season,
    "post_irrigated_off_season": post_irrigated_off_season,
    "pre_irrigated_off_season": pre_irrigated_off_season,
    "saline_irrigated_off_season": saline_irrigated_off_season,
}
default_parameters = {
    "ottawa_parameters": ottawa_parameters,
    "deep_rooting_parameters": deep_rooting_parameters,
    "high_evaporation_parameters": high_evaporation_parameters,
    "hot_climate_parameters": hot_climate_parameters,
}

default_climate = {
    "ottawa_temperatures": ottawa_temperatures,
    "ottawa_eto": ottawa_eto,
    "ottawa_rainfall": ottawa_rain,
    "manuloa_co2_records": manuloa_co2_records,
}
