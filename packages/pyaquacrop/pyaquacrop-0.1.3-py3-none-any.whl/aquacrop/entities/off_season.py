from typing import Dict, Any
from aquacrop.file_generators.DATA.off_generator import generate_offseason_file

class OffSeason:
    """
    Represents off-season conditions for AquaCrop simulation
    """
    def __init__(self, name: str, description: str, params: Dict[str, Any] = None):
        """
        Initialize an off-season entity
        
        Args:
            name: Off-season name (used for file naming)
            description: Off-season description
            params: Dictionary of off-season parameters including:
                - mulch_cover_before: % ground covered by mulches BEFORE growing period
                - mulch_cover_after: % ground covered by mulches AFTER growing period
                - And irrigation parameters (see off_generator.py)
        """
        self.name = "".join(name.split())
        self.description = description
        self.params = {
            'mulch_cover_before': 0,
            'mulch_cover_after': 0,
            'mulch_effect': 50,
            'num_irrigation_before': 0,
            'irrigation_quality_before': 0.0,
            'irrigation_events_before': [],
            'num_irrigation_after': 0,
            'irrigation_quality_after': 0.0,
            'irrigation_events_after': [],
            'surface_wetted_offseason': 100
        }
        # Update with provided parameters
        if params:
            self.params.update(params)
        
    def generate_file(self, directory: str) -> str:
        """Generate off-season conditions file in directory and return file path"""
        return generate_offseason_file(
            file_path=f"{directory}/{self.name}.OFF",
            description=self.description,
            **self.params
        )