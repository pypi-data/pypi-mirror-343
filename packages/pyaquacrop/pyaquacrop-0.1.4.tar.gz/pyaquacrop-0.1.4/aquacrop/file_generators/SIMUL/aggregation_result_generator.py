"""
Aggregation Results settings generator for AquaCrop (AggregationResults.SIM)
"""

import os

def generate_aggregation_results_settings(
    file_path: str,
    aggregation_level: int = 0
) -> str:
    """
    Generate an AquaCrop aggregation results settings file (AggregationResults.SIM)
    
    Args:
        file_path: Path to write the file
        aggregation_level: Aggregation level for intermediate results:
            0: None (default)
            1: Daily
            2: 10-daily
            3: Monthly
    
    Returns:
        The path to the generated file
    """
    # Validate aggregation level
    if aggregation_level not in [0, 1, 2, 3]:
        aggregation_level = 0
    
    # Define aggregation level descriptions
    level_descriptions = {
        0: "none",
        1: "daily",
        2: "10-daily",
        3: "monthly"
    }
    
    content = f" {aggregation_level} : Time aggregation for intermediate results (0 = {level_descriptions[0]} ; 1 = {level_descriptions[1]}; 2 = {level_descriptions[2]}; 3 = {level_descriptions[3]})"
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path