"""
Project file generator for AquaCrop (.PRM and .PRO files)
"""

import os
from typing import Dict, List, Optional
from aquacrop.utils.julianDayConverter import convertJulianToDateString
from aquacrop.constants import Constants
def generate_project_file(
    file_path: str,
    description: str,
    periods: List[Dict],
) -> str:
    """
    Generate an AquaCrop project file (.PRM or .PRO)
    
    Args:
        file_path: Path to write the file
        description: Project description
        periods: List of simulation periods, each containing:
            - year: Year number (1, 2, etc.)
            - first_day_sim: First day of simulation (Julian day)
            - last_day_sim: Last day of simulation (Julian day)
            - first_day_crop: First day of crop cycle (Julian day)
            - last_day_crop: Last day of crop cycle (Julian day)
            - is_seeding_year: Whether this is a seeding year (True) or not (False)
            - cli_file: Climate file name
            - tnx_file: Temperature file name
            - eto_file: ETo file name
            - plu_file: Rainfall file name
            - co2_file: CO2 file name
            - cal_file: Calendar file name
            - cro_file: Crop file name
            - irr_file: Irrigation file name
            - man_file: Management file name
            - sol_file: Soil file name
            - gwt_file: Groundwater file name
            - sw0_file: Initial conditions file name
            - off_file: Off-season file name
            - obs_file: Observations file name
        version: AquaCrop version
    
    Returns:
        The path to the generated file
    """
    
    lines = [description]
    lines.append(f"      {Constants.AQUACROP_VERSION_NUMBER}       : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})")
    
    for period in periods:
        year = period['year']
        is_seeding_year = period.get('is_seeding_year', True)
        
        first_day_sim = period['first_day_sim']
        last_day_sim = period['last_day_sim']
        first_day_crop = period['first_day_crop']
        last_day_crop = period['last_day_crop']
        
        # Date conversions for readable format in the file
        first_date_sim_str = convertJulianToDateString(first_day_sim)
        last_date_sim_str = convertJulianToDateString(last_day_sim)
        first_date_crop_str = convertJulianToDateString(first_day_crop)
        last_date_crop_str = convertJulianToDateString(last_day_crop)
        
        lines.append(f"      {year}         : Year number of cultivation ({'Seeding' if is_seeding_year else 'Non-seeding'}/planting year)")
        lines.append(f"  {first_day_sim}         : First day of simulation period - {first_date_sim_str}")
        lines.append(f"  {last_day_sim}         : Last day of simulation period - {last_date_sim_str}")
        lines.append(f"  {first_day_crop}         : First day of cropping period - {first_date_crop_str}")
        lines.append(f"  {last_day_crop}         : Last day of cropping period - {last_date_crop_str}")
        
        # Define path strings
        data_path = "'./DATA/'"
        simul_path = "'./SIMUL/'"
        obs_path = "'./OBS/'"
        none_str = "(None)"
        
        # Add file references
        lines.append("-- 1. Climate (CLI) file")
        lines.append(f"   {period.get('cli_file', none_str)}")
        lines.append(f"   {data_path if period.get('cli_file') else none_str}")
        
        lines.append("   1.1 Temperature (Tnx or TMP) file")
        lines.append(f"   {period.get('tnx_file', none_str)}")
        lines.append(f"   {data_path if period.get('tnx_file') else none_str}")
        
        lines.append("   1.2 Reference ET (ETo) file")
        lines.append(f"   {period.get('eto_file', none_str)}")
        lines.append(f"   {data_path if period.get('eto_file') else none_str}")
        
        lines.append("   1.3 Rain (PLU) file")
        lines.append(f"   {period.get('plu_file', none_str)}")
        lines.append(f"   {data_path if period.get('plu_file') else none_str}")
        
        # TODO: This is a fortran bug, we need to call the file MaunaLoa.CO2
        lines.append("   1.4 Atmospheric CO2 concentration (CO2) file")
        lines.append("   MaunaLoa.CO2")
        lines.append("   './SIMUL/'")
        
        lines.append("-- 2. Calendar (CAL) file")
        lines.append(f"   {period.get('cal_file', none_str)}")
        lines.append(f"   {data_path if period.get('cal_file') else none_str}")
        
        lines.append("-- 3. Crop (CRO) file")
        lines.append(f"   {period.get('cro_file', none_str)}")
        lines.append(f"   {data_path if period.get('cro_file') else none_str}")
        
        lines.append("-- 4. Irrigation management (IRR) file")
        lines.append(f"   {period.get('irr_file', none_str)}")
        lines.append(f"   {data_path if period.get('irr_file') and period.get('irr_file') != none_str else none_str}")
        
        lines.append("-- 5. Field management (MAN) file")
        lines.append(f"   {period.get('man_file', none_str)}")
        lines.append(f"   {data_path if period.get('man_file') else none_str}")
        
        lines.append("-- 6. Soil profile (SOL) file")
        lines.append(f"   {period.get('sol_file', none_str)}")
        lines.append(f"   {data_path if period.get('sol_file') else none_str}")
        
        lines.append("-- 7. Groundwater table (GWT) file")
        lines.append(f"   {period.get('gwt_file', none_str)}")
        lines.append(f"   {data_path if period.get('gwt_file') and period.get('gwt_file') != none_str else none_str}")
        
        lines.append("-- 8. Initial conditions (SW0) file")
        init_cond = period.get('sw0_file', none_str)
        if year > 1 and (not init_cond or init_cond == none_str or init_cond == "(None)"):
            init_cond = "KeepSWC"
            init_desc = "Keep soil water profile of previous run"
        elif init_cond == "KeepSWC":
            init_desc = "Keep soil water profile of previous run"
        else:
            init_desc = none_str if not init_cond or init_cond in [none_str, "(None)"] else data_path
        lines.append(f"   {init_cond}")
        lines.append(f"   {init_desc}")
        
        lines.append("-- 9. Off-season conditions (OFF) file")
        lines.append(f"   {period.get('off_file', none_str)}")
        lines.append(f"   {data_path if period.get('off_file') and period.get('off_file') != none_str else none_str}")
        
        lines.append("-- 10. Field data (OBS) file")
        lines.append(f"   {period.get('obs_file', none_str)}")
        lines.append(f"   {obs_path if period.get('obs_file') and period.get('obs_file') != none_str else none_str}")
    
    # Write the file
    content = "\n".join(lines)
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path