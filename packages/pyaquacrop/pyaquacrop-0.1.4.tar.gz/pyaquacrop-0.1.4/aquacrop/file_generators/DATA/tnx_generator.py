"""
Temperature file generator for AquaCrop (.Tnx files)
"""

import os
from typing import List, Tuple

def generate_temperature_file(
    file_path: str,
    location: str,
    temperatures: List[Tuple[float, float]],  # List of (tmin, tmax) tuples
    record_type: int = 1,
    first_day: int = 1,
    first_month: int = 1,
    first_year: int = 2014
) -> str:
    
    """
    Generate an AquaCrop temperature file (.Tnx)
    
    Args:
        file_path: Path to write the file
        location: Location description
        temperatures: List of (tmin, tmax) tuples
        record_type: Record type (1=daily, 2=10-daily, 3=monthly)
        first_day: First day of record
        first_month: First month of record
        first_year: First year of record
    
    Returns:
        The path to the generated file
    """
    
    if record_type not in {1, 2, 3}:
        raise ValueError("record_type must be 1, 2, or 3")
    
    if first_day not in {1, 11, 21} and record_type == 2:
        raise ValueError("first_day must be 1, 11, or 21 for 10-day records")
    if first_day not in {1} and record_type == 3:
        raise ValueError("first_day must be 1 for monthly records")
   
    lines = [
        f"{location}",
        f"     {record_type}  : Daily records (1=daily, 2=10-daily and 3=monthly data)",
        f"     {first_day}  : First day of record (1, 11 or 21 for 10-day or 1 for months)",
        f"     {first_month}  : First month of record",
        f"  {first_year}  : First year of record (1901 if not linked to a specific year)",
        "",
        "  Tmin (C)   TMax (C)",
        "========================"
    ]
    
    for tmin, tmax in temperatures:
        lines.append(f"{tmin:.1f}\t{tmax:.1f}")
    
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path