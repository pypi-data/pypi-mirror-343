from typing import Any, Dict, Optional

from aquacrop.file_generators.DATA.gwt_generator import generate_groundwater_file


class GroundWater:
    """
    Represents groundwater conditions for AquaCrop simulation
    """

    def __init__(
        self, name: str, description: str, params: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a groundwater entity

        Args:
            name: Groundwater name (used for file naming)
            description: Groundwater description
            params: Dictionary of groundwater parameters including:
                - groundwater_type: Type code (0: none, 1: fixed, 2: variable)
                - first_day/month/year: When observations start
                - groundwater_observations: List of observations
        """
        self.name = "".join(name.split())
        self.description = description
        self.params = {
            "groundwater_type": 0,
            "first_day": 1,
            "first_month": 1,
            "first_year": 1901,
            "groundwater_observations": [],
        }
        # Update with provided parameters
        if params:
            self.params.update(params)

    def generate_file(self, directory: str) -> str:
        """Generate groundwater file in directory and return file path"""
        return generate_groundwater_file(
            file_path=f"{directory}/{self.name}.GWT",
            description=self.description,
            **self.params,
        )
