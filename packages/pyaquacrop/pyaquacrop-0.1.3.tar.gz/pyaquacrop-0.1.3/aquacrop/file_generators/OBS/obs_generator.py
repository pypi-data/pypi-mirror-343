"""
Observations file generator for AquaCrop (.OBS files)
"""

import os
from typing import List, Dict, Tuple, Optional
from aquacrop.constants import Constants
def generate_observation_file(
    file_path: str,
    location: str,
    observations: List[Dict],
    soil_depth: float = 1.0,
    first_day: int = 1,
    first_month: int = 1,
    first_year: int = 2014,

) -> str:
    """
    Generate an AquaCrop observations file (.OBS)
    
    Args:
        file_path: Path to write the file
        location: Location description
        observations: List of observation dictionaries, each containing:
            - day: Day number (required)
            - canopy_cover: Tuple of (mean, std) for canopy cover (%) (optional)
            - biomass: Tuple of (mean, std) for biomass (ton/ha) (optional)
            - soil_water: Tuple of (mean, std) for soil water content (mm) (optional)
        soil_depth: Depth of sampled soil profile (m)
        first_day: First day of observations
        first_month: First month of observations
        first_year: First year of observations
        version: AquaCrop version
    
    Returns:
        The path to the generated file
    """
    lines = [
        f"{location}",
        f"     {Constants.AQUACROP_VERSION_NUMBER}   : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
        f"     {soil_depth:.2f}  : depth of sampled soil profile",
        f"     {first_day}     : first day of observations",
        f"     {first_month}     : first month of observations",
        f"  {first_year}     : first year of observations (1901 if not linked to a specific year)",
        "",
        "   Day    Canopy cover (%)    dry Biomass (ton/ha)    Soil water content (mm)",
        "            Mean     Std         Mean       Std           Mean      Std",
        "============================================================================="
    ]
    
    # Sort observations by day
    sorted_obs = sorted(observations, key=lambda x: x['day'])
    
    for obs in sorted_obs:
        day = obs['day']
        
        # Get values or defaults
        cc_mean, cc_std = obs.get('canopy_cover', (-9.0, -9.0))
        bio_mean, bio_std = obs.get('biomass', (-9.0, -9.0))
        sw_mean, sw_std = obs.get('soil_water', (-9.0, -9.0))
        
        # Format biomass with right alignment
        bio_mean_str = f"{bio_mean:.3f}"
        # Adjust spacing based on number of digits before decimal point
        digits_before_decimal = len(str(int(bio_mean))) if bio_mean != -9.0 else 2
        bio_spacing = 10 - digits_before_decimal  # Base spacing minus adjustment for digits
        
        lines.append(f"   {day}      {cc_mean:.1f}    {cc_std:.1f}{' ' * bio_spacing}{bio_mean_str}     {bio_std:.1f}           {sw_mean:.1f}     {sw_std:.1f}")
    
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path