"""
CO2 file generator for AquaCrop (.CO2 files)
"""

import os
from typing import List, Dict, Tuple, Optional

def generate_co2_file(
    file_path: str,
    description: str = "Default atmospheric CO2 concentration",
    records: Optional[List[Tuple[int, float]]] = None
) -> str:
    """
    Generate an AquaCrop CO2 file (.CO2)
    
    Args:
        file_path: Path to write the file
        description: Description of the CO2 file
        records: List of tuples (year, co2_ppm) or None for default values
    
    Returns:
        The path to the generated file
    """
    # Default Mauna Loa CO2 records if none provided
    if records is None:
        records = [
            (1902, 297.4),
            (1910, 300.0),
            (1920, 303.0),
            (1930, 306.0),
            (1940, 310.5),
            (1950, 311.0),
            (1960, 316.91),
            (1970, 325.68),
            (1980, 338.76),
            (1990, 354.45),
            (2000, 369.71),
            (2010, 390.1),
            (2015, 401.02),
            (2020, 414.21),
            (2023, 421.08),
            (2030, 430.0),  # Projected values
            (2050, 470.0),
            (2100, 570.0)
        ]
    
    lines = [
        f"{description}",
        f"Year     CO2 (ppm by volume)",
        f"============================"
    ]
    
    # Sort by year to ensure chronological order
    sorted_records = sorted(records, key=lambda x: x[0])
    
    for year, co2 in sorted_records:
        lines.append(f"  {year}  {co2:.2f}")
    
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path