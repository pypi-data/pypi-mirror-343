"""
Groundwater file generator for AquaCrop (.GWT files)
"""
import os
from typing import List, Optional, Dict, Union
from datetime import datetime

from aquacrop.constants import Constants

def generate_groundwater_file(
    file_path: str,
    description: str,
    groundwater_type: int = 0,
    
    # For types 1 and 2 (fixed or variable groundwater table)
    first_day: int = 1,
    first_month: int = 1,
    first_year: int = 1901,  # 1901 if not linked to a specific year
    
    # Groundwater observations
    groundwater_observations: Optional[List[Dict[str, Union[int, float]]]] = None,
) -> str:
    """
    Generate an AquaCrop groundwater file (.GWT) with all possible parameters
    
    Args:
        file_path: Path to write the file
        description: Groundwater description
        
        # Basic groundwater parameters
        groundwater_type: Type code
                         (0: no groundwater table, 
                          1: groundwater table at fixed depth and with constant salinity,
                          2: variable groundwater table)
        
        # For types 1 and 2 (fixed or variable groundwater table)
        first_day: First day of observations
        first_month: First month of observations
        first_year: First year of observations (1901 if not linked to a specific year)
        
        # Groundwater observations
        groundwater_observations: List of dicts with keys 'day', 'depth', 'ec' for each groundwater observation
    
    Returns:
        The path to the generated file
    """
    # Initialize observations list if not provided
    if groundwater_observations is None:
        groundwater_observations = []
    
    # Generate groundwater file content
    lines = [
        f"{description}",
        f" {Constants.AQUACROP_VERSION_NUMBER} : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
        f" {groundwater_type} : {_get_groundwater_type_description(groundwater_type)}",
    ]
    
    # Add type-specific content
    if groundwater_type == 0:  # No groundwater table
        pass  # No additional info needed
    
    elif groundwater_type in [1, 2]:  # Fixed or variable groundwater table
        # Add date information if variable groundwater table
        if groundwater_type == 2:
            lines.extend([
                f" {first_day} : first day of observations",
                f" {first_month} : first month of observations",
                f" {first_year} : first year of observations {_get_year_description(first_year)}",
                f"",
            ])
        
        # Add table header
        lines.extend([
            f" Day Depth (m) ECw (dS/m)",
            f"====================================",
        ])
        
        # Add groundwater observations
        for observation in groundwater_observations:
            lines.append(f" {observation['day']} {observation['depth']:.2f} {observation['ec']:.1f}")
    
    # Write the content to file
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path

def _get_groundwater_type_description(type_code: int) -> str:
    """Get the description for groundwater type code"""
    types = {
        0: "no groundwater table",
        1: "groundwater table at fixed depth and with constant salinity",
        2: "variable groundwater table"
    }
    return types.get(type_code, "Unknown groundwater type")

def _get_year_description(year: int) -> str:
    """Get description for year value"""
    if year == 1901:
        return "(1901 if not linked to a specific year)"
    else:
        return ""

