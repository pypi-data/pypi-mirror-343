"""
Daily Results settings generator for AquaCrop (DailyResults.SIM)
"""

import os
from typing import List, Optional

def generate_daily_results_settings(
    file_path: str,
    output_types: Optional[List[int]] = None
) -> str:
    """
    Generate an AquaCrop daily results settings file (DailyResults.SIM)
    
    Args:
        file_path: Path to write the file
        output_types: List of daily output types to enable:
            1: Various parameters of the soil water balance
            2: Crop development and production
            3: Soil water content in the soil profile and root zone
            4: Soil salinity in the soil profile and root zone
            5: Soil water content at various depths of the soil profile
            6: Soil salinity at various depths of the soil profile
            7: Climate input parameters
            8: Irrigation events and intervals
            If None, all types (1-7) will be enabled
    
    Returns:
        The path to the generated file
    """
    if output_types is None:
        output_types = [1, 2, 3, 4, 5, 6, 7]
    
    # Map of output types to descriptions
    type_descriptions = {
        1: "Various parameters of the soil water balance",
        2: "Crop development and production",
        3: "Soil water content in the soil profile and root zone",
        4: "Soil salinity in the soil profile and root zone",
        5: "Soil water content at various depths of the soil profile",
        6: "Soil salinity at various depths of the soil profile",
        7: "Climate input parameters",
        8: "Irrigation events and intervals"
    }
    
    lines = []
    
    # Add enabled output types
    for output_type in sorted(output_types):
        if output_type in type_descriptions:
            lines.append(f" {output_type} : {type_descriptions[output_type]}")
    
    # Add extra newline for compatibility with reference file
    lines.append("")
    
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path