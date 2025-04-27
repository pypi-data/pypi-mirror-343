"""
Crop file generator for AquaCrop (.CRO files) with parameter validation
"""

import os
from typing import Dict, Optional, List, Set, Any
from aquacrop.constants import Constants

def validate_crop_parameters(params: Dict) -> List[str]:
    """
    Validate that all required parameters for crop file generation are present.
    
    Args:
        params: Dictionary of provided crop parameters
    
    Returns:
        List of missing parameter names (empty if all required parameters are present)
    """
    # Complete list of all required parameters for crop file generation
    required_params = {
        # Basic crop classification
        'crop_type', 'is_sown', 'cycle_determination', 'adjust_for_eto',
        
        # Temperature parameters
        'base_temp', 'upper_temp', 'gdd_cycle_length', 
        
        # Crop water stress parameters
        'p_upper_canopy', 'p_lower_canopy', 'shape_canopy', 'p_upper_stomata', 
        'shape_stomata', 'p_upper_senescence', 'shape_senescence', 'dormancy_eto_threshold',
        'p_upper_pollination', 'aeration_stress_threshold',
        
        # Soil fertility stress parameters
        'fertility_stress_calibration', 'shape_fertility_canopy_expansion',
        'shape_fertility_max_canopy', 'shape_fertility_water_productivity',
        'shape_fertility_decline',
        
        # Temperature stress parameters
        'cold_stress_for_pollination', 'heat_stress_for_pollination',
        'minimum_growing_degrees_pollination',
        
        # Salinity stress parameters
        'salinity_threshold_ece', 'salinity_max_ece', 'salinity_shape_factor',
        'salinity_stress_cc', 'salinity_stress_stomata',
        
        # Transpiration parameters
        'kc_max', 'kc_decline',
        
        # Rooting parameters
        'min_rooting_depth', 'max_rooting_depth', 'root_expansion_shape',
        'max_water_extraction_top', 'max_water_extraction_bottom',
        'soil_evaporation_reduction',
        
        # Canopy development parameters
        'canopy_cover_per_seedling', 'canopy_regrowth_size', 'plant_density',
        'canopy_growth_coefficient', 'canopy_thinning_years', 'canopy_thinning_shape',
        'max_canopy_cover', 'canopy_decline_coefficient',
        
        # Crop cycle parameters (Calendar days)
        'days_emergence', 'days_max_rooting', 'days_senescence',
        'days_maturity', 'days_flowering', 'days_flowering_length',
        'days_crop_determinancy', 'days_hi_start',
        
        # Crop cycle parameters (Growing degree days)
        'gdd_emergence', 'gdd_max_rooting', 'gdd_senescence',
        'gdd_maturity', 'gdd_flowering', 'gdd_flowering_length',
        'cgc_gdd', 'cdc_gdd', 'gdd_hi_start',
        
        # Biomass and yield parameters
        'water_productivity', 'water_productivity_yield_formation',
        'co2_response_strength', 'harvest_index', 'water_stress_hi_increase',
        'veg_growth_impact_hi', 'stomatal_closure_impact_hi',
        'max_hi_increase', 'dry_matter_content',
        
        # Perennial crop parameters
        'is_perennial', 'first_year_min_rooting', 'assimilate_transfer',
        'assimilate_storage_days', 'assimilate_transfer_percent',
        'root_to_shoot_transfer_percent',
        
        # Crop calendar for perennials
        'restart_type', 'restart_window_day', 'restart_window_month',
        'restart_window_length', 'restart_gdd_threshold', 'restart_days_required',
        'restart_occurrences', 'end_type', 'end_window_day', 'end_window_month',
        'end_window_years_offset', 'end_window_length', 'end_gdd_threshold',
        'end_days_required', 'end_occurrences'
    }
    
    # Find missing parameters
    missing_params = [param for param in required_params if param not in params]
    
    return missing_params

def generate_crop_file(
    file_path: str,
    description: str,
    params: Dict,
    strict_validation: bool = True
) -> str:
    """
    Generate an AquaCrop crop file (.CRO) with all possible crop parameters
    
    Args:
        file_path: Path to write the file
        description: Crop description
        params: Dictionary of crop parameters
        strict_validation: If True, raise an error if any required parameters are missing.
                           If False, print a warning but continue.
    
    Returns:
        The path to the generated file
        
    Raises:
        ValueError: If any required parameters are missing (only when strict_validation=True)
    """
    # Validate that all required parameters are present
    missing_params = validate_crop_parameters(params)
    
    if missing_params:
        error_message = f"Missing required crop parameters: {', '.join(missing_params)}"
        if strict_validation:
            raise ValueError(error_message)
        else:
            print(f"WARNING: {error_message}")
            print("File generation may fail or produce incorrect results.")
    
    is_protected = 1  # File not protected
    
    try:
        lines = [
            f"{description}",
            f"     {Constants.AQUACROP_VERSION_NUMBER}       : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
            f"     {is_protected}         : File not protected",
            f"     {params['crop_type']}         : {'forage crop' if params['crop_type'] == 4 else 'fruit/grain producing crop'}",
            f"     {1 if params['is_sown'] else 0}         : Crop is {'sown' if params['is_sown'] else 'transplanted'}",
            f"     {params['cycle_determination']}         : Determination of crop cycle : by {'growing degree-days' if params['cycle_determination'] else 'calendar days'}",
            f"     {1 if params['adjust_for_eto'] else 0}         : Soil water depletion factors (p) {'are' if params['adjust_for_eto'] else 'are not'} adjusted by ETo",
            f"     {params['base_temp']:.1f}       : Base temperature (degC) below which crop development does not progress",
            f"    {params['upper_temp']:.1f}       : Upper temperature (degC) above which crop development no longer increases with an increase in temperature",
            f"  {params['gdd_cycle_length']}         : Total length of crop cycle in growing degree-days",
            f"     {params['p_upper_canopy']:.2f}      : Soil water depletion factor for canopy expansion (p-exp) - Upper threshold",
            f"     {params['p_lower_canopy']:.2f}      : Soil water depletion factor for canopy expansion (p-exp) - Lower threshold",
            f"     {params['shape_canopy']:.1f}       : Shape factor for water stress coefficient for canopy expansion (0.0 = straight line)",
            f"     {params['p_upper_stomata']:.2f}      : Soil water depletion fraction for stomatal control (p - sto) - Upper threshold",
            f"     {params['shape_stomata']:.1f}       : Shape factor for water stress coefficient for stomatal control (0.0 = straight line)",
            f"     {params['p_upper_senescence']:.2f}      : Soil water depletion factor for canopy senescence (p - sen) - Upper threshold",
            f"     {params['shape_senescence']:.1f}       : Shape factor for water stress coefficient for canopy senescence (0.0 = straight line)",
            f"   {params['dormancy_eto_threshold']}         : Sum(ETo) during dormant period to be exceeded before crop is permanently wilted",
            f"     {params['p_upper_pollination']:.2f}      : Soil water depletion factor for pollination (p - pol) - Upper threshold",
            f"     {params['aeration_stress_threshold']}         : Vol% for Anaerobiotic point (* (SAT - [vol%]) at which deficient aeration occurs *)"
        ]
        
        # Add remaining crop parameters with values from the parameters dictionary
        lines.extend([
            f"    {params['fertility_stress_calibration']}         : Considered soil fertility stress for calibration of stress response (%)",
            f"     {params['shape_fertility_canopy_expansion']:.2f}      : Shape factor for the response of canopy expansion to soil fertility stress",
            f"     {params['shape_fertility_max_canopy']:.2f}      : Shape factor for the response of maximum canopy cover to soil fertility stress",
            f"    {params['shape_fertility_water_productivity']:.2f}      : Shape factor for the response of crop Water Productivity to soil fertility stress",
            f"     {params['shape_fertility_decline']:.2f}      : Shape factor for the response of decline of canopy cover to soil fertility stress",
            f"    -9         : dummy - Parameter no Longer required",
            f"     {params['cold_stress_for_pollination']}         : Minimum air temperature below which pollination starts to fail (cold stress) (degC)",
            f"    {params['heat_stress_for_pollination']}         : Maximum air temperature above which pollination starts to fail (heat stress) (degC)",
            f"     {params['minimum_growing_degrees_pollination']:.1f}       : Minimum growing degrees required for full crop transpiration (degC - day)",
            f"     {params['salinity_threshold_ece']}         : Electrical Conductivity of soil saturation extract at which crop starts to be affected by soil salinity (dS/m)",
            f"    {params['salinity_max_ece']}         : Electrical Conductivity of soil saturation extract at which crop can no longer grow (dS/m)",
            f"    {params['salinity_shape_factor']}         : Dummy - no longer applicable",
            f"    {params['salinity_stress_cc']}         : Calibrated distortion (%) of CC due to salinity stress (Range: 0 (none) to +100 (very strong))",
            f"   {params['salinity_stress_stomata']}         : Calibrated response (%) of stomata stress to ECsw (Range: 0 (none) to +200 (extreme))",
            f"     {params['kc_max']:.2f}      : Crop coefficient when canopy is complete but prior to senescence (KcTr,x)",
            f"     {params['kc_decline']:.3f}     : Decline of crop coefficient (%/day) as a result of ageing, nitrogen deficiency, etc.",
            f"     {params['min_rooting_depth']:.2f}      : Minimum effective rooting depth (m)",
            f"     {params['max_rooting_depth']:.2f}      : Maximum effective rooting depth (m)",
            f"    {params['root_expansion_shape']}         : Shape factor describing root zone expansion",
            f"     {params['max_water_extraction_top']:.3f}     : Maximum root water extraction (m3water/m3soil.day) in top quarter of root zone",
            f"     {params['max_water_extraction_bottom']:.3f}     : Maximum root water extraction (m3water/m3soil.day) in bottom quarter of root zone",
            f"    {params['soil_evaporation_reduction']}         : Effect of canopy cover in reducing soil evaporation in late season stage",
            f"     {params['canopy_cover_per_seedling']:.2f}      : Soil surface covered by an individual seedling at 90 % emergence (cm2)",
            f"    {params['canopy_regrowth_size']:.2f}      : Canopy size of individual plant (re-growth) at 1st day (cm2)",
            f"  {params['plant_density']}      : Number of plants per hectare",
            f"     {params['canopy_growth_coefficient']:.5f}   : Canopy growth coefficient (CGC): Increase in canopy cover (fraction soil cover per day)",
            f"     {params['canopy_thinning_years']}         : Number of years at which CCx declines to 90 % of its value due to self-thinning - for Perennials",
            f"     {params['canopy_thinning_shape']:.2f}      : Shape factor of the decline of CCx over the years due to self-thinning - for Perennials",
            f"    -9         : dummy - Parameter no Longer required",
            f"     {params['max_canopy_cover']:.2f}      : Maximum canopy cover (CCx) in fraction soil cover",
            f"     {params['canopy_decline_coefficient']:.5f}   : Canopy decline coefficient (CDC): Decrease in canopy cover (in fraction per day)",
            f"     {params['days_emergence']}         : Calendar Days: from sowing to emergence",
            f"   {params['days_max_rooting']}         : Calendar Days: from sowing to maximum rooting depth",
            f"   {params['days_senescence']}         : Calendar Days: from sowing to start senescence",
            f"   {params['days_maturity']}         : Calendar Days: from sowing to maturity (length of crop cycle)",
            f"     {params['days_flowering']}         : Calendar Days: from sowing to flowering",
            f"     {params['days_flowering_length']}         : Length of the flowering stage (days)",
            f"     {params['days_crop_determinancy']}         : Crop determinancy {'linked with flowering' if params['days_crop_determinancy'] == 1 else 'unlinked with flowering'}",
            f"    -9         : parameter NO LONGER required",
            f"    {params['days_hi_start']}         : Building up of Harvest Index starting at sowing/transplanting (days)",
            f"    {params['water_productivity']:.1f}       : Water Productivity normalized for ETo and CO2 (WP*) (gram/m2)",
            f"   {params['water_productivity_yield_formation']}         : Water Productivity normalized for ETo and CO2 during yield formation (as % WP*)",
            f"    {params['co2_response_strength']}         : Sink strength (%) quatifying biomass response to elevated atmospheric CO2 concentration",
            f"   {params['harvest_index']*100:.0f}         : Reference Harvest Index (HIo) (%)",
            f"    {params['water_stress_hi_increase']}         : Possible increase (%) of HI due to water stress before flowering",
            f"    {params['veg_growth_impact_hi']:.1f}       : {'No impact on' if params['veg_growth_impact_hi'] < 0 else 'Impact of'} HI of restricted vegetative growth during yield formation ",
            f"    {params['stomatal_closure_impact_hi']:.1f}       : {'No effect on' if params['stomatal_closure_impact_hi'] < 0 else 'Effect of'} HI of stomatal closure during yield formation",
            f"    {params['max_hi_increase']}         : Allowable maximum increase (%) of specified HI",
            f"     {params['gdd_emergence']}         : GDDays: from sowing to emergence",
            f"  {params['gdd_max_rooting']}         : GDDays: from sowing to maximum rooting depth",
            f"  {params['gdd_senescence']}         : GDDays: from sowing to start senescence",
            f"  {params['gdd_maturity']}         : GDDays: from sowing to maturity (length of crop cycle)",
            f"     {params['gdd_flowering']}         : GDDays: from sowing to flowering",
            f"     {params['gdd_flowering_length']}         : Length of the flowering stage (growing degree days)",
            f"     {params['cgc_gdd']:.6f}  : CGC for GGDays: Increase in canopy cover (in fraction soil cover per growing-degree day)",
            f"     {params['cdc_gdd']:.6f}  : CDC for GGDays: Decrease in canopy cover (in fraction per growing-degree day)",
            f"   {params['gdd_hi_start']}         : GDDays: building-up of Harvest Index during yield formation",
            f"    {params['dry_matter_content']}         : dry matter content (%) of fresh yield",
            f"     {params['first_year_min_rooting']:.2f}      : Minimum effective rooting depth (m) in first year (for perennials)",
            f"     {1 if params['is_perennial'] else 0}         : Crop is {'perennial' if params['is_perennial'] else 'not perennial'} (for perennials)",
            f"     {params['assimilate_transfer']}         : Transfer of assimilates from above ground parts to root system is {'considered' if params['assimilate_transfer'] else 'not considered'}",
            f"   {params['assimilate_storage_days']}         : Number of days at end of season during which assimilates are stored in root system",
            f"    {params['assimilate_transfer_percent']}         : Percentage of assimilates transferred to root system at last day of season",
            f"    {params['root_to_shoot_transfer_percent']}         : Percentage of stored assimilates transferred to above ground parts in next season",
            "",
            " Internal crop calendar",
            " ========================================================",
            f"    {params['restart_type']}         : The Restart of growth is generated by {'Growing-degree days' if params['restart_type'] == 13 else 'other method'}",
            f"     {params['restart_window_day']}         : First Day for the time window (Restart of growth)",
            f"     {params['restart_window_month']}         : First Month for the time window (Restart of growth)",
            f"   {params['restart_window_length']}         : Length (days) of the time window (Restart of growth)",
            f"    {params['restart_gdd_threshold']:.1f}       : Threshold for the Restart criterion: Growing-degree days",
            f"     {params['restart_days_required']}         : Number of successive days for the Restart criterion",
            f"     {params['restart_occurrences']}         : Number of occurrences before the Restart criterion applies",
            f"    {params['end_type']}         : The End of growth is generated by {'Growing-degree days' if params['end_type'] == 63 else 'other method'}",
            f"    {params['end_window_day']}         : Last Day for the time window (End of growth)",
            f"    {params['end_window_month']}         : Last Month for the time window (End of growth)",
            f"     {params['end_window_years_offset']}         : Number of years to add to the Onset year",
            f"    {params['end_window_length']}         : Length (days) of the time window (End of growth)",
            f"    {params['end_gdd_threshold']:.1f}       : Threshold for the End criterion: Growing-degree days",
            f"     {params['end_days_required']}         : Number of successive days for the End criterion",
            f"     {params['end_occurrences']}         : Number of occurrences before the End criterion applies"
        ])
        
        content = "\n".join(lines)
        
        if file_path:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
        
        return file_path
        
    except KeyError as e:
        # This should not happen if validation is properly done, but just in case
        raise ValueError(f"Missing parameter: {str(e)}")

# Example usage in Crop class
class Crop:
    """
    Represents a crop with its growth parameters for AquaCrop simulation
    """
    def __init__(self, name: str, description: str, params: Dict[str, Any], strict_validation: bool = True):
        """
        Initialize a crop entity
        
        Args:
            name: Crop name (used for file naming)
            description: Crop description
            params: Dictionary of crop parameters
            strict_validation: Whether to strictly validate all required parameters
        """
        self.name = "".join(name.split())
        self.description = description
        self.params = params
        self.strict_validation = strict_validation
        
        # Validate parameters during initialization
        missing_params = validate_crop_parameters(params)
        if missing_params and strict_validation:
            raise ValueError(f"Missing required crop parameters: {', '.join(missing_params)}")
        
    def generate_file(self, directory: str) -> str:
        """Generate crop file in directory and return file path"""
        return generate_crop_file(
            file_path=f"{directory}/{self.name}.CRO",
            description=self.description,
            params=self.params,
            strict_validation=self.strict_validation
        )