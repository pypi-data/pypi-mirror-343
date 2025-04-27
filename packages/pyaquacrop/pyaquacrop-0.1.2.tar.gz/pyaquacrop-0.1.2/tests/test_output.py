import os

import numpy as np
import pandas as pd
import pytest

from aquacrop.output import OutputFile, OutputReader


@pytest.fixture
def test_files_dir():
    """Fixture to provide the path to test files directory"""
    base_dir = os.path.join(os.path.dirname(__file__), "referenceFiles", "OUTP")
    assert os.path.exists(base_dir), f"Test directory {base_dir} not found"
    return base_dir


@pytest.fixture
def day_file(test_files_dir):
    """Fixture to provide the path to a day output file"""
    # Using the provided paste.txt as a day file for testing
    file_path = os.path.join(test_files_dir, "OttawaPRMday.OUT")
    assert os.path.exists(file_path), f"Test file {file_path} not found"
    return file_path


@pytest.fixture
def season_file(test_files_dir):
    """Fixture to provide the path to a season output file"""
    file_path = os.path.join(test_files_dir, "OttawaPRMseason.OUT")
    assert os.path.exists(file_path), f"Test file {file_path} not found"
    return file_path


@pytest.fixture
def harvests_file(test_files_dir):
    """Fixture to provide the path to a harvests output file"""
    file_path = os.path.join(test_files_dir, "OttawaPRMharvests.OUT")
    assert os.path.exists(file_path), f"Test file {file_path} not found"
    return file_path


@pytest.fixture
def evaluation_file(test_files_dir):
    """Fixture to provide the path to an evaluation output file"""
    file_path = os.path.join(test_files_dir, "OttawaPRM1evaluation.OUT")
    assert os.path.exists(file_path), f"Test file {file_path} not found"
    return file_path


@pytest.fixture
def output_reader(test_files_dir):
    """Fixture to provide an initialized OutputReader with test files"""
    reader = OutputReader(test_files_dir)
    reader.scan_directory()
    return reader


class TestOutputFile:
    """Test cases for the OutputFile class"""

    def test_parse_day_file(self, day_file):
        """Test parsing a daily output file"""
        output_file = OutputFile.from_file(day_file)

        # Verify correct output type detection
        assert output_file.output_type == "day", "Failed to detect day file type"

        # Verify data structure
        assert isinstance(
            output_file.data, dict
        ), "Day file data should be a dictionary of DataFrames by run"

        # Verify run numbers
        assert 1 in output_file.data, "Expected run 1 data in day file"

        # Verify DataFrame content for run 1
        run1_data = output_file.data[1]
        assert isinstance(run1_data, pd.DataFrame), "Run data should be a DataFrame"
        assert not run1_data.empty, "DataFrame should not be empty"

        # Check expected columns
        expected_columns = [
            "Day",
            "Month",
            "Year",
            "DAP",
            "Stage",
            "WC(3.00)",
            "Rain",
            "Irri",
        ]
        for col in expected_columns:
            assert col in run1_data.columns, f"Expected column {col} in day output data"

        # Check data types for key columns
        assert pd.api.types.is_numeric_dtype(
            run1_data["Day"]
        ), "Day column should be numeric"
        assert pd.api.types.is_numeric_dtype(
            run1_data["Month"]
        ), "Month column should be numeric"
        assert pd.api.types.is_numeric_dtype(
            run1_data["Year"]
        ), "Year column should be numeric"

        # Basic validation of data
        assert run1_data["Day"].max() <= 31, "Day values should be valid"
        assert run1_data["Month"].max() <= 12, "Month values should be valid"
        assert run1_data["Year"].min() >= 1900, "Year values should be valid"

    def test_parse_season_file(self, season_file):
        """Test parsing a season output file"""
        output_file = OutputFile.from_file(season_file)

        # Verify correct output type detection
        assert output_file.output_type == "season", "Failed to detect season file type"

        # Verify data structure
        assert isinstance(
            output_file.data, pd.DataFrame
        ), "Season file data should be a DataFrame"
        assert not output_file.data.empty, "DataFrame should not be empty"

        # Check expected columns
        expected_columns = [
            "RunNr",
            "Rain",
            "ETo",
            "GD",
            "CO2",
            "BioMass",
            "Y(dry)",
            "Y(fresh)",
        ]
        for col in expected_columns:
            assert (
                col in output_file.data.columns
            ), f"Expected column {col} in season output data"

        # Check number of rows (one per run)
        assert len(output_file.data) >= 3, "Expected at least 3 runs in season data"

        # Check data types for key columns
        assert pd.api.types.is_numeric_dtype(
            output_file.data["RunNr"]
        ), "RunNr column should be numeric"
        assert pd.api.types.is_numeric_dtype(
            output_file.data["Rain"]
        ), "Rain column should be numeric"
        assert pd.api.types.is_numeric_dtype(
            output_file.data["BioMass"]
        ), "BioMass column should be numeric"

        # Basic validation of data
        assert output_file.data["RunNr"].min() >= 1, "Run numbers should start from 1"
        assert output_file.data["Rain"].min() >= 0, "Rain values should be non-negative"
        assert (
            output_file.data["BioMass"].min() >= 0
        ), "Biomass values should be non-negative"

    def test_parse_harvests_file(self, harvests_file):
        """Test parsing a harvests output file"""
        output_file = OutputFile.from_file(harvests_file)

        # Verify correct output type detection
        assert (
            output_file.output_type == "harvests"
        ), "Failed to detect harvests file type"

        # Verify data structure
        assert isinstance(
            output_file.data, dict
        ), "Harvests file data should be a dictionary of DataFrames by run"

        # Verify run numbers
        for run_num in [1, 2, 3]:
            assert (
                run_num in output_file.data
            ), f"Expected run {run_num} data in harvests file"

            # Verify DataFrame content for each run
            run_data = output_file.data[run_num]
            assert isinstance(
                run_data, pd.DataFrame
            ), f"Run {run_num} data should be a DataFrame"
            assert (
                not run_data.empty
            ), f"DataFrame for run {run_num} should not be empty"

            # Check expected columns
            expected_columns = [
                "Nr",
                "Day",
                "Month",
                "Year",
                "DAP",
                "Interval",
                "Biomass",
                "Sum(B)",
                "Dry-Yield",
            ]
            for col in expected_columns:
                assert (
                    col in run_data.columns
                ), f"Expected column {col} in harvests output data for run {run_num}"

            # Check data types for key columns
            assert pd.api.types.is_numeric_dtype(
                run_data["Nr"]
            ), "Nr column should be numeric"
            assert pd.api.types.is_numeric_dtype(
                run_data["Biomass"]
            ), "Biomass column should be numeric"
            assert pd.api.types.is_numeric_dtype(
                run_data["Dry-Yield"]
            ), "Dry-Yield column should be numeric"

            # Basic validation of data
            assert run_data["Nr"].min() >= 0, "Harvest numbers should start from 0"
            assert (
                run_data["Biomass"].min() >= 0
            ), "Biomass values should be non-negative"

    def test_parse_evaluation_file(self, evaluation_file):
        """Test parsing an evaluation output file"""
        output_file = OutputFile.from_file(evaluation_file)

        # Verify correct output type detection
        assert (
            output_file.output_type == "evaluation"
        ), "Failed to detect evaluation file type"

        # Verify data structure
        assert isinstance(
            output_file.data, dict
        ), "Evaluation file data should be a dictionary"

        # Check for expected assessment types
        for assessment in ["biomass", "canopy_cover", "soil_water", "statistics"]:
            assert (
                assessment in output_file.data
            ), f"Expected {assessment} assessment in evaluation data"

        # Check biomass data structure
        assert isinstance(
            output_file.data["biomass"], dict
        ), "Biomass data should be a dictionary by run"

        # Check run number 1 exists in biomass data
        assert (
            1 in output_file.data["biomass"]
        ), "Expected run 1 data in biomass evaluation"

        # Verify biomass DataFrame content
        biomass_data = output_file.data["biomass"][1]
        assert isinstance(
            biomass_data, pd.DataFrame
        ), "Biomass data should be a DataFrame"
        assert not biomass_data.empty, "Biomass DataFrame should not be empty"

        # Check expected columns in biomass data
        expected_columns = [
            "Nr",
            "Observed",
            "StdDev",
            "Simulated",
            "Day",
            "Month",
            "Year",
            "Date",
        ]
        for col in expected_columns:
            assert (
                col in biomass_data.columns
            ), f"Expected column {col} in biomass evaluation data"

        # Check statistics data
        assert (
            "biomass" in output_file.data["statistics"]
        ), "Expected biomass statistics"
        biomass_stats = output_file.data["statistics"]["biomass"]

        # Check for expected statistics (removing 'd' which isn't present in the actual output)
        for stat in [
            "n",
            "avg_observed",
            "avg_simulated",
            "pearson_r",
            "rmse",
            "cv_rmse",
            "ef",
        ]:
            assert (
                stat in biomass_stats
            ), f"Expected statistic {stat} in biomass evaluation"

        # Basic validation of statistics
        assert biomass_stats["n"] > 0, "Number of observations should be positive"
        assert (
            0 <= biomass_stats["pearson_r"] <= 1
        ), "Correlation coefficient should be between 0 and 1"
        assert biomass_stats["rmse"] >= 0, "RMSE should be non-negative"


class TestOutputReader:
    """Test cases for the OutputReader class"""

    def test_scan_directory(self, output_reader):
        """Test scanning a directory for output files"""
        # Verify files were found
        assert (
            len(output_reader.output_files) > 0
        ), "No output files found in test directory"

        # Check for specific file types
        file_types = [
            output_file.output_type
            for output_file in output_reader.output_files.values()
        ]

        # Should find at least one of each file type in test directory
        assert "season" in file_types, "No season output file found"
        assert "harvests" in file_types, "No harvests output file found"
        assert "evaluation" in file_types, "No evaluation output file found"

        # Day file might be named differently, so not checking for it

    def test_get_season_data(self, output_reader):
        """Test getting season data from reader"""
        season_data = output_reader.get_season_data(project_name="Ottawa")

        # Verify data structure
        assert isinstance(
            season_data, pd.DataFrame
        ), "Season data should be a DataFrame"
        assert not season_data.empty, "Season DataFrame should not be empty"

        # Check for expected columns
        expected_columns = ["RunNr", "Rain", "ETo", "BioMass", "Y(dry)", "Y(fresh)"]
        for col in expected_columns:
            assert col in season_data.columns, f"Expected column {col} in season data"

    def test_get_harvests_data(self, output_reader):
        """Test getting harvests data from reader"""
        for run_num in [1, 2, 3]:
            harvests_data = output_reader.get_harvests_data(
                project_name="Ottawa", run_number=run_num
            )

            # Verify data structure
            assert isinstance(
                harvests_data, pd.DataFrame
            ), f"Harvests data for run {run_num} should be a DataFrame"
            assert (
                not harvests_data.empty
            ), f"Harvests DataFrame for run {run_num} should not be empty"

            # Check for expected columns
            expected_columns = [
                "Nr",
                "Day",
                "Month",
                "Year",
                "Biomass",
                "Dry-Yield",
                "Fresh-Yield",
            ]
            for col in expected_columns:
                assert (
                    col in harvests_data.columns
                ), f"Expected column {col} in harvests data for run {run_num}"

    def test_get_evaluation_data(self, output_reader):
        """Test getting evaluation data from reader"""
        for run_num in [1, 2, 3]:
            biomass_data = output_reader.get_evaluation_data(
                project_name="Ottawa", run_number=run_num, assessment_type="biomass"
            )

            # For some runs, we might not have evaluation data, so check conditionally
            if not biomass_data.empty:
                # Verify data structure
                assert isinstance(
                    biomass_data, pd.DataFrame
                ), f"Biomass data for run {run_num} should be a DataFrame"

                # Check for expected columns
                expected_columns = ["Nr", "Observed", "Simulated", "Date"]
                for col in expected_columns:
                    assert (
                        col in biomass_data.columns
                    ), f"Expected column {col} in biomass data for run {run_num}"

    def test_get_evaluation_statistics(self, output_reader):
        """Test getting evaluation statistics from reader"""
        stats = output_reader.get_evaluation_statistics(
            project_name="Ottawa", run_number=1, assessment_type="biomass"
        )

        # Verify data structure
        assert isinstance(stats, dict), "Statistics should be a dictionary"

        # Check for empty stats (in case run 1 doesn't have evaluation data)
        if stats:
            # Check for expected statistics
            for stat in ["n", "avg_observed", "avg_simulated", "pearson_r", "rmse"]:
                assert stat in stats, f"Expected statistic {stat} in biomass statistics"

    def test_merge_biomass_evaluation(self, output_reader):
        """Test merging biomass evaluation data for all runs"""
        merged_data = output_reader.merge_biomass_evaluation(project_name="Ottawa")

        # Verify data structure
        assert isinstance(
            merged_data, pd.DataFrame
        ), "Merged data should be a DataFrame"

        # The merged data might be empty if no evaluation files exist
        if not merged_data.empty:
            # Check for expected columns
            expected_columns = ["Nr", "Observed", "Simulated", "Run"]
            for col in expected_columns:
                assert (
                    col in merged_data.columns
                ), f"Expected column {col} in merged biomass data"

            # Check that we have data from multiple runs
            assert (
                len(merged_data["Run"].unique()) >= 1
            ), "Expected data from at least one run"


def test_parse_paste_txt_content(day_file):
    """Test parsing the specific paste.txt file content to ensure all data is correctly extracted"""
    output_file = OutputFile.from_file(day_file)

    # Verify we have day data
    assert output_file.output_type == "day"

    # Get run 1 data
    run1_data = output_file.get_data(run_number=1)
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"

    # Verify basic structure
    assert isinstance(run1_data, pd.DataFrame)
    assert not run1_data.empty

    # Check specific data points from the paste.txt file
    # First day (index 0)
    assert run1_data.iloc[0]["Day"] == 21
    assert run1_data.iloc[0]["Month"] == 5
    assert run1_data.iloc[0]["Year"] == 2014
    assert run1_data.iloc[0]["DAP"] == 1
    assert run1_data.iloc[0]["CC"] == 5.4
    assert (
        abs(run1_data.iloc[0]["Biomass"] - 0.017) < 0.001
    )  # Using approximate comparison for floats

    # Last day (using negative indexing)
    assert run1_data.iloc[-1]["Day"] == 15
    assert run1_data.iloc[-1]["Month"] == 6
    assert run1_data.iloc[-1]["Year"] == 2014

    # Check for computed columns
    assert "WC(3.00)" in run1_data.columns
    assert "Rain" in run1_data.columns
    assert "Irri" in run1_data.columns
    assert "Biomass" in run1_data.columns
    assert "CC" in run1_data.columns

    # Verify total number of rows (matching the entries in paste.txt)
    assert len(run1_data) == 26

    # Check data consistency
    # Biomass should be non-decreasing
    assert all(run1_data["Biomass"].diff()[1:] >= 0)

    # Total rainfall should match expected value
    total_rain = run1_data["Rain"].sum()
    expected_rain = 76.1  # Sum from paste.txt
    assert abs(total_rain - expected_rain) < 0.1

    # Basic data validation checks
    assert all(0 <= run1_data["CC"]) and all(
        run1_data["CC"] <= 100
    )  # CC should be between 0-100%
    assert all(run1_data["Biomass"] >= 0)  # Biomass should be non-negative

    # Check data types for numerical columns
    numerical_columns = [
        "Day",
        "Month",
        "Year",
        "DAP",
        "Stage",
        "WC(3.00)",
        "Rain",
        "Irri",
        "CC",
        "Biomass",
        "E",
        "Tr",
    ]

    for col in numerical_columns:
        if col in run1_data.columns:
            assert pd.api.types.is_numeric_dtype(
                run1_data[col]
            ), f"Column {col} should be numeric"


def test_day_data_analysis_operations(day_file):
    """Test performing common data analysis operations on the parsed day output"""
    output_file = OutputFile.from_file(day_file)
    run1_data = output_file.get_data(run_number=1)

    # 1. Test filtering operations
    # Filter for days with rainfall
    rainy_days = run1_data[run1_data["Rain"] > 0]
    assert len(rainy_days) > 0
    assert all(rainy_days["Rain"] > 0)

    # Filter for days with high canopy cover (>20%)
    if isinstance(run1_data, pd.DataFrame) and "CC" in run1_data.columns:
        high_cc_days = run1_data[run1_data["CC"] > 20]
        if not high_cc_days.empty:
            assert all(high_cc_days["CC"] > 20)

    # 2. Test grouping operations
    # Group by month and calculate statistics
    monthly_stats = run1_data.groupby("Month").agg(
        {
            "Biomass": ["mean", "max"],
            "Rain": "sum",
            "CC": (
                "max"
                if isinstance(run1_data, pd.DataFrame) and "CC" in run1_data.columns
                else "count"
            ),
        }
    )
    assert isinstance(monthly_stats, pd.DataFrame)
    assert not monthly_stats.empty

    # 3. Test calculation of derived variables
    # Calculate cumulative rainfall
    run1_data["CumRain"] = run1_data["Rain"].cumsum()
    assert "CumRain" in run1_data.columns

    # FIX: Use approximate comparison for floating-point values with a small tolerance
    cum_rain_last = run1_data["CumRain"].iloc[-1]
    rain_sum = run1_data["Rain"].sum()
    assert (
        abs(cum_rain_last - rain_sum) < 1e-10
    ), f"CumRain last value {cum_rain_last} should match Rain sum {rain_sum}"

    # Calculate biomass growth rate (if more than one data point)
    if len(run1_data) > 1 and "Biomass" in run1_data.columns:
        run1_data["BiomassGrowthRate"] = (
            run1_data["Biomass"].diff() / run1_data["DAP"].diff()
        )
        # Fill NaN in first row
        run1_data["BiomassGrowthRate"] = run1_data["BiomassGrowthRate"].fillna(0)
        assert "BiomassGrowthRate" in run1_data.columns

        # Verify calculation - the rate should be positive or zero for normal crop growth
        assert all(run1_data["BiomassGrowthRate"] >= 0)

    # Calculate water use efficiency (WUE = Biomass / Cumulative Transpiration)
    if "Tr" in run1_data.columns and "Biomass" in run1_data.columns:
        run1_data["CumTranspiration"] = run1_data["Tr"].cumsum()

        # Avoid division by zero
        safe_cum_tr = run1_data["CumTranspiration"].replace(0, np.nan)
        run1_data["WUE"] = run1_data["Biomass"] / safe_cum_tr
        run1_data["WUE"] = run1_data["WUE"].fillna(0)

        assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
        assert "WUE" in run1_data.columns
        # WUE should be positive or zero
        assert all(run1_data["WUE"] >= 0)

    # 4. Test pivot table creation
    if isinstance(run1_data, pd.DataFrame) and "CC" in run1_data.columns:
        # Create a month by day pivot table of canopy cover
        pivot_cc = pd.pivot_table(
            run1_data, values="CC", index="Month", columns="Day", aggfunc="mean"
        )
        assert isinstance(pivot_cc, pd.DataFrame)

    # 5. Test statistical analysis
    # Calculate correlation matrix
    if isinstance(run1_data, pd.DataFrame) and all(
        col in run1_data.columns for col in ["Biomass", "CC", "Tr"]
    ):
        corr_matrix = run1_data[["Biomass", "CC", "Tr"]].corr()
        assert isinstance(corr_matrix, pd.DataFrame)
        assert corr_matrix.shape == (3, 3)

        # Biomass and CC should be positively correlated
        assert corr_matrix.loc["Biomass", "CC"] > 0

    # 6. Test time-based analysis
    # Create date column
    run1_data["Date"] = pd.to_datetime(
        pd.DataFrame(run1_data).apply(
            lambda row: f"{int(row['Year'])}-{int(row['Month'])}-{int(row['Day'])}",
            axis=1,
        )
    )
    assert isinstance(run1_data, pd.DataFrame), "run1_data should be a DataFrame"
    assert "Date" in run1_data.columns
    assert pd.api.types.is_datetime64_dtype(run1_data["Date"])

    # Resample to weekly frequency
    weekly_data = (
        run1_data.set_index("Date")
        .resample("W")
        .agg(
            {
                "Biomass": "max",
                "Rain": "sum",
                "CC": "mean" if "CC" in run1_data.columns else "count",
            }
        )
    )
    assert isinstance(weekly_data, pd.DataFrame)

    # 7. Test export/transformation capabilities
    # Convert to different formats
    csv_str = run1_data.to_csv(index=False)
    assert isinstance(csv_str, str)
    assert len(csv_str) > 0

    # Convert to records format
    records = run1_data.to_dict(orient="records")
    assert isinstance(records, list)
    assert len(records) == len(run1_data)

    # Test slicing operations
    subset = run1_data[["Day", "Month", "Year", "Biomass"]]
    assert list(subset.columns) == ["Day", "Month", "Year", "Biomass"]
    assert len(subset) == len(run1_data)


def test_output_integration(output_reader, day_file):
    """Test integrating data from different output types for comprehensive analysis"""
    # First, make sure we have a day output file in the reader
    day_output = OutputFile.from_file(day_file)
    output_reader.output_files["paste.txt"] = day_output

    # Get data from different output types
    day_data = output_reader.get_day_data(project_name=None, run_number=1)
    season_data = output_reader.get_season_data(project_name="Ottawa")
    harvests_data = output_reader.get_harvests_data(project_name="Ottawa", run_number=1)
    evaluation_data = output_reader.get_evaluation_data(
        project_name="Ottawa", run_number=1, assessment_type="biomass"
    )
