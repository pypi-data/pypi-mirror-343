import os


# Helper function to find data files with correct path
def get_data_file_path(filename):
    """Get the full path to a data file, trying several possible locations"""
    # Try relative to the templates directory first
    templates_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(templates_dir, "data", filename),  # ./templates/data/
        os.path.join(
            templates_dir, "../templates/data", filename
        ),  # ../templates/data/
        os.path.join(os.getcwd(), "aquacrop/templates/data", filename),  # from cwd
        os.path.join(os.getcwd(), "templates/data", filename),  # from cwd
        os.path.join(os.getcwd(), "data", filename),  # from cwd
        os.path.join("./data", filename),  # relative to running script
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # If not found, return the first path (which will fail but with a clear error)
    print(
        f"Warning: Could not find data file {filename}. Tried paths: {possible_paths}"
    )
    return possible_paths[0]


# Load weather data from data files with robust path finding
def load_ottawa_weather():
    # Parse temperature data
    temperatures = []
    try:
        temp_path = get_data_file_path("Ottawa.Tnx")
        with open(temp_path, "r") as f:
            lines = f.readlines()
            data_started = False
            for line in lines:
                if data_started and line.strip():
                    # Handle both tab-delimited and space-delimited formats
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        try:
                            tmin = float(parts[0])
                            tmax = float(parts[1])
                            temperatures.append((tmin, tmax))
                        except (ValueError, IndexError):
                            pass
                elif "========================" in line:
                    data_started = True
    except Exception as e:
        print(f"Warning: Could not load temperature data: {e}")
        # Provide default temperature data
        temperatures = [
            (10.5, 22.3),
            (11.2, 23.1),
            (9.8, 21.5),
            (12.4, 24.6),
            (13.1, 25.2),
            (11.7, 23.8),
            (10.9, 22.5),
            (12.2, 24.1),
            (13.5, 26.0),
            (12.8, 25.3),
            (11.5, 23.2),
            (10.2, 21.8),
            (9.5, 20.4),
            (11.0, 22.7),
            (12.5, 24.8),
            (13.8, 26.5),
        ]

    # Parse ETo data
    eto_values = []
    try:
        eto_path = get_data_file_path("Ottawa.ETo")
        with open(eto_path, "r") as f:
            lines = f.readlines()
            data_started = False
            for line in lines:
                if data_started and line.strip():
                    try:
                        eto = float(line.strip())
                        eto_values.append(eto)
                    except ValueError:
                        pass
                elif "=======================" in line:
                    data_started = True
    except Exception as e:
        print(f"Warning: Could not load ETo data: {e}")
        # Provide default ETo data
        eto_values = [
            3.5,
            3.8,
            2.9,
            3.2,
            3.7,
            4.1,
            3.9,
            3.6,
            3.3,
            3.6,
            2.8,
            2.5,
            3.0,
            3.4,
            3.8,
            4.2,
        ]

    # Parse rainfall data
    rainfall_values = []
    try:
        rain_path = get_data_file_path("Ottawa.PLU")
        with open(rain_path, "r") as f:
            lines = f.readlines()
            data_started = False
            for line in lines:
                if data_started and line.strip():
                    try:
                        rain = float(line.strip())
                        rainfall_values.append(rain)
                    except ValueError:
                        pass
                elif "=======================" in line:
                    data_started = True
    except Exception as e:
        print(f"Warning: Could not load rainfall data: {e}")
        # Provide default rainfall data
        rainfall_values = [
            0.0,
            5.2,
            12.4,
            0.0,
            0.0,
            7.6,
            3.1,
            0.0,
            0.0,
            0.0,
            15.8,
            22.5,
            4.3,
            0.0,
            0.0,
            5.2,
        ]

    print(
        f"Loaded data sizes: Temperatures={len(temperatures)}, ETo={len(eto_values)}, Rain={len(rainfall_values)}"
    )

    # Return the complete datasets without subsetting
    return temperatures, eto_values, rainfall_values


# Define CO2 concentration records matching MaunaLoa.CO2
manuloa_co2_records = [
    (1902, 297.4),
    (1905, 298.2),
    (1912, 300.7),
    (1915, 301.3),
    (1924, 304.5),
    (1926, 305.0),
    (1929, 305.2),
    (1932, 307.8),
    (1934, 309.2),
    (1936, 307.9),
    (1938, 310.5),
    (1939, 310.1),
    (1940, 310.5),
    (1944, 309.7),
    (1948, 310.7),
    (1953, 311.9),
    (1954, 314.1),
    (1958, 315.29),
    (1959, 315.98),
    (1960, 316.91),
    (1961, 317.64),
    (1962, 318.45),
    (1963, 318.99),
    (1964, 319.62),
    (1965, 320.04),
    (1966, 321.37),
    (1967, 322.18),
    (1968, 323.05),
    (1969, 324.62),
    (1970, 325.68),
    (1971, 326.32),
    (1972, 327.46),
    (1973, 329.68),
    (1974, 330.19),
    (1975, 331.12),
    (1976, 332.03),
    (1977, 333.84),
    (1978, 335.41),
    (1979, 336.84),
    (1980, 338.76),
    (1981, 340.12),
    (1982, 341.48),
    (1983, 343.15),
    (1984, 344.85),
    (1985, 346.35),
    (1986, 347.61),
    (1987, 349.31),
    (1988, 351.69),
    (1989, 353.2),
    (1990, 354.45),
    (1991, 355.7),
    (1992, 356.54),
    (1993, 357.21),
    (1994, 358.96),
    (1995, 360.97),
    (1996, 362.74),
    (1997, 363.88),
    (1998, 366.84),
    (1999, 368.54),
    (2000, 369.71),
    (2001, 371.32),
    (2002, 373.45),
    (2003, 375.98),
    (2004, 377.7),
    (2005, 379.98),
    (2006, 382.09),
    (2007, 384.02),
    (2008, 385.83),
    (2009, 387.64),
    (2010, 390.1),
    (2011, 391.85),
    (2012, 394.06),
    (2013, 396.74),
    (2014, 398.82),
    (2015, 401.02),
    (2016, 404.41),
    (2017, 406.77),
    (2018, 408.72),
    (2019, 411.66),
    (2020, 414.21),
    (2021, 416.41),
    (2022, 418.53),
    (2023, 421.08),
    (2025, 425.08),
    (2099, 573.08),
]

# Load weather data
ottawa_temperatures, ottawa_eto, ottawa_rain = load_ottawa_weather()
