from typing import Any, Dict, Optional

from aquacrop.file_generators.DATA.sw0_generator import generate_initial_conditions_file


class InitialConditions:
    """
    Represents initial soil water conditions for AquaCrop simulation
    """

    def __init__(
        self, name: str, description: str, params: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize an initial conditions entity

        Args:
            name: Initial conditions name (used for file naming)
            description: Initial conditions description
            params: Dictionary of initial condition parameters including:
                - initial_canopy_cover: Canopy cover (%) at start of simulation
                - initial_biomass: Biomass (ton/ha) at start
                - soil_water_content_type: 0 for layers, 1 for depths
                - soil_data: List of soil water content by layer/depth
        """
        self.name = "".join(name.split())
        self.description = description
        self.params = {
            "initial_canopy_cover": -9.00,  # Default calculated by AquaCrop
            "initial_biomass": 0.000,
            "initial_rooting_depth": -9.00,  # Default calculated by AquaCrop
            "water_layer": 0.0,
            "water_layer_ec": 0.00,
            "soil_water_content_type": 0,  # For specific layers
            "soil_data": [],
        }
        # Update with provided parameters
        if params:
            self.params.update(params)

    def generate_file(self, directory: str) -> str:
        """Generate initial conditions file in directory and return file path"""
        return generate_initial_conditions_file(
            file_path=f"{directory}/{self.name}.SW0",
            description=self.description,
            **self.params,
        )
