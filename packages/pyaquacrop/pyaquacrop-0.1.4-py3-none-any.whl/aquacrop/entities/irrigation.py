from typing import Any, Dict, List, Optional

from aquacrop.file_generators.DATA.irr_generator import generate_irrigation_file


class Irrigation:
    """
    Represents irrigation parameters for AquaCrop simulation
    """

    def __init__(
        self, name: str, description: str, params: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize an irrigation entity

        Args:
            name: Irrigation name (used for file naming)
            description: Irrigation description
            params: Dictionary of irrigation parameters including:
                - irrigation_method: Method code (1: Sprinkler, 2: Basin, etc.)
                - surface_wetted: Percentage of soil surface wetted by irrigation
                - irrigation_mode: Mode code (1: Specification of events, etc.)
                - Plus mode-specific parameters (see irr_generator.py)
        """
        self.name = "".join(name.split())
        self.description = description
        self.params = {
            "irrigation_method": 1,
            "surface_wetted": 100,
            "irrigation_mode": 1,
            "reference_day": -9,
            "irrigation_events": [],
            "time_criterion": 1,
            "depth_criterion": 1,
            "generation_rules": [],
            "depletion_threshold": 50,
        }
        # Update with provided parameters
        if params:
            self.params.update(params)

    def generate_file(self, directory: str) -> str:
        """Generate irrigation file in directory and return file path"""
        return generate_irrigation_file(
            file_path=f"{directory}/{self.name}.IRR",
            description=self.description,
            **self.params,
        )
