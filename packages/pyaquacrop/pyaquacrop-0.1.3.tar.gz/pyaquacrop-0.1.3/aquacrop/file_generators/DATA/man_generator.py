"""
Management file generator for AquaCrop (.MAN files)
"""
import os
from typing import List, Optional, Dict
from aquacrop.constants import Constants

def generate_management_file(
    file_path: str,
    description: str,
   # Soil fertility
    fertility_stress: int = 50,
    
    # Mulches
    mulch_cover: int = 0,
    mulch_effect: int = 50,
    
    # Field surface conditions
    bund_height: float = 0.00,
    surface_runoff_affected: int = 0,
    runoff_adjustment: int = 0,
    
    # Weeds
    weed_cover_initial: int = 0,
    weed_cover_increase: int = 0,
    weed_shape_factor: float = 100.00,
    weed_replacement: int = 100,
    
    # Multiple cuttings
    multiple_cuttings: bool = False,
    canopy_after_cutting: int = 25,
    cgc_increase_after_cutting: int = 20,
    cutting_window_start_day: int = 1,
    cutting_window_length: int = -9,
    cutting_schedule_type: int = 0,
    cutting_time_criterion: int = 0,
    final_harvest_at_maturity: int = 0,
    day_nr_base: int = 41274,
    harvest_days: Optional[List[int]] = None,
) -> str:
    """
    Generate an AquaCrop management file (.MAN) with all possible parameters
    
    Args:
        file_path: Path to write the file
        description: Management description
        
        # Soil fertility
        fertility_stress: Degree of soil fertility stress (%, 0-100)
        
        # Mulches
        mulch_cover: Percentage of ground surface covered by mulches
        mulch_effect: Effect (%) of mulches on reduction of soil evaporation
        
        # Field surface conditions
        bund_height: Height (m) of soil bunds
        surface_runoff_affected: Whether surface runoff is affected by field practices (0=no, 1=yes)
        runoff_adjustment: Adjustment method for runoff (0=none, 1=method1, etc.)
        
        # Weeds
        weed_cover_initial: Relative cover of weeds at canopy closure (%)
        weed_cover_increase: Increase of relative cover of weeds in mid-season (+%)
        weed_shape_factor: Shape factor of the CC expansion function in weed-infested field
        weed_replacement: Replacement (%) by weeds of the self-thinned part of CC
        
        # Multiple cuttings
        multiple_cuttings: Whether multiple cuttings are considered (True/False)
        canopy_after_cutting: Canopy cover (%) after cutting
        cgc_increase_after_cutting: Increase (%) of CGC after cutting
        cutting_window_start_day: First day of window for multiple cuttings (1=start of growth cycle)
        cutting_window_length: Number of days in window for cuttings (-9=total growth cycle)
        cutting_schedule_type: Multiple cuttings schedule type (0=specified, 1=auto)
        cutting_time_criterion: Time criterion for cuttings (0=N/A, etc.)
        final_harvest_at_maturity: Whether final harvest at crop maturity is considered (0=no, 1=yes)
        day_nr_base: Day number for Day 1 of list of cuttings
        harvest_days: List of harvest days (for multiple cuttings)
        
        version: AquaCrop version
    
    Returns:
        The path to the generated file
    """
    # Initialize harvest_days if not provided
    if harvest_days is None:
        harvest_days = []
    
    # Generate management file content
    lines = [
        f"{description}",
        f"     {Constants.AQUACROP_VERSION_NUMBER}       : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
        f"     {mulch_cover}         : percentage (%) of ground surface covered by mulches IN growing period",
        f"    {mulch_effect}         : effect (%) of mulches on reduction of soil evaporation",
        f"    {fertility_stress}         : Degree of soil fertility stress (%) - Effect is crop specific",
        f"     {bund_height:.2f}      : height (m) of soil bunds",
        f"     {surface_runoff_affected}         : surface runoff {'IS' if surface_runoff_affected else 'NOT'} affected by field surface practices",
        f"     {runoff_adjustment}         : {'N/A (surface runoff is not affected or completely prevented)' if runoff_adjustment == 0 else 'surface runoff is affected by field practices'}",
        f"     {weed_cover_initial}         : relative cover of weeds at canopy closure (%)",
        f"     {weed_cover_increase}         : increase of relative cover of weeds in mid-season (+%)",
        f"   {weed_shape_factor:.2f}      : shape factor of the CC expansion function in a weed infested field",
        f"   {weed_replacement}         : replacement (%) by weeds of the self-thinned part of the CC - only for perennials"
    ]
    
    # Add multiple cutting information if enabled or harvest days provided
    # TODO: Fortran code requires all cutting parameters to be included even if not enabled
    # Add multiple cutting information regardless if enabled or not
    # Always include all cutting parameters - this is the key fix
    if multiple_cuttings or harvest_days:
        lines.extend([
            f"     1         : Multiple cuttings are considered",
            f"    {canopy_after_cutting}         : Canopy cover (%) after cutting",
            f"    {cgc_increase_after_cutting}         : Increase (%) of Canopy Growth Coefficient (CGC) after cutting",
            f"     {cutting_window_start_day}         : First day of window for multiple cuttings (1 = start of growth cycle)",
            f"    {cutting_window_length}         : Number of days in window for multiple cuttings (-9 = total growth cycle)",
            f"     {cutting_schedule_type}         : Multiple cuttings schedule is {'specified' if cutting_schedule_type == 0 else 'automatic'}",
            f"     {cutting_time_criterion}         : Time criterion: {'Not Applicable' if cutting_time_criterion == 0 else 'Specified'}",
            f"     {final_harvest_at_maturity}         : final harvest at crop maturity is {'considered' if final_harvest_at_maturity else 'not considered'}",
            f" {day_nr_base}         : dayNr for Day 1 of list of cuttings",
            "",
            " Harvest Day",
            "==============",
        ])
        
        # Add harvest days
        for day in harvest_days:
            lines.append(f"   {day}")
    else:
        # Even when cuttings are disabled, we must include ALL the cutting parameters
        lines.extend([
            f"     0         : Multiple cuttings are NOT considered",
            f"    {canopy_after_cutting}         : Canopy cover (%) after cutting",
            f"    {cgc_increase_after_cutting}         : Increase (%) of Canopy Growth Coefficient (CGC) after cutting",
            f"     {cutting_window_start_day}         : First day of window for multiple cuttings (1 = start of growth cycle)",
            f"    {cutting_window_length}         : Number of days in window for multiple cuttings (-9 = total growth cycle)",
            f"     {cutting_schedule_type}         : Multiple cuttings schedule is {'specified' if cutting_schedule_type == 0 else 'automatic'}",
            f"     {cutting_time_criterion}         : Time criterion: {'Not Applicable' if cutting_time_criterion == 0 else 'Specified'}",
            f"     {final_harvest_at_maturity}         : final harvest at crop maturity is {'considered' if final_harvest_at_maturity else 'not considered'}",
            f" {day_nr_base}         : dayNr for Day 1 of list of cuttings"
        ])
    
    # Write the content to file
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path