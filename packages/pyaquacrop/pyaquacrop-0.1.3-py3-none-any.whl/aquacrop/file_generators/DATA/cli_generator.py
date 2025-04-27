"""
Climate file generator for AquaCrop (.CLI files)
"""

import os
from aquacrop.constants import Constants

def generate_climate_file(
    file_path: str,
    location: str,
    tnx_file: str,
    eto_file: str,
    plu_file: str,
    co2_file: str,
) -> str:
    """
    Generate an AquaCrop climate file (.CLI)
    
    Args:
        file_path: Path to write the file
        location: Location description
        tnx_file: Temperature file name
        eto_file: Reference ET file name
        plu_file: Rainfall file name
        co2_file: CO2 file name
        version: AquaCrop version
    
    Returns:
        The path to the generated file
    """
    lines = [
        f"{location}",
        f" {Constants.AQUACROP_VERSION_NUMBER}   : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
        f"{tnx_file}",
        f"{eto_file}",
        f"{plu_file}",
        f"{co2_file}"
    ]
    
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path