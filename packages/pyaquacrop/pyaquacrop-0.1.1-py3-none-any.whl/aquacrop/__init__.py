"""
AquaCrop Python API - A Python wrapper for the AquaCrop crop growth model
"""

__version__ = "0.1.1"

# Import core classes first
from aquacrop.entities.crop import Crop
from aquacrop.entities.soil import Soil, SoilLayer
from aquacrop.entities.climate import Weather
from aquacrop.entities.irrigation import Irrigation
from aquacrop.entities.management import FieldManagement
from aquacrop.entities.calendar import Calendar
from aquacrop.entities.off_season import OffSeason
from aquacrop.entities.observation import Observation
from aquacrop.entities.ground_water import GroundWater
from aquacrop.entities.initial_conditions import InitialConditions
from aquacrop.entities.parameter import Parameter
from aquacrop.aquacrop import AquaCrop

# Import presets module - but DON'T import from it
import aquacrop.templates

# Explicitly re-export all the classes we want to expose at the top level
__all__ = [
    "Crop",
    "Soil",
    "SoilLayer",
    "Weather",
    "FieldManagement",
    "Irrigation",
    "Calendar",
    "OffSeason",
    "Observation",
    "GroundWater",
    "InitialConditions",
    "Parameter",
    "AquaCrop",
]
