import os
from typing import List, Dict, Any, Tuple, Optional
from aquacrop.file_generators.DATA.cli_generator import generate_climate_file
from aquacrop.file_generators.DATA.tnx_generator import generate_temperature_file
from aquacrop.file_generators.DATA.eto_generator import generate_eto_file
from aquacrop.file_generators.DATA.plu_generator import generate_rainfall_file
from aquacrop.file_generators.DATA.co2_generator import generate_co2_file

class Weather:
    """
    Represents weather data for AquaCrop simulation including temperature, ETo,
    rainfall and CO2 concentration
    """
    def __init__(self, location: str, 
                 temperatures: List[Tuple[float, float]],  # List of (tmin, tmax) tuples
                 eto_values: List[float],                 # List of ET0 values (mm/day)
                 rainfall_values: List[float],            # List of rainfall values (mm)
                 record_type: int = 1,                    # 1=daily, 2=10-daily, 3=monthly
                 first_day: int = 1,
                 first_month: int = 1,
                 first_year: int = 2014,
                 co2_records: Optional[List[Tuple[int, float]]] = None):  # List of (year, co2_ppm) tuples
        """
        Initialize a weather entity
        
        Args:
            location: Location name
            temperatures: List of (tmin, tmax) tuples in °C
            eto_values: List of reference evapotranspiration values in mm/day
            rainfall_values: List of rainfall values in mm
            record_type: Time step of records (1=daily, 2=10-daily, 3=monthly)
            first_day: First day of record
            first_month: First month of record
            first_year: First year of record
            co2_records: Optional list of (year, CO2 concentration) tuples
        """
        self.location = location
        self.temperatures = temperatures
        self.eto_values = eto_values
        self.rainfall_values = rainfall_values
        self.record_type = record_type
        self.first_day = first_day
        self.first_month = first_month
        self.first_year = first_year
        self.co2_records = co2_records
        
    def generate_files(self, directory: str) -> Dict[str, str]:
        """Generate all weather-related files in directory and return file paths"""
        # Generate temperature file
        tnx_file = generate_temperature_file(
            file_path=f"{directory}/{self.location}.Tnx",
            location=self.location,
            temperatures=self.temperatures,
            record_type=self.record_type,
            first_day=self.first_day,
            first_month=self.first_month,
            first_year=self.first_year
        )
        
        # Generate ETo file
        eto_file = generate_eto_file(
            file_path=f"{directory}/{self.location}.ETo",
            location=self.location,
            eto_values=self.eto_values,
            record_type=self.record_type,
            first_day=self.first_day,
            first_month=self.first_month,
            first_year=self.first_year
        )
        
        # Generate rainfall file
        plu_file = generate_rainfall_file(
            file_path=f"{directory}/{self.location}.PLU",
            location=self.location,
            rainfall_values=self.rainfall_values,
            record_type=self.record_type,
            first_day=self.first_day,
            first_month=self.first_month,
            first_year=self.first_year
        )
        
        # Generate CO2 file
        # TODO: This is a fortran bug, we need to call the file MaunaLoa.CO2
        parent_directory = directory.split("/")[:-1]
        co2_directory = os.path.join(os.path.dirname(directory), "SIMUL")

        
        co2_file = generate_co2_file(
            file_path=os.path.join(co2_directory, "MaunaLoa.CO2"),
            description=f"CO2 concentration for {self.location}",
            records=self.co2_records
        )
        
        # Generate climate file that references the other files
        cli_file = generate_climate_file(
            file_path=f"{directory}/{self.location}.CLI",
            location=self.location,
            tnx_file=f"{self.location}.Tnx",
            eto_file=f"{self.location}.ETo",
            plu_file=f"{self.location}.PLU",
            co2_file=f"MaunaLoa.CO2" # TODO: This is an error in the fortran code so we must call it like this
        )
        
        return {
            'climate': cli_file,
            'temperature': tnx_file,
            'eto': eto_file,
            'rainfall': plu_file,
            'co2': co2_file
        }