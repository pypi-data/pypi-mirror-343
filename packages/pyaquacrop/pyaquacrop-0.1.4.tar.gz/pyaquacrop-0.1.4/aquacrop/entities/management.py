from typing import Any, Dict, List, Optional

from aquacrop.file_generators.DATA.man_generator import generate_management_file


class FieldManagement:
    """
    Represents field management practices for AquaCrop simulation
    """

    def __init__(
        self, name: str, description: str, params: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a field management entity

        Args:
            name: Management name (used for file naming)
            description: Management description
            params: Dictionary of management parameters including:
                - fertility_stress: Degree of soil fertility stress (%)
                - mulch_cover: Percentage of ground surface covered by mulches
                - bund_height: Height of soil bunds
                - And various weed and cutting parameters (see man_generator.py)
        """
        self.name = "".join(name.split())
        self.description = description
        self.params = {
            "fertility_stress": 50,
            "mulch_cover": 0,
            "mulch_effect": 50,
            "bund_height": 0.00,
            "surface_runoff_affected": 0,
            "runoff_adjustment": 0,
            "weed_cover_initial": 0,
            "weed_cover_increase": 0,
            "weed_shape_factor": 100.00,
            "weed_replacement": 100,
            # TODO: Even for non-perennial crops, these parameters MUST be included
            "multiple_cuttings": False,  # Explicitly disable multiple cuttings
            "canopy_after_cutting": 25,  # Default value - required by Fortran code
            "cgc_increase_after_cutting": 20,  # Required by Fortran code
            "cutting_window_start_day": 1,
            "cutting_window_length": -9,
            "cutting_schedule_type": 0,
            "cutting_time_criterion": 0,
            "final_harvest_at_maturity": 0,
            "day_nr_base": 41274,
        }
        # Update with provided parameters
        if params:
            self.params.update(params)

    def generate_file(self, directory: str) -> str:
        """Generate management file in directory and return file path"""
        return generate_management_file(
            file_path=f"{directory}/{self.name}.MAN",
            description=self.description,
            **self.params,
        )
