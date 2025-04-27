"""
Off-season conditions file generator for AquaCrop (.OFF files)
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Union

from aquacrop.constants import Constants


def generate_offseason_file(
    file_path: str,
    description: str,
    # Mulches
    mulch_cover_before: int = 0,
    mulch_cover_after: int = 0,
    mulch_effect: int = 50,
    # Irrigation events before growing period
    num_irrigation_before: int = 0,
    irrigation_quality_before: float = 0.0,
    irrigation_events_before: Optional[List[Dict[str, Union[int, float]]]] = None,
    # Irrigation events after growing period
    num_irrigation_after: int = 0,
    irrigation_quality_after: float = 0.0,
    irrigation_events_after: Optional[List[Dict[str, Union[int, float]]]] = None,
    # Irrigation surface wetted
    surface_wetted_offseason: int = 100,
) -> str:
    """
    Generate an AquaCrop off-season conditions file (.OFF) with all possible parameters

    Args:
        file_path: Path to write the file
        description: Off-season description

        # Mulches
        mulch_cover_before: Percentage of ground surface covered by mulches BEFORE growing period
        mulch_cover_after: Percentage of ground surface covered by mulches AFTER growing period
        mulch_effect: Effect (%) of mulches on reduction of soil evaporation

        # Irrigation events before growing period
        num_irrigation_before: Number of irrigation events BEFORE growing period
        irrigation_quality_before: Quality of irrigation water BEFORE growing period (dS/m)
        irrigation_events_before: List of dicts with keys 'day', 'depth' for each irrigation event before

        # Irrigation events after growing period
        num_irrigation_after: Number of irrigation events AFTER growing period
        irrigation_quality_after: Quality of irrigation water AFTER growing period (dS/m)
        irrigation_events_after: List of dicts with keys 'day', 'depth' for each irrigation event after

        # Irrigation surface wetted
        surface_wetted_offseason: Percentage of soil surface wetted by off-season irrigation

    Returns:
        The path to the generated file
    """
    # Initialize event lists if not provided
    if irrigation_events_before is None:
        irrigation_events_before = []

    if irrigation_events_after is None:
        irrigation_events_after = []

    # Validate that the number of events matches the lists
    if len(irrigation_events_before) != num_irrigation_before:
        num_irrigation_before = len(irrigation_events_before)

    if len(irrigation_events_after) != num_irrigation_after:
        num_irrigation_after = len(irrigation_events_after)

    # Generate off-season file content
    lines = [
        f"{description}",
        f" {Constants.AQUACROP_VERSION_NUMBER} : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
        f" {mulch_cover_before} : percentage (%) of ground surface covered by mulches BEFORE growing period",
        f" {mulch_cover_after} : percentage (%) of ground surface covered by mulches AFTER growing period",
        f" {mulch_effect} : effect (%) of mulches on reduction of soil evaporation",
        f" {num_irrigation_before} : number of irrigation events BEFORE growing period",
        f" {irrigation_quality_before:.1f} : quality of irrigation water BEFORE growing period (dS/m)",
        f" {num_irrigation_after} : number of irrigation events AFTER growing period",
        f" {irrigation_quality_after:.1f} : quality of irrigation water AFTER growing period (dS/m)",
        f" {surface_wetted_offseason} : percentage (%) of soil surface wetted by off-season irrigation",
    ]

    # Add irrigation events if there are any
    if num_irrigation_before > 0 or num_irrigation_after > 0:
        lines.extend(
            [
                f" Day Depth(mm) When",
                f"=================================",
            ]
        )

        # Add irrigation events before growing period
        for event in irrigation_events_before:
            lines.append(f" {event['day']} {event['depth']} before season")

        # Add irrigation events after growing period
        for event in irrigation_events_after:
            lines.append(f" {event['day']} {event['depth']} after season")

    # Write the content to file
    content = "\n".join(lines)

    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)

    return file_path


# Example usage
if __name__ == "__main__":
    # Example matching Table 2.23v - 4 in the documentation
    irrigation_before = [{"day": 10, "depth": 40.0}]

    generate_offseason_file(
        file_path="example_offseason.off",
        description="Irrigation and field management conditions in the off-season",
        mulch_cover_before=0,
        mulch_cover_after=70,
        mulch_effect=50,
        num_irrigation_before=1,
        irrigation_quality_before=1.5,
        irrigation_events_before=irrigation_before,
        num_irrigation_after=0,
        irrigation_quality_after=4.0,
        surface_wetted_offseason=100,
    )

    # Example with both before and after irrigation events
    irrigation_before = [{"day": 15, "depth": 30.0}, {"day": 30, "depth": 45.0}]

    irrigation_after = [{"day": 10, "depth": 50.0}, {"day": 25, "depth": 40.0}]

    generate_offseason_file(
        file_path="example_offseason_complete.off",
        description="Off-season with irrigation events before and after growing period",
        mulch_cover_before=30,
        mulch_cover_after=60,
        mulch_effect=40,
        num_irrigation_before=2,
        irrigation_quality_before=1.2,
        irrigation_events_before=irrigation_before,
        num_irrigation_after=2,
        irrigation_quality_after=2.5,
        irrigation_events_after=irrigation_after,
        surface_wetted_offseason=100,
    )
