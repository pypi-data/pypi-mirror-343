# #!/usr/bin/env python
# """
# Example script for testing the AquaCrop Python API

# This script demonstrates how to use the AquaCrop Python API to set up and run
# a crop simulation for maize (corn) grown under rainfed conditions.
# """

# import os
# from datetime import date

# import matplotlib.pyplot as plt
# import pandas as pd

# # Import AquaCrop components
# from aquacrop import (
#     AquaCrop,
#     Calendar,
#     Crop,
#     FieldManagement,
#     InitialConditions,
#     Irrigation,
#     Parameter,
#     Soil,
#     SoilLayer,
#     Weather,
# )


# def test_main():
#     """Run a sample AquaCrop simulation for maize crop"""
#     print("Setting up AquaCrop simulation for maize...")

#     # Define simulation period
#     start_date = date(2020, 5, 1)  # May 1, 2020
#     end_date = date(2020, 10, 15)  # October 15, 2020
#     planting_date = date(2020, 5, 5)  # May 5, 2020

#     # Create output directory
#     output_dir = "tests/tempFiles"
#     os.makedirs(output_dir, exist_ok=True)

#     # Setup soil profile (loamy soil)
#     soil = Soil(
#         name="Loam",
#         description="Loamy soil with good water holding capacity",
#         soil_layers=[
#             SoilLayer(
#                 thickness=1.50,
#                 sat=46.0,
#                 fc=29.0,
#                 wp=13.0,
#                 ksat=1200.0,
#                 description="Loam topsoil",
#             )
#         ],
#         curve_number=46,  # SCS curve number for runoff estimation
#         readily_evaporable_water=7,  # mm
#     )

#     # Setup maize crop parameters
#     maize = Crop(
#         name="Maize",
#         description="Maize/Corn with 120-day cycle",
#         params={
#             # Basic classifications
#             "crop_type": 2,  # forage crop
#             "is_sown": True,
#             "cycle_determination": 0,  # by growing degree-days
#             "adjust_for_eto": True,
#             # Temperature parameters
#             "base_temp": 5.0,
#             "upper_temp": 30.0,
#             "gdd_cycle_length": 1920,
#             "dormancy_eto_threshold": 600,
#             # Crop water stress parameters
#             "p_upper_canopy": 0.15,
#             "p_lower_canopy": 0.55,
#             "shape_canopy": 3.0,
#             "p_upper_stomata": 0.60,
#             "shape_stomata": 3.0,
#             "p_upper_senescence": 0.70,
#             "shape_senescence": 3.0,
#             "p_upper_pollination": 0.90,
#             "aeration_stress_threshold": 2,
#             # Soil fertility stress parameters
#             "fertility_stress_calibration": 50,
#             "shape_fertility_canopy_expansion": 2.35,
#             "shape_fertility_max_canopy": 0.79,
#             "shape_fertility_water_productivity": -0.16,
#             "shape_fertility_decline": 6.26,
#             # Temperature stress parameters
#             "cold_stress_for_pollination": 8,
#             "heat_stress_for_pollination": 40,
#             "minimum_growing_degrees_pollination": 8.0,
#             # Salinity stress parameters
#             "salinity_threshold_ece": 2,
#             "salinity_max_ece": 16,
#             "salinity_shape_factor": -9,
#             "salinity_stress_cc": 25,
#             "salinity_stress_stomata": 100,
#             # Transpiration parameters
#             "kc_max": 1.15,
#             "kc_decline": 0.050,
#             # Rooting parameters
#             "min_rooting_depth": 0.30,
#             "max_rooting_depth": 3.00,
#             "root_expansion_shape": 15,
#             "max_water_extraction_top": 0.020,
#             "max_water_extraction_bottom": 0.010,
#             "soil_evaporation_reduction": 60,
#             # Canopy development parameters
#             "canopy_cover_per_seedling": 2.50,
#             "canopy_regrowth_size": 19.38,
#             "plant_density": 2000000,
#             "max_canopy_cover": 0.95,
#             "canopy_growth_coefficient": 0.17713,
#             "canopy_thinning_years": 9,
#             "canopy_thinning_shape": 0.50,
#             "canopy_decline_coefficient": 0.03636,
#             # Crop cycle parameters (Calendar days)
#             "days_emergence": 2,
#             "days_max_rooting": 178,
#             "days_senescence": 180,
#             "days_maturity": 180,
#             "days_flowering": 0,
#             "days_flowering_length": 0,
#             "days_crop_determinancy": 0,
#             "days_hi_start": 17,
#             # Crop cycle parameters (Growing degree days)
#             "gdd_emergence": 5,
#             "gdd_max_rooting": 1920,
#             "gdd_senescence": 1920,
#             "gdd_maturity": 1920,
#             "gdd_flowering": 0,
#             "gdd_flowering_length": 0,
#             "cgc_gdd": 0.012,
#             "cdc_gdd": 0.006,
#             "gdd_hi_start": 118,
#             # Biomass and yield parameters
#             "water_productivity": 15.0,
#             "water_productivity_yield_formation": 100,
#             "co2_response_strength": 50,
#             "harvest_index": 1.00,
#             "water_stress_hi_increase": -9,
#             "veg_growth_impact_hi": -9.0,
#             "stomatal_closure_impact_hi": -9.0,
#             "max_hi_increase": -9,
#             "dry_matter_content": 20,
#             # Perennial crop parameters
#             "is_perennial": False,
#             "first_year_min_rooting": 0.30,
#             "assimilate_transfer": 1,
#             "assimilate_storage_days": 100,
#             "assimilate_transfer_percent": 65,
#             "root_to_shoot_transfer_percent": 60,
#             # Crop calendar for perennials
#             "restart_type": 13,
#             "restart_window_day": 1,
#             "restart_window_month": 4,
#             "restart_window_length": 120,
#             "restart_gdd_threshold": 20.0,
#             "restart_days_required": 8,
#             "restart_occurrences": 2,
#             "end_type": 63,
#             "end_window_day": 31,
#             "end_window_month": 10,
#             "end_window_years_offset": 0,
#             "end_window_length": 60,
#             "end_gdd_threshold": 10.0,
#             "end_days_required": 8,
#             "end_occurrences": 1,
#         },
#     )

#     # Create synthetic weather data
#     # In a real application, you would load actual weather data
#     # This is a simplified example with constant values
#     temps = [(15.0, 28.0)] * 180  # 180 days of min=15.0°C, max=28.0°C
#     eto = [5.0] * 180  # 5 mm/day reference ET

#     # Create some rainfall events
#     rainfall = [0.0] * 180
#     # Add some rainfall events
#     rain_days = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
#     rain_amounts = [15, 25, 10, 20, 30, 5, 15, 25, 10, 15, 5, 10]
#     for day, amount in zip(rain_days, rain_amounts):
#         rainfall[day] = amount

#     # Create CO2 data
#     co2_records = [
#         (1902, 297.4),
#         (1950, 311.0),
#         (2000, 369.71),
#         (2020, 414.21),
#         (2025, 430.0),
#     ]

#     # Setup weather
#     climate = Weather(
#         location="TestLocation",
#         temperatures=temps,
#         eto_values=eto,
#         rainfall_values=rainfall,
#         record_type=1,  # 1=daily
#         first_day=1,
#         first_month=5,  # May
#         first_year=2020,
#         co2_records=co2_records,
#     )

#     # Field management settings
#     management = FieldManagement(
#         name="StandardManagement",
#         description="Standard field management practices",
#         params={
#             "fertility_stress": 0,  # No soil fertility stress
#             "mulch_cover": 0,  # No mulch
#             "bund_height": 0.0,  # No bunds
#             "surface_runoff_affected": 0,  # Default surface runoff
#         },
#     )

#     # Setup optional irrigation (but we'll use rainfed in this example)
#     irrigation = Irrigation(
#         name="RainfedOnly",
#         description="No irrigation - rainfed only",
#         params={
#             "irrigation_method": 1,  # 1=Sprinkler
#             "irrigation_mode": 3,  # 3=No irrigation (calculate requirements only)
#         },
#     )

#     # Model parameters
#     parameter = Parameter(
#         name="DefaultParams",
#         params={
#             # Using library defaults
#         },
#     )

#     # Initial conditions
#     initial_conditions = InitialConditions(
#         name="StandardInitial",
#         description="Standard initial conditions with 50% TAW",
#         params={
#             "soil_water_content_type": 0,  # 0=for specific layers
#             "soil_data": [
#                 {
#                     "thickness": 0.3,
#                     "water_content": 23.0,
#                     "ec": 0.0,
#                 },  # 50% TAW in topsoil
#                 {
#                     "thickness": 1.7,
#                     "water_content": 20.5,
#                     "ec": 0.0,
#                 },  # 50% TAW in subsoil
#             ],
#         },
#     )

#     # Create AquaCrop simulation
#     simulation = AquaCrop(
#         start_date=start_date,
#         end_date=end_date,
#         planting_date=planting_date,
#         crop=maize,
#         soil=soil,
#         irrigation=irrigation,
#         management=management,
#         climate=climate,
#         initial_conditions=initial_conditions,
#         parameter=parameter,
#         working_dir=output_dir,
#         need_daily_output=True,
#         need_seasonal_output=True,
#     )

#     # Run simulation
#     print("Running AquaCrop simulation...")
#     results = simulation.run()

#     # Save results to CSV files
#     print("Saving results...")
#     results_dir = simulation.save_results()

#     # Analyze and plot results
#     analyze_results(results, output_dir)

#     print(f"Simulation completed. Results saved to {results_dir}")

#     return results


# def analyze_results(results, output_dir):
#     """Analyze and plot simulation results"""
#     # Check if we have daily results
#     if results["day"] is not None:
#         daily_data = results["day"]

#         # Create a plots directory
#         plots_dir = os.path.join(output_dir, "plots")
#         os.makedirs(plots_dir, exist_ok=True)

#         # Create key plots
#         plot_data(
#             daily_data,
#             "Day",
#             "CC",
#             "Canopy Cover",
#             os.path.join(plots_dir, "canopy_cover.png"),
#         )
#         plot_data(
#             daily_data,
#             "Day",
#             "Biomass",
#             "Biomass (ton/ha)",
#             os.path.join(plots_dir, "biomass.png"),
#         )
#         plot_data(
#             daily_data,
#             "Day",
#             "SWC",
#             "Soil Water Content (mm)",
#             os.path.join(plots_dir, "soil_water.png"),
#         )

#         # Plot water stress
#         if "Tr" in daily_data.columns and "Trx" in daily_data.columns:
#             daily_data["WaterStress"] = 1 - (daily_data["Tr"] / daily_data["Trx"])
#             plot_data(
#                 daily_data,
#                 "Day",
#                 "WaterStress",
#                 "Water Stress (0-1)",
#                 os.path.join(plots_dir, "water_stress.png"),
#             )

#         # Print summary statistics
#         print("\nSimulation Summary:")
#         print(f"Maximum Canopy Cover: {daily_data['CC'].max():.2f}%")
#         print(f"Final Biomass: {daily_data['Biomass'].iloc[-1]:.2f} ton/ha")

#         if "Y(dry)" in daily_data.columns:
#             print(f"Final Dry Yield: {daily_data['Y(dry)'].iloc[-1]:.2f} ton/ha")

#         # Water balance components
#         if "Rain" in daily_data.columns:
#             total_rain = daily_data["Rain"].sum()
#             print(f"Total Rainfall: {total_rain:.1f} mm")

#         if "Irr" in daily_data.columns:
#             total_irr = daily_data["Irr"].sum()
#             print(f"Total Irrigation: {total_irr:.1f} mm")

#         if "Tr" in daily_data.columns:
#             total_tr = daily_data["Tr"].sum()
#             print(f"Total Transpiration: {total_tr:.1f} mm")

#         if "E" in daily_data.columns:
#             total_e = daily_data["E"].sum()
#             print(f"Total Soil Evaporation: {total_e:.1f} mm")

#     # Check if we have seasonal results
#     if results["season"] is not None:
#         seasonal_data = results["season"]
#         print("\nSeasonal Results:")
#         print(seasonal_data)


# def plot_data(data, x_col, y_col, title, output_path=None, display=True):
#     """
#     Create and display/save a simple plot

#     Args:
#         data: DataFrame containing the data
#         x_col: Column name for x-axis
#         y_col: Column name for y-axis
#         title: Plot title
#         output_path: Path to save the figure (optional)
#         display: Whether to display the figure (default: True)
#     """
#     if y_col not in data.columns:
#         print(
#             f"Warning: Column '{y_col}' not found in data. Available columns: {data.columns.tolist()}"
#         )
#         return

#     # Import libraries at function level to ensure proper handling
#     import matplotlib.pyplot as plt
#     import numpy as np

#     # Create a copy to avoid modifying original data
#     plot_data = data.copy()

#     # Handle potential infinity values for NumPy 2.0 compatibility
#     for col in plot_data.select_dtypes(include=["float"]).columns:
#         mask = np.isinf(plot_data[col])
#         if mask.any():
#             # Replace any infinite values with np.inf (lowercase)
#             plot_data.loc[mask, col] = np.inf

#     fig, ax = plt.figure(figsize=(10, 6)), plt.gca()
#     ax.plot(plot_data[x_col], plot_data[y_col])
#     ax.set_title(title)
#     ax.set_xlabel("Days After Planting")
#     ax.set_ylabel(title)
#     ax.grid(True)

#     # Save the figure if output_path is provided
#     if output_path:
#         # plt.savefig(output_path)
#         # print(f"Plot saved to {output_path}")
#         pass

#     # Display the figure if requested
#     if display:
#         plt.show()
#     else:
#         plt.close()

#     return fig, ax  # Return figure and axes for further customization if needed
