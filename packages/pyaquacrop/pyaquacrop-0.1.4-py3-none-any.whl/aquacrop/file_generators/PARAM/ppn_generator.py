"""
Parameter file generator for AquaCrop (.PP1 and .PPn files)
"""

import os
from typing import Dict, Optional

def generate_parameter_file(
    file_path: str,
    params: Optional[Dict] = None
) -> str:
    """
    Generate an AquaCrop parameter file (.PP1 or .PPn)
    
    Args:
        file_path: Path to write the file
        params: Dictionary of parameters (if None, defaults will be used):
            - evaporation_decline_factor: Evaporation decline factor for stage II
            - kex: Soil evaporation coefficient for fully wet and non-shaded soil surface
            - cc_threshold_for_hi: Threshold for green CC below which HI can no longer increase (% cover)
            - root_expansion_start_depth: Starting depth of root zone expansion curve (% of Zmin)
            - max_root_expansion: Maximum allowable root zone expansion (fixed at 5 cm/day)
            - shape_root_water_stress: Shape factor for effect water stress on root zone expansion
            - germination_soil_water: Required soil water content in top soil for germination (% TAW)
            - fao_adjustment_factor: Adjustment factor for FAO-adjustment soil water depletion
            - aeration_days: Number of days after which deficient aeration is fully effective
            - senescence_factor: Exponent of senescence factor
            - senescence_reduction: Decrease of p(sen) once early canopy senescence is triggered
            - top_soil_thickness: Thickness top soil (cm) for soil water depletion
            - evaporation_depth: Depth (cm) of soil profile affected by soil evaporation
            - cn_depth: Depth (m) of soil profile for CN adjustment
            - cn_adjustment: Whether CN is adjusted to Antecedent Moisture Class
            - salt_diffusion_factor: Salt diffusion factor (%)
            - salt_solubility: Salt solubility (g/liter)
            - soil_water_gradient_factor: Shape factor for effect of soil water content gradient
            - default_min_temp: Default minimum temperature if no temperature file is specified
            - default_max_temp: Default maximum temperature if no temperature file is specified
            - gdd_method: Default method for the calculation of growing degree days
            - rainfall_estimation: Whether daily rainfall is estimated by USDA-SCS procedure
            - effective_rainfall_pct: Percentage of effective rainfall
            - showers_per_decade: Number of showers in a decade for run-off estimate
            - soil_evaporation_reduction: Parameter for reduction of soil evaporation
    
    Returns:
        The path to the generated file
    """
    # Default parameters
    default_params = {
        'evaporation_decline_factor': 4,
        'kex': 1.10,
        'cc_threshold_for_hi': 5,
        'root_expansion_start_depth': 70,
        'max_root_expansion': 5.00,
        'shape_root_water_stress': -6,
        'germination_soil_water': 20,
        'fao_adjustment_factor': 1.0,
        'aeration_days': 3,
        'senescence_factor': 1.00,
        'senescence_reduction': 12,
        'top_soil_thickness': 10,
        'evaporation_depth': 30,
        'cn_depth': 0.30,
        'cn_adjustment': 1,
        'salt_diffusion_factor': 20,
        'salt_solubility': 100,
        'soil_water_gradient_factor': 16,
        'default_min_temp': 12.0,
        'default_max_temp': 28.0,
        'gdd_method': 3,
        'rainfall_estimation': 1,
        'effective_rainfall_pct': 70,
        'showers_per_decade': 2,
        'soil_evaporation_reduction': 5
    }
    
    # Update with provided parameters (if any)
    if params:
        default_params.update(params)
    
    # Use short variable name for better readability
    p = default_params
    
    lines = [
        f"      {p['evaporation_decline_factor']}         : Evaporation decline factor for stage II",
        f"      {p['kex']:.2f}      : Ke(x) Soil evaporation coefficient for fully wet and non-shaded soil surface",
        f"      {p['cc_threshold_for_hi']}         : Threshold for green CC below which HI can no longer increase (% cover)",
        f"     {p['root_expansion_start_depth']}         : Starting depth of root zone expansion curve (% of Zmin)",
        f"      {p['max_root_expansion']:.2f}      : Maximum allowable root zone expansion (fixed at 5 cm/day)",
        f"     {p['shape_root_water_stress']}         : Shape factor for effect water stress on root zone expansion",
        f"     {p['germination_soil_water']}         : Required soil water content in top soil for germination (% TAW)",
        f"      {p['fao_adjustment_factor']:.1f}       : Adjustment factor for FAO-adjustment soil water depletion (p) by ETo",
        f"      {p['aeration_days']}         : Number of days after which deficient aeration is fully effective",
        f"      {p['senescence_factor']:.2f}      : Exponent of senescence factor adjusting drop in photosynthetic activity of dying crop",
        f"     {p['senescence_reduction']}         : Decrease of p(sen) once early canopy senescence is triggered (% of p(sen))",
        f"     {p['top_soil_thickness']}         : Thickness top soil (cm) in which soil water depletion has to be determined",
        f"     {p['evaporation_depth']}         : Depth [cm] of soil profile affected by water extraction by soil evaporation",
        f"      {p['cn_depth']:.2f}      : Considered depth (m) of soil profile for calculation of mean soil water content for CN adjustment",
        f"      {p['cn_adjustment']}         : CN is adjusted to Antecedent Moisture Class",
        f"     {p['salt_diffusion_factor']}         : Salt diffusion factor (capacity for salt diffusion in micro pores) [%]",
        f"    {p['salt_solubility']}         : Salt solubility [g/liter]",
        f"     {p['soil_water_gradient_factor']}         : Shape factor for effect of soil water content gradient on capillary rise",
        f"     {p['default_min_temp']:.1f}       : Default minimum temperature (degC) if no temperature file is specified",
        f"     {p['default_max_temp']:.1f}       : Default maximum temperature (degC) if no temperature file is specified",
        f"      {p['gdd_method']}         : Default method for the calculation of growing degree days",
        f"      {p['rainfall_estimation']}         : Daily rainfall is estimated by USDA-SCS procedure (when input is 10-day/monthly rainfall)",
        f"     {p['effective_rainfall_pct']}         : Percentage of effective rainfall (when input is 10-day/monthly rainfall)",
        f"      {p['showers_per_decade']}         : Number of showers in a decade for run-off estimate (when input is 10-day/monthly rainfall)",
        f"      {p['soil_evaporation_reduction']}         : Parameter for reduction of soil evaporation (when input is 10-day/monthly rainfall)"
    ]
    
    content = "\n".join(lines)
    
    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(content)
    
    return file_path