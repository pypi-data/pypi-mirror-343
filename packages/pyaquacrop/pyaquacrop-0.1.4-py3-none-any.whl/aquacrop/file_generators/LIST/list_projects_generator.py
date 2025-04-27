"""
CO2 file generator for AquaCrop (.CO2 files)
"""

import os
from typing import List, Dict, Tuple

def generate_co2_file(
    file_path: str,
    description: str,
    co2_records: List[Tuple[int, float]]  # List of (year, CO2 concentration) tuples
) -> str:
    """
    Generate an AquaCrop CO2 file (.CO2)
    
    Args:
        file_path: Path to write the file
        description: Description for the CO2 file
        co2_records: List of tuples (year, CO2 concentration in ppm)
    
    Returns:
        The path to the generated file
    """
    lines = [
        f"{description}",
        f"Year     CO2 (ppm by volume)",
        "============================"
    ]
    
    # Sort records by year
    sorted_records = sorted(co2_records, key=lambda x: x[0])
    
    for year, co2 in sorted_records:
        lines.append(f"  {year}  {co2:.2f}")
    
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path

