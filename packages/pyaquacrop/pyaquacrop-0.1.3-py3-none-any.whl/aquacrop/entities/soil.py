from dataclasses import dataclass
from typing import List, Optional
from aquacrop.file_generators.DATA.sol_generator import generate_soil_file

@dataclass
class SoilLayer:
    """
    Represents a single soil horizon layer with hydraulic properties
    """
    thickness: float  # Thickness of horizon (m)
    sat: float        # Saturation point (vol %)
    fc: float         # Field capacity (vol %)
    wp: float         # Wilting point (vol %)
    ksat: float       # Saturated hydraulic conductivity (mm/day)
    penetrability: float = 100  # Root penetrability (%)
    gravel: float = 0  # Gravel content (%)
    cra: float = -0.3906  # Soil hydraulic parameter a
    crb: float = 1.2556  # Soil hydraulic parameter b
    description: str = "soil horizon"

class Soil:
    """
    Represents soil profile with multiple layers for AquaCrop simulation
    """
    def __init__(self, name: str, description: str, soil_layers: List[SoilLayer], 
                 curve_number: int = 61, readily_evaporable_water: int = 9):
        self.name = "".join(name.split())
        self.description = description
        self.soil_layers = soil_layers
        self.curve_number = curve_number
        self.readily_evaporable_water = readily_evaporable_water
        
    def generate_file(self, directory: str) -> str:
        """Generate soil file in directory and return file path"""
        # Convert soil layers to format expected by generator
        horizons = []
        for layer in self.soil_layers:
            horizons.append({
                'thickness': layer.thickness,
                'sat': layer.sat,
                'fc': layer.fc,
                'wp': layer.wp,
                'ksat': layer.ksat,
                'penetrability': layer.penetrability,
                'gravel': layer.gravel,
                'cra': layer.cra,
                'crb': layer.crb,
                'description': layer.description
            })
        
        # Generate and return file path
        return generate_soil_file(
            file_path=f"{directory}/{self.name}.SOL",
            description=self.description,
            horizons=horizons,
            curve_number=self.curve_number,
            readily_evaporable_water=self.readily_evaporable_water
        )