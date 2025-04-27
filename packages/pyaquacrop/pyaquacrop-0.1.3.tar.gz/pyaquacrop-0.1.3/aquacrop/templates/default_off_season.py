from aquacrop import OffSeason

# Default off-season with no special conditions
default_off_season = OffSeason(
    name="Default OffSeason",
    description="Default off-season conditions with no mulch or irrigation",
    params={
        'mulch_cover_before': 0,
        'mulch_cover_after': 0,
        'mulch_effect': 50,
        'num_irrigation_before': 0,
        'num_irrigation_after': 0,
    }
)

# Off-season with mulch cover
mulched_off_season = OffSeason(
    name="Mulched OffSeason",
    description="Off-season with mulch cover both before and after growing period",
    params={
        'mulch_cover_before': 70,  # 70% mulch cover before growing period
        'mulch_cover_after': 70,   # 70% mulch cover after growing period
        'mulch_effect': 80,        # 80% effect on evaporation reduction
        'num_irrigation_before': 0,
        'num_irrigation_after': 0,
    }
)

# Off-season with pre-irrigation
pre_irrigated_off_season = OffSeason(
    name="Pre-Irrigated OffSeason",
    description="Off-season with irrigation events before growing period",
    params={
        'mulch_cover_before': 0,
        'mulch_cover_after': 0,
        'mulch_effect': 50,
        'num_irrigation_before': 2,
        'irrigation_quality_before': 0.3,
        'irrigation_events_before': [
            {'day': 15, 'depth': 40},
            {'day': 30, 'depth': 40}
        ],
        'num_irrigation_after': 0,
        'surface_wetted_offseason': 100
    }
)

# Off-season with post-irrigation
post_irrigated_off_season = OffSeason(
    name="Post-Irrigated OffSeason",
    description="Off-season with irrigation events after growing period",
    params={
        'mulch_cover_before': 0,
        'mulch_cover_after': 0,
        'mulch_effect': 50,
        'num_irrigation_before': 0,
        'num_irrigation_after': 2,
        'irrigation_quality_after': 0.3,
        'irrigation_events_after': [
            {'day': 15, 'depth': 40},
            {'day': 30, 'depth': 40}
        ],
        'surface_wetted_offseason': 100
    }
)

# Off-season with both pre and post irrigation
full_irrigated_off_season = OffSeason(
    name="Fully Irrigated OffSeason",
    description="Off-season with irrigation events both before and after growing period",
    params={
        'mulch_cover_before': 0,
        'mulch_cover_after': 0,
        'mulch_effect': 50,
        'num_irrigation_before': 2,
        'irrigation_quality_before': 0.3,
        'irrigation_events_before': [
            {'day': 15, 'depth': 40},
            {'day': 30, 'depth': 40}
        ],
        'num_irrigation_after': 2,
        'irrigation_quality_after': 0.3,
        'irrigation_events_after': [
            {'day': 15, 'depth': 40},
            {'day': 30, 'depth': 40}
        ],
        'surface_wetted_offseason': 100
    }
)

# Off-season with saline irrigation
saline_irrigated_off_season = OffSeason(
    name="Saline Irrigated OffSeason",
    description="Off-season with saline irrigation events",
    params={
        'mulch_cover_before': 0,
        'mulch_cover_after': 0,
        'mulch_effect': 50,
        'num_irrigation_before': 1,
        'irrigation_quality_before': 3.0,  # 3.0 dS/m (saline water)
        'irrigation_events_before': [
            {'day': 15, 'depth': 50}
        ],
        'num_irrigation_after': 1,
        'irrigation_quality_after': 3.0,  # 3.0 dS/m (saline water)
        'irrigation_events_after': [
            {'day': 15, 'depth': 50}
        ],
        'surface_wetted_offseason': 100
    }
)

# Off-season with mulch and irrigation
mulched_irrigated_off_season = OffSeason(
    name="Mulched Irrigated OffSeason",
    description="Off-season with mulch cover and irrigation events",
    params={
        'mulch_cover_before': 60,
        'mulch_cover_after': 60,
        'mulch_effect': 70,
        'num_irrigation_before': 1,
        'irrigation_quality_before': 0.3,
        'irrigation_events_before': [
            {'day': 20, 'depth': 40}
        ],
        'num_irrigation_after': 1,
        'irrigation_quality_after': 0.3,
        'irrigation_events_after': [
            {'day': 20, 'depth': 40}
        ],
        'surface_wetted_offseason': 100
    }
)