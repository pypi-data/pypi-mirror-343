import os
from typing import List, Optional, Dict, Union
from aquacrop.constants import Constants

def generate_irrigation_file(
    file_path: str,
    description: str,
    irrigation_method: int = 1,
    surface_wetted: int = 100,
    irrigation_mode: int = 1,
    
    # For mode 1: Specification of irrigation events
    reference_day: int = -9,  # -9 if reference day is onset of growing period
    irrigation_events: Optional[List[Dict[str, Union[int, float]]]] = None,
    
    # For mode 2: Generation of irrigation schedule
    time_criterion: int = 1,  # 1: Fixed interval, 2: Allowable depletion (mm), 3: % of RAW, 4: Min surface water
    depth_criterion: int = 1,  # 1: Back to Field Capacity, 2: Fixed application depth
    generation_rules: Optional[List[Dict[str, Union[int, float]]]] = None,
    
    # For mode 3: Determination of net irrigation requirement
    depletion_threshold: int = 50  # % RAW below which soil water may not drop
) -> str:
    """
    Generate an AquaCrop irrigation file (.IRR) with all possible parameters
    
    Args:
        file_path: Path to write the file
        description: Irrigation description
        
        # Basic irrigation parameters
        irrigation_method: Method code (1: Sprinkler, 2: Basin, 3: Border, 4: Furrow, 5: Drip)
        surface_wetted: Percentage of soil surface wetted by irrigation
        irrigation_mode: Mode code (1: Specification of events, 2: Generate schedule, 3: Determine requirements)
        
        # For mode 1: Specification of irrigation events
        reference_day: Day number of reference day (-9 if reference day is onset of growing period)
        irrigation_events: List of dicts with keys 'day', 'depth', 'ec' for each irrigation event
        
        # For mode 2: Generation of irrigation schedule
        time_criterion: Code for time criterion (1: Fixed interval, 2: Allowable depletion (mm), 
                        3: % of RAW, 4: Min surface water)
        depth_criterion: Code for depth criterion (1: Back to Field Capacity, 2: Fixed application depth)
        generation_rules: List of dicts with keys 'from_day', 'time_value', 'depth_value', 'ec'
        
        # For mode 3: Determination of net irrigation requirement
        depletion_threshold: % RAW below which soil water may not drop
    
    Returns:
        The path to the generated file
    """
    # Initialize lists if not provided
    if irrigation_events is None:
        irrigation_events = []
    
    if generation_rules is None:
        generation_rules = []
    
    # Generate irrigation file content
    lines = [
        f"{description}",
        f" {Constants.AQUACROP_VERSION_NUMBER} : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
        f" {irrigation_method} : {_get_irrigation_method_description(irrigation_method)}",
        f"{surface_wetted} : Percentage of soil surface wetted by irrigation",
        f" {irrigation_mode} : {_get_irrigation_mode_description(irrigation_mode)}",
    ]
    
    # Add mode-specific content
    if irrigation_mode == 1:  # Specification of irrigation events
        lines.extend([
            f" {reference_day} : Reference DayNr for Day 1 {_get_reference_day_description(reference_day)}",
            f" Day Depth (mm) ECw (dS/m)",
            f"====================================",
        ])
        
        # Add irrigation events
        for event in irrigation_events:
            lines.append(f" {event['day']} {event['depth']} {event['ec']:.1f}")
            
    elif irrigation_mode == 2:  # Generation of irrigation schedule
        lines.extend([
            f" {time_criterion} : {_get_time_criterion_description(time_criterion)}",
            f" {depth_criterion} : {_get_depth_criterion_description(depth_criterion)}",
            f"",
            f" From day {_get_time_criterion_column_name(time_criterion)} {_get_depth_criterion_column_name(depth_criterion)} ECw (dS/m)",
            f"=========================================================================",
        ])
        
        # Add generation rules
        for rule in generation_rules:
            lines.append(f" {rule['from_day']} {rule['time_value']} {rule['depth_value']} {rule['ec']:.1f}")
            
    elif irrigation_mode == 3:  # Determination of net irrigation requirement
        lines.extend([
            f" {depletion_threshold} : Threshold for irrigation (% of RAW)",
        ])
    
    # Write the content to file
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path

def _get_irrigation_method_description(method_code: int) -> str:
    """Get the description for irrigation method code"""
    methods = {
        1: "Sprinkler irrigation",
        2: "Surface irrigation: Basin",
        3: "Surface irrigation: Border",
        4: "Surface irrigation: Furrow",
        5: "Drip irrigation"
    }
    return methods.get(method_code, "Unknown irrigation method")

def _get_irrigation_mode_description(mode_code: int) -> str:
    """Get the description for irrigation mode code"""
    modes = {
        1: "Specification of irrigation events",
        2: "Generate irrigation schedule",
        3: "Determination of net irrigation water requirement"
    }
    return modes.get(mode_code, "Unknown irrigation mode")

def _get_reference_day_description(ref_day: int) -> str:
    """Get description for reference day"""
    if ref_day == -9:
        return "(= onset of growing period)"
    else:
        return f"(= {ref_day})"

def _get_time_criterion_description(criterion_code: int) -> str:
    """Get the description for time criterion code"""
    criteria = {
        1: "Time criterion = fixed intervals",
        2: "Time criterion = allowable depletion (mm water)",
        3: "Time criterion = allowable depletion (% of RAW)",
        4: "Time criterion = keep minimum level of surface water layer"
    }
    return criteria.get(criterion_code, "Unknown time criterion")

def _get_depth_criterion_description(criterion_code: int) -> str:
    """Get the description for depth criterion code"""
    criteria = {
        1: "Depth criterion = back to Field Capacity",
        2: "Depth criterion = fixed application depth"
    }
    return criteria.get(criterion_code, "Unknown depth criterion")

def _get_time_criterion_column_name(criterion_code: int) -> str:
    """Get column name for time criterion"""
    columns = {
        1: "Interval (days)",
        2: "Depletion (mm)",
        3: "Depletion (% RAW)",
        4: "Min. depth (mm)"
    }
    return columns.get(criterion_code, "Value")

def _get_depth_criterion_column_name(criterion_code: int) -> str:
    """Get column name for depth criterion"""
    columns = {
        1: "Back to FC +/- (mm)",
        2: "Application depth (mm)"
    }
    return columns.get(criterion_code, "Value")

