import atexit
import os
import platform
import shutil
import subprocess
import tempfile
import urllib.request
import zipfile
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.error import URLError

from aquacrop.utils.julianDayConverter import calculateAquaCropJulianDay


class WeatherDataSufficiencyError(Exception):
    """Exception raised when weather data is insufficient for simulation period."""

    pass


class AquaCrop:
    """
    High-level wrapper for AquaCrop model that orchestrates:
    - Initialization of all required entities
    - File generation in a working directory
    - Running the AquaCrop model
    - Parsing and returning results

    Now with support for multi-year simulations.
    """

    def __init__(
        self,
        simulation_periods: Optional[List[Dict]] = None,
        crop=None,
        soil=None,
        irrigation=None,
        management=None,
        climate=None,
        calendar=None,
        off_season=None,
        observation=None,
        ground_water=None,
        initial_conditions=None,
        parameter=None,
        working_dir=None,
        need_daily_output=True,
        need_seasonal_output=True,
        need_harvest_output=True,
        need_evaluation_output=True,
    ):

        # Handle both new simulation_periods approach and old separate parameters approach
        if not simulation_periods:
            raise ValueError("At least one simulation period must be provided")

        # Store the complete simulation periods
        self.simulation_periods = simulation_periods

        # Extract main dates from first period
        first_period = simulation_periods[0]

        # Set backward-compatible attributes for the first period
        self.start_date = first_period["start_date"]
        self.end_date = first_period["end_date"]

        # Handle missing planting_date
        if "planting_date" not in first_period:
            first_period["planting_date"] = first_period["start_date"]
        self.planting_date = first_period["planting_date"]

        # Set default is_seeding_year if not specified for each period
        if "is_seeding_year" not in first_period:
            first_period["is_seeding_year"] = True

        # Store all other parameters
        self.crop = crop
        self.soil = soil
        self.irrigation = irrigation
        self.management = management
        self.climate = climate
        self.calendar = calendar
        self.off_season = off_season
        self.observation = observation
        self.ground_water = ground_water
        self.initial_conditions = initial_conditions
        self.parameter = parameter

        # Setup working directory
        self.is_temp_dir = working_dir is None
        self.working_dir = (
            os.path.abspath(working_dir)
            if working_dir
            else tempfile.mkdtemp(prefix="aquacrop_")
        )
        if self.working_dir is None:
            self.working_dir = tempfile.mkdtemp(prefix="aquacrop_")

        self.need_daily_output = need_daily_output
        self.need_seasonal_output = need_seasonal_output
        self.need_harvest_output = need_harvest_output
        self.need_evaluation_output = need_evaluation_output
        self.results = None

        # Get the actual directory where the aquacrop package is installed
        # This uses the current module's location to find the package root
        aquacrop_dir = os.path.dirname(os.path.abspath(__file__))

        self.root_directory = os.path.dirname(aquacrop_dir)

        # Register cleanup for temporary directory
        if self.is_temp_dir:
            atexit.register(self._cleanup)

    def __del__(self):
        """Clean up temporary directory if it was created automatically"""
        self._cleanup()

    def _cleanup(self):
        """Clean up temporary resources"""
        if (
            self.is_temp_dir
            and hasattr(self, "working_dir")
            and self.working_dir
            and os.path.exists(self.working_dir)
        ):
            try:
                shutil.rmtree(self.working_dir)
                self.is_temp_dir = False  # Prevent multiple cleanup attempts
            except Exception as e:
                print(
                    f"Warning: Failed to clean up temporary directory {self.working_dir}: {e}"
                )

    def _check_weather_data_sufficiency(self) -> Dict[str, Any]:
        """
        Check if weather data is sufficient for the entire simulation period.

        Returns:
            Dictionary containing sufficiency status for each weather component
            and detailed information about required vs available entries.
        """
        # Calculate total simulation days
        start_simulation = self.simulation_periods[0]["start_date"]
        end_simulation = self.simulation_periods[-1]["end_date"]
        total_days = (end_simulation - start_simulation).days + 1

        # Calculate required entries based on record type
        if self.climate is None:
            raise ValueError(
                "Climate data is not provided. Please ensure 'self.climate' is set."
            )
        record_type = self.climate.record_type
        required_entries = total_days  # For daily data
        if record_type == 2:  # 10-daily
            required_entries = (total_days + 9) // 10
        elif record_type == 3:  # Monthly
            required_entries = (total_days + 30) // 30

        # Check data sufficiency
        available_temp = len(self.climate.temperatures)
        available_eto = len(self.climate.eto_values)
        available_rain = len(self.climate.rainfall_values)

        is_temp_sufficient = available_temp >= required_entries
        is_eto_sufficient = available_eto >= required_entries
        is_rain_sufficient = available_rain >= required_entries

        all_sufficient = is_temp_sufficient and is_eto_sufficient and is_rain_sufficient

        data_status = {
            "all_sufficient": all_sufficient,
            "temperature_sufficient": is_temp_sufficient,
            "eto_sufficient": is_eto_sufficient,
            "rainfall_sufficient": is_rain_sufficient,
            "required_entries": required_entries,
            "available": {
                "temperature": available_temp,
                "eto": available_eto,
                "rainfall": available_rain,
            },
            "simulation_period": {
                "start_date": start_simulation,
                "end_date": end_simulation,
                "total_days": total_days,
            },
            "record_type": {
                "code": record_type,
                "description": (
                    "daily"
                    if record_type == 1
                    else "10-daily" if record_type == 2 else "monthly"
                ),
            },
        }

        return data_status

    def _validate_weather_data(self, strict: bool = False) -> Dict[str, Any]:
        """
        Validate weather data sufficiency before running a simulation.

        Args:
            strict: If True, raise an exception if data is insufficient.
                   If False, just return validation status.

        Returns:
            Dictionary containing validation status.

        Raises:
            WeatherDataSufficiencyError: If weather data is insufficient and strict checking is enabled.
        """
        data_status = self._check_weather_data_sufficiency()

        if not data_status["all_sufficient"] and strict:
            missing_components = []
            if not data_status["temperature_sufficient"]:
                missing_components.append(
                    f"temperature (has {data_status['available']['temperature']}, needs {data_status['required_entries']})"
                )
            if not data_status["eto_sufficient"]:
                missing_components.append(
                    f"ETo (has {data_status['available']['eto']}, needs {data_status['required_entries']})"
                )
            if not data_status["rainfall_sufficient"]:
                missing_components.append(
                    f"rainfall (has {data_status['available']['rainfall']}, needs {data_status['required_entries']})"
                )

            error_msg = (
                f"Insufficient weather data for simulation period "
                f"({data_status['simulation_period']['start_date']} to {data_status['simulation_period']['end_date']}). "
                f"Missing data for: {', '.join(missing_components)}."
            )

            raise WeatherDataSufficiencyError(error_msg)

        return data_status

    def _initialize(self):
        pass

    def _setup_working_dir(self):
        """Set up working directory with all necessary files"""
        print(f"Setting up working directory at: {self.working_dir}")

        # Create main directories
        if not self.working_dir:
            raise ValueError("Working directory is not set.")
        os.makedirs(os.path.join(self.working_dir, "DATA"), exist_ok=True)
        os.makedirs(os.path.join(self.working_dir, "OUTP"), exist_ok=True)
        os.makedirs(os.path.join(self.working_dir, "SIMUL"), exist_ok=True)
        os.makedirs(os.path.join(self.working_dir, "LIST"), exist_ok=True)
        os.makedirs(os.path.join(self.working_dir, "OBS"), exist_ok=True)
        os.makedirs(os.path.join(self.working_dir, "PARAM"), exist_ok=True)

        # Generate entity files
        data_dir = os.path.join(self.working_dir, "DATA")
        obs_dir = os.path.join(self.working_dir, "OBS")
        list_dir = os.path.join(self.working_dir, "LIST")
        param_dir = os.path.join(self.working_dir, "PARAM")
        simul_dir = os.path.join(self.working_dir, "SIMUL")

        # Generate climate files
        if self.climate is None:
            raise ValueError(
                "Climate data is not provided. Please ensure 'self.climate' is set."
            )
        climate_files = self.climate.generate_files(data_dir)

        # Generate crop file
        if self.crop is None:
            raise ValueError(
                "Crop data is not provided. Please ensure 'self.crop' is set."
            )
        crop_file = self.crop.generate_file(data_dir)

        # Generate soil file
        if self.soil is None:
            raise ValueError(
                "Soil data is not provided. Please ensure 'self.soil' is set."
            )
        soil_file = self.soil.generate_file(data_dir)

        # Generate irrigation file
        irrigation_file = None
        if self.irrigation:
            irrigation_file = self.irrigation.generate_file(data_dir)

        # Generate management file
        if self.management is None:
            raise ValueError(
                "Management data is not provided. Please ensure 'self.management' is set."
            )
        management_file = self.management.generate_file(data_dir)
        # Generate parameter file if provided
        if self.parameter:
            self.parameter.generate_file(param_dir)

        # Generate optional files if provided
        calendar_file = None
        if self.calendar:
            calendar_file = self.calendar.generate_file(data_dir)

        off_season_file = None
        if self.off_season:
            off_season_file = self.off_season.generate_file(data_dir)

        observation_file = None
        if self.observation:
            observation_file = self.observation.generate_file(obs_dir)

        ground_water_file = None
        if self.ground_water:
            ground_water_file = self.ground_water.generate_file(data_dir)

        initial_conditions_file = None
        if self.initial_conditions:
            initial_conditions_file = self.initial_conditions.generate_file(data_dir)

        # Generate project file
        from aquacrop.file_generators.LIST.prm_generator import generate_project_file

        # Initialize periods list
        periods = []

        # Process all simulation periods
        for i, period_data in enumerate(self.simulation_periods, start=1):
            # Handle missing planting_date (use start_date if not provided)
            if "planting_date" not in period_data:
                planting_date = period_data["start_date"]
            else:
                planting_date = period_data["planting_date"]

            period = {
                "year": i,
                "first_day_sim": calculateAquaCropJulianDay(period_data["start_date"]),
                "last_day_sim": calculateAquaCropJulianDay(period_data["end_date"]),
                "first_day_crop": calculateAquaCropJulianDay(planting_date),
                "last_day_crop": calculateAquaCropJulianDay(period_data["end_date"]),
                "is_seeding_year": period_data.get(
                    "is_seeding_year", True if i == 1 else False
                ),
                "cli_file": os.path.basename(climate_files["climate"]),
                "tnx_file": os.path.basename(climate_files["temperature"]),
                "eto_file": os.path.basename(climate_files["eto"]),
                "plu_file": os.path.basename(climate_files["rainfall"]),
                "co2_file": os.path.basename(climate_files["co2"]),
                "cal_file": (
                    os.path.basename(calendar_file) if calendar_file else "(None)"
                ),
                "cro_file": os.path.basename(crop_file),
                "irr_file": (
                    os.path.basename(irrigation_file) if irrigation_file else "(None)"
                ),
                "man_file": os.path.basename(management_file),
                "sol_file": os.path.basename(soil_file),
                "gwt_file": (
                    os.path.basename(ground_water_file)
                    if ground_water_file
                    else "(None)"
                ),
                # Use "KeepSWC" for years after first to continue with soil water from previous run
                "sw0_file": (
                    "KeepSWC"
                    if i > 1
                    else (
                        os.path.basename(initial_conditions_file)
                        if initial_conditions_file
                        else "(None)"
                    )
                ),
                "off_file": (
                    os.path.basename(off_season_file) if off_season_file else "(None)"
                ),
                "obs_file": (
                    os.path.basename(observation_file) if observation_file else "(None)"
                ),
            }
            periods.append(period)

        # Generate the project file with all periods
        project_file = generate_project_file(
            file_path=os.path.join(list_dir, "PROJECT.PRM"),
            description=f"AquaCrop simulation for {os.path.basename(crop_file)}",
            periods=periods,
        )

        # Configure output settings
        from aquacrop.file_generators.SIMUL.daily_results_generator import (
            generate_daily_results_settings,
        )
        from aquacrop.file_generators.SIMUL.particular_result_generator import (
            generate_particular_results_settings,
        )

        if self.need_daily_output:
            generate_daily_results_settings(
                file_path=os.path.join(simul_dir, "DailyResults.SIM"),
                output_types=[1, 2, 3, 4, 5, 6, 7, 8],  # Enable all output types
            )

        if self.need_harvest_output or self.need_evaluation_output:
            generate_particular_results_settings(
                file_path=os.path.join(simul_dir, "ParticularResults.SIM"),
                output_types=[1, 2],  # Enable both harvest and evaluation outputs
            )

        # Return project file path
        return project_file

    def _download_aquacrop_executable(self, url, target_dir):
        """
        Download and extract the AquaCrop executable from the given URL using built-in Python libraries

        Args:
            url: URL to download the zip file from
            target_dir: Directory to extract the executable to

        Returns:
            Path to the extracted executable
        """

        print(f"Downloading AquaCrop executable from {url}")

        # Create target directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        # Download the zip file to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as temp_file:
            try:
                with urllib.request.urlopen(url) as response:
                    # Copy the downloaded data to our temporary file
                    shutil.copyfileobj(response, temp_file)

            except URLError as e:
                raise RuntimeError(f"Failed to download from {url}: {e}")

        try:
            # Extract the zip file
            with zipfile.ZipFile(temp_file.name, "r") as zip_ref:
                zip_ref.extractall(target_dir)

            # Determine the executable name based on platform
            system = platform.system().lower()
            if system == "windows":
                exe_name = "aquacrop.exe"
            else:
                exe_name = "aquacrop"

            # Find the extracted executable
            for root, dirs, files in os.walk(target_dir):
                if exe_name in files:
                    exe_path = os.path.join(root, exe_name)

                    # Set executable permissions on Unix-like systems
                    if system != "windows":
                        import stat

                        os.chmod(
                            exe_path,
                            os.stat(exe_path).st_mode
                            | stat.S_IXUSR
                            | stat.S_IXGRP
                            | stat.S_IXOTH,
                        )

                    print(f"Extracted AquaCrop executable to {exe_path}")
                    return exe_path

            raise FileNotFoundError(f"Could not find {exe_name} in the extracted files")

        finally:
            # Clean up the temporary file
            os.unlink(temp_file.name)

    def _find_aquacrop_executable(self):
        """Find the appropriate AquaCrop executable for the current platform"""
        import os
        import platform
        import stat

        system = platform.system().lower()
        arch = platform.machine()

        print(f"Detected platform: {system} ({arch})")

        # Build the expected path based on platform
        model_dir = os.path.join(self.root_directory, "model")

        if system == "linux":
            platform_dir = os.path.join(model_dir, "linux")
            exe_path = os.path.join(platform_dir, "aquacrop")
            download_url = "https://github.com/KUL-RSDA/AquaCrop/releases/download/v7.2/aquacrop-7.2-x86_64-linux.zip"
        elif system == "darwin":  # macOS
            platform_dir = os.path.join(model_dir, "macOS")
            exe_path = os.path.join(platform_dir, "aquacrop")
            download_url = "https://github.com/KUL-RSDA/AquaCrop/releases/download/v7.2/aquacrop-7.2-x86_64-macos.zip"
        elif system == "windows":
            platform_dir = os.path.join(model_dir, "windows")
            exe_path = os.path.join(platform_dir, "aquacrop.exe")
            download_url = "https://github.com/KUL-RSDA/AquaCrop/releases/download/v7.2/aquacrop-7.2-x86_64-windows.zip"
        else:
            raise RuntimeError(f"Unsupported platform: {system}")

        print(f"Looking for executable at: {exe_path}")

        # If executable doesn't exist, download it
        if not os.path.exists(exe_path):
            print(
                f"AquaCrop executable not found at {exe_path}. Downloading from {download_url}"
            )

            try:
                # Ensure the platform directory exists
                os.makedirs(platform_dir, exist_ok=True)

                # Try to download the executable
                exe_path = self._download_aquacrop_executable(
                    download_url, platform_dir
                )
            except Exception as e:
                raise RuntimeError(f"Failed to download AquaCrop executable: {e}")

        # Check if the file is executable
        if not os.access(exe_path, os.X_OK) and system != "windows":
            print(
                f"Warning: The file at {exe_path} exists but is not marked as executable. Setting executable permissions."
            )
            os.chmod(
                exe_path,
                os.stat(exe_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
            )

        return exe_path

    def run(self, validate_data: bool = True, strict_validation: bool = False):
        """
        Run AquaCrop simulation

        Args:
            validate_data: Whether to validate weather data before running simulation
            strict_validation: If True, raise an error if weather data is insufficient

        Returns:
            Simulation results

        Raises:
            WeatherDataSufficiencyError: If weather data is insufficient and strict validation is enabled
        """
        # Validate weather data if requested
        if validate_data:
            data_status = self._validate_weather_data(strict=strict_validation)
            if not data_status["all_sufficient"]:
                print("Warning: Insufficient weather data for simulation period.")
                for component in ["temperature", "eto", "rainfall"]:
                    if not data_status[f"{component}_sufficient"]:
                        print(
                            f"  - {component.capitalize()}: has {data_status['available'][component]}, needs {data_status['required_entries']}"
                        )
                if strict_validation:
                    return None

        # Set up working directory and files
        project_file = self._setup_working_dir()

        print(f"Running AquaCrop simulation with project file: {project_file}")

        # Run AquaCrop executable
        try:
            # Find the AquaCrop executable
            aquacrop_exe_source = self._find_aquacrop_executable()

            # Copy the executable to the working directory
            # AquaCrop requires the executable to be in the same directory as the input files
            aquacrop_exe_dest = os.path.join(
                self.working_dir, os.path.basename(aquacrop_exe_source)
            )

            shutil.copy2(aquacrop_exe_source, aquacrop_exe_dest)

            # Make sure it's executable
            os.chmod(aquacrop_exe_dest, 0o755)

            print(f"Using AquaCrop executable: {aquacrop_exe_dest}")

            # Run AquaCrop with project file
            result = subprocess.run(
                [aquacrop_exe_dest, os.path.basename(project_file)],
                cwd=self.working_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    f"AquaCrop failed with code {result.returncode}: {result.stderr}"
                )

            print(f"AquaCrop simulation completed successfully")

            # Parse output files
            self._parse_results()

            return self.results

        except Exception as e:
            print(f"Error running AquaCrop: {e}")
            raise

    def _parse_results(self):
        """Parse AquaCrop output files and store results"""
        from aquacrop.output import OutputReader

        print(f"Parsing simulation results...")

        # Create output reader and scan output directory
        output_dir = os.path.join(self.working_dir, "OUTP")
        reader = OutputReader(output_dir=output_dir)
        reader.scan_directory()

        # Store results
        self.results = {
            "day": reader.get_day_data() if self.need_daily_output else None,
            "season": reader.get_season_data() if self.need_seasonal_output else None,
            "harvests": (
                reader.get_harvests_data() if self.need_harvest_output else None
            ),
            "evaluation": {
                "biomass": (
                    reader.merge_biomass_evaluation()
                    if self.need_evaluation_output
                    else None
                ),
                "statistics": (
                    reader.get_evaluation_statistics(assessment_type="biomass")
                    if self.need_evaluation_output
                    else None
                ),
            },
        }

        print(f"Results successfully parsed")

    def save_results(self, output_path=None):
        """Save results to the specified output directory"""
        if not self.results:
            raise ValueError("No results available. Run the simulation first.")

        # Use the specified output path or default to working_dir/results
        output_dir = output_path or os.path.join(self.working_dir, "results")
        os.makedirs(output_dir, exist_ok=True)

        print(f"Saving results to: {output_dir}")

        # Save daily results (handling both single DataFrame and dictionary of DataFrames)
        if self.results["day"] is not None:
            if isinstance(self.results["day"], dict):
                # For multiple runs, save each run to a separate file
                for run_num, df in self.results["day"].items():
                    run_file = os.path.join(
                        output_dir, f"daily_results_run_{run_num}.csv"
                    )
                    df.to_csv(run_file, index=False)

                # Also save a combined version if desired
                from pandas import concat

                all_runs = []
                for run_num, df in self.results["day"].items():
                    df_copy = df.copy()
                    df_copy["Run"] = run_num
                    all_runs.append(df_copy)

                if all_runs:
                    combined_df = concat(all_runs, ignore_index=True)
                    combined_df.to_csv(
                        os.path.join(output_dir, "daily_results_all_runs.csv"),
                        index=False,
                    )
            else:
                # Single DataFrame case (original behavior)
                self.results["day"].to_csv(
                    os.path.join(output_dir, "daily_results.csv"), index=False
                )

        # Handle other result types similarly...
        if self.results["season"] is not None:
            self.results["season"].to_csv(
                os.path.join(output_dir, "seasonal_results.csv"), index=False
            )

        if self.results["harvests"] is not None:
            if isinstance(self.results["harvests"], dict):
                # For multiple runs, save each run to a separate file
                for run_num, df in self.results["harvests"].items():
                    run_file = os.path.join(
                        output_dir, f"harvest_results_run_{run_num}.csv"
                    )
                    df.to_csv(run_file, index=False)

                # Also save a combined version
                all_runs = []
                for run_num, df in self.results["harvests"].items():
                    df_copy = df.copy()
                    df_copy["Run"] = run_num
                    all_runs.append(df_copy)

                if all_runs:
                    from pandas import concat

                    combined_df = concat(all_runs, ignore_index=True)
                    combined_df.to_csv(
                        os.path.join(output_dir, "harvest_results_all_runs.csv"),
                        index=False,
                    )
            else:
                # Single DataFrame case
                self.results["harvests"].to_csv(
                    os.path.join(output_dir, "harvest_results.csv"), index=False
                )

        if self.results["evaluation"]["biomass"] is not None:
            if isinstance(self.results["evaluation"]["biomass"], dict):
                # For multiple runs, save each run to a separate file
                for run_num, df in self.results["evaluation"]["biomass"].items():
                    run_file = os.path.join(
                        output_dir, f"evaluation_biomass_run_{run_num}.csv"
                    )
                    df.to_csv(run_file, index=False)

                # Also save a combined version
                all_runs = []
                for run_num, df in self.results["evaluation"]["biomass"].items():
                    df_copy = df.copy()
                    df_copy["Run"] = run_num
                    all_runs.append(df_copy)

                if all_runs:
                    from pandas import concat

                    combined_df = concat(all_runs, ignore_index=True)
                    combined_df.to_csv(
                        os.path.join(output_dir, "evaluation_biomass_all_runs.csv"),
                        index=False,
                    )
            else:
                # Single DataFrame case
                self.results["evaluation"]["biomass"].to_csv(
                    os.path.join(output_dir, "evaluation_biomass.csv"), index=False
                )

        # Save statistics as JSON
        if self.results["evaluation"]["statistics"] is not None:
            import json

            with open(os.path.join(output_dir, "evaluation_statistics.json"), "w") as f:
                json.dump(self.results["evaluation"]["statistics"], f, indent=2)

        print(f"Results successfully saved")
        return output_dir
