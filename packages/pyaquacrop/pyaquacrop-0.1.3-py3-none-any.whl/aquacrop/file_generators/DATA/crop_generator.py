"""
Crop file generator for AquaCrop (.CRO files)
"""

import os
from typing import Dict, Optional
from aquacrop.constants import Constants

def generate_crop_file(
    file_path: str,
    description: str,
    params: Dict,
) -> str:
    """
    Generate an AquaCrop crop file (.CRO) with all possible crop parameters
    
    Args:
        file_path: Path to write the file
        description: Crop description
        params: Dictionary of crop parameters (all possible parameters accepted):
            # Basic crop classification
            - crop_type: Crop type (1=leafy, 2=fruit/grain, 3=root/tuber, 4=forage)
            - is_sown: Whether the crop is sown (True) or transplanted (False)
            - cycle_determination: Method to determine crop cycle (0=calendar days, 1=growing degree-days)
            - adjust_for_eto: Whether to adjust soil water depletion factors by ETo
            
            # Temperature parameters
            - base_temp: Base temperature (°C) below which crop development does not progress
            - upper_temp: Upper temperature (°C) above which crop development no longer increases
            - gdd_cycle_length: Total length of crop cycle in growing degree-days
            - gdd_method: Method for calculating growing degree days (1-3)
            
            # Crop water stress parameters
            - p_upper_canopy: Upper threshold for canopy expansion water stress
            - p_lower_canopy: Lower threshold for canopy expansion water stress
            - shape_canopy: Shape factor for water stress coefficient for canopy expansion
            - p_upper_stomata: Upper threshold for stomatal water stress
            - shape_stomata: Shape factor for water stress coefficient for stomatal control
            - p_upper_senescence: Upper threshold for canopy senescence water stress
            - shape_senescence: Shape factor for water stress coefficient for canopy senescence
            - p_upper_pollination: Upper threshold for pollination water stress
            - aeration_stress_threshold: Vol% for anaerobic point (SAT-vol% at which deficient aeration occurs)
            
            # Soil fertility stress parameters
            - fertility_stress_calibration: Soil fertility stress level (%) used for calibration
            - shape_fertility_canopy_expansion: Shape factor for fertility stress impact on canopy expansion
            - shape_fertility_max_canopy: Shape factor for fertility stress impact on maximum canopy cover
            - shape_fertility_water_productivity: Shape factor for fertility stress impact on water productivity
            - shape_fertility_decline: Shape factor for fertility stress impact on canopy decline
            
            # Temperature stress parameters
            - cold_stress_for_pollination: Minimum air temperature (°C) below which pollination fails
            - heat_stress_for_pollination: Maximum air temperature (°C) above which pollination fails
            - minimum_growing_degrees_pollination: Minimum GDD required for full transpiration (°C-day)
            
            # Salinity stress parameters
            - salinity_threshold_ece: EC level at which crop is affected by salinity (dS/m)
            - salinity_max_ece: EC level at which crop can no longer grow (dS/m)
            - salinity_shape_factor: Shape of the salinity response curve
            - salinity_stress_cc: Calibrated distortion (%) of canopy cover due to salinity stress
            - salinity_stress_stomata: Calibrated response (%) of stomata to salinity stress
            
            # Transpiration parameters
            - kc_max: Crop coefficient when canopy is complete but prior to senescence
            - kc_decline: Decline of crop coefficient (%/day) due to aging or nitrogen deficiency
            
            # Rooting parameters
            - min_rooting_depth: Minimum effective rooting depth (m)
            - max_rooting_depth: Maximum effective rooting depth (m)
            - root_expansion_shape: Shape factor describing root zone expansion
            - max_water_extraction_top: Maximum root water extraction (m³/m³/day) in top quarter
            - max_water_extraction_bottom: Maximum root water extraction (m³/m³/day) in bottom quarter
            - soil_evaporation_reduction: Effect of canopy cover in reducing soil evaporation (%)
            
            # Canopy development parameters
            - canopy_cover_per_seedling: Soil surface covered by an individual seedling at 90% emergence (cm²)
            - plant_density: Number of plants per hectare
            - max_canopy_cover: Maximum canopy cover (CCx) as fraction
            - canopy_growth_coefficient: Increase in canopy cover (fraction per day)
            - canopy_decline_coefficient: Decrease in canopy cover (fraction per day)
            - canopy_regrowth_size: Canopy size of individual plant (re-growth) at 1st day (cm²)
            - canopy_thinning_years: Years at which CCx declines due to self-thinning (perennials)
            - canopy_thinning_shape: Shape factor of the decline of CCx over the years (perennials)
            
            # Crop cycle parameters (Calendar days)
            - days_emergence: Days from sowing to emergence
            - days_max_rooting: Days from sowing to maximum rooting depth
            - days_senescence: Days from sowing to start senescence
            - days_maturity: Days from sowing to maturity (length of crop cycle)
            - days_flowering: Days from sowing to flowering
            - days_flowering_length: Length of the flowering stage (days)
            - days_crop_determinancy: Crop determinancy linked with flowering (0=no, 1=yes)
            - days_hi_start: Days at which harvest index building starts
            
            # Crop cycle parameters (Growing degree days)
            - gdd_emergence: GDD from sowing to emergence
            - gdd_max_rooting: GDD from sowing to maximum rooting depth
            - gdd_senescence: GDD from sowing to start senescence
            - gdd_maturity: GDD from sowing to maturity
            - gdd_flowering: GDD from sowing to flowering
            - gdd_flowering_length: Length of flowering stage (GDD)
            - cgc_gdd: Canopy growth coefficient in GDD (fraction per growing degree day)
            - cdc_gdd: Canopy decline coefficient in GDD (fraction per growing degree day)
            - gdd_hi_start: GDD for building up of harvest index during yield formation
            
            # Biomass and yield parameters
            - water_productivity: Water productivity normalized for ETo and CO2 (g/m²)
            - water_productivity_yield_formation: WP* during yield formation (% of WP*)
            - co2_response_strength: Biomass response to elevated atmospheric CO2 (%)
            - harvest_index: Reference harvest index (HIo) (%)
            - water_stress_hi_increase: Possible increase (%) of HI due to water stress before flowering
            - veg_growth_impact_hi: Impact of restricted vegetative growth on HI
            - stomatal_closure_impact_hi: Effect of stomatal closure on HI
            - max_hi_increase: Allowable maximum increase (%) of specified HI
            - dry_matter_content: Dry matter content (%) of fresh yield
            
            # Perennial crop parameters
            - is_perennial: Whether the crop is perennial
            - first_year_min_rooting: Minimum effective rooting depth (m) in first year
            - assimilate_transfer: Whether transfer of assimilates to root system is considered (0=no, 1=yes)
            - assimilate_storage_days: Days at end of season for storing assimilates in root system
            - assimilate_transfer_percent: Percentage of assimilates transferred to root system
            - root_to_shoot_transfer_percent: Percentage of stored assimilates transferred to shoots
            
            # Crop calendar for perennials
            - restart_type: What triggers regrowth (13=Growing degree days, etc.)
            - restart_window_day: First day for restart time window
            - restart_window_month: First month for restart time window
            - restart_window_length: Length of restart time window (days)
            - restart_gdd_threshold: GDD threshold for restart
            - restart_days_required: Number of successive days for restart criterion
            - restart_occurrences: Number of occurrences before restart criterion applies
            - end_type: What triggers end of growth (63=Growing degree days, etc.)
            - end_window_day: Last day for end time window
            - end_window_month: Last month for end time window
            - end_window_years_offset: Years to add to onset year
            - end_window_length: Length of end time window (days)
            - end_gdd_threshold: GDD threshold for end criterion
            - end_days_required: Number of successive days for end criterion
            - end_occurrences: Number of occurrences before end criterion applies
            
        version: AquaCrop version
    
    Returns:
        The path to the generated file
    """
    # Default values for all parameters (these will be overridden by the values in params)
    
    
    # Update with provided parameters
   
    
    is_protected = 1  # File not protected
    
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
        f"     {1 if params['is_perennial'] else 0}         : Crop is {'sown' if params['is_perennial'] else 'not sown'} in 1st year (for perennials)",
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