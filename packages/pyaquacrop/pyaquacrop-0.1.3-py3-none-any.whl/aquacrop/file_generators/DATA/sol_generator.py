"""
Soil file generator for AquaCrop (.SOL files)
"""

import os
from typing import List, Dict
from aquacrop.constants import Constants

def generate_soil_file(
    file_path: str,
    description: str,
    horizons: List[Dict],
    curve_number: int = 61,
    readily_evaporable_water: int = 9,

) -> str:
    """
    Generate an AquaCrop soil file (.SOL)
    
    Args:
        file_path: Path to write the file
        description: Soil description
        horizons: List of soil horizons, each containing:
            - thickness: Thickness of horizon (m)
            - sat: Saturation point (vol %)
            - fc: Field capacity (vol %)
            - wp: Wilting point (vol %)
            - ksat: Saturated hydraulic conductivity (mm/day)
            - penetrability: Root penetrability (%, default 100)
            - gravel: Gravel content (%, default 0)
            - cra: Soil hydraulic parameter a
            - crb: Soil hydraulic parameter b
            - description: Horizon description
        curve_number: Curve number for runoff (CN)
        readily_evaporable_water: Readily evaporable water from top layer (mm)
        version: AquaCrop version
    
    Returns:
        The path to the generated file
    """
    lines = [
        f"{description}",
        f"        {Constants.AQUACROP_VERSION_NUMBER}                 : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
        f"       {curve_number}                   : CN (Curve Number)",
        f"        {readily_evaporable_water}                   : Readily evaporable water from top layer (mm)",
        f"        {len(horizons)}                   : number of soil horizons",
        f"       -9                   : variable no longer applicable",
        f"  Thickness  Sat   FC    WP     Ksat   Penetrability  Gravel  CRa       CRb           description",
        f"  ---(m)-   ----(vol %)-----  (mm/day)      (%)        (%)    -----------------------------------------"
    ]
    
    for h in horizons:
        thickness = h['thickness']
        sat = h['sat']
        fc = h['fc']
        wp = h['wp']
        ksat = h['ksat']
        penetrability = h.get('penetrability', 100)
        gravel = h.get('gravel', 0)
        cra = h.get('cra', -0.3906)
        crb = h.get('crb', 1.2556)
        description = h.get('description', 'soil horizon')
        
        lines.append(f"    {thickness:.2f}    {sat:.1f}  {fc:.1f}  {wp:.1f}  {ksat:.1f}        {penetrability}         {gravel}     {cra:.6f}  {crb:.6f}   {description}               ")
    
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path