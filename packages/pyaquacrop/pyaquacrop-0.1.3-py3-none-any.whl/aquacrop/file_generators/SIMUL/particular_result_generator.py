"""
Particular Results settings generator for AquaCrop (ParticularResults.SIM)
"""

import os
from typing import List, Optional

def generate_particular_results_settings(
    file_path: str,
    output_types: Optional[List[int]] = None
) -> str:
    """
    Generate an AquaCrop particular results settings file (ParticularResults.SIM)
    
    Args:
        file_path: Path to write the file
        output_types: List of particular output types to enable:
            1: Biomass and Yield at Multiple cuttings (for herbaceous forage crops)
            2: Evaluation of simulation results (when Field Data)
            If None, both types will be enabled
    
    Returns:
        The path to the generated file
    """
    if output_types is None:
        output_types = [1, 2]
    
    # Map of output types to descriptions
    type_descriptions = {
        1: "Biomass and Yield at Multiple cuttings (for herbaceous forage crops)",
        2: "Evaluation of simulation results (when Field Data)"
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