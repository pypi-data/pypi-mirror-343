from typing import Dict, List
from aquacrop.file_generators.OBS.obs_generator import generate_observation_file

class Observation:
    """
    Represents field observations for AquaCrop simulation
    """
    def __init__(self, name: str, location: str, observations: List[Dict], 
                 soil_depth: float = 1.0, first_day: int = 1, 
                 first_month: int = 1, first_year: int = 2014):
        """
        Initialize an observation entity
        
        Args:
            name: Observation name (used for file naming)
            location: Location description
            observations: List of observation dictionaries with keys:
                - day: Day number
                - canopy_cover: Tuple of (mean, std) for canopy cover (%)
                - biomass: Tuple of (mean, std) for biomass (ton/ha)
                - soil_water: Tuple of (mean, std) for soil water content (mm)
            soil_depth: Depth of sampled soil profile (m)
            first_day: First day of observations
            first_month: First month of observations
            first_year: First year of observations
        """
        self.name = "".join(name.split())
        self.location = location
        self.observations = observations
        self.soil_depth = soil_depth
        self.first_day = first_day
        self.first_month = first_month
        self.first_year = first_year
        
    def generate_file(self, directory: str) -> str:
        """Generate observation file in directory and return file path"""
        return generate_observation_file(
            file_path=f"{directory}/{self.name}.OBS",
            location=self.location,
            observations=self.observations,
            soil_depth=self.soil_depth,
            first_day=self.first_day,
            first_month=self.first_month,
            first_year=self.first_year
        )