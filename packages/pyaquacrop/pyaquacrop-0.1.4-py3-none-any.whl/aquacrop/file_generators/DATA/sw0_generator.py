"""
Initial conditions file generator for AquaCrop (.SW0 files)
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Union

from aquacrop.constants import Constants


def generate_initial_conditions_file(
    file_path: str,
    description: str,
    # Initial crop conditions
    initial_canopy_cover: float = -9.00,  # -9.00 = default (will be calculated by AquaCrop)
    initial_biomass: float = 0.000,  # Biomass produced before start of simulation (ton/ha)
    initial_rooting_depth: float = -9.00,  # -9.00 = default (will be calculated by AquaCrop)
    # Surface water conditions (if soil bunds present)
    water_layer: float = 0.0,  # Water layer (mm) stored between soil bunds
    water_layer_ec: float = 0.00,  # Electrical conductivity (dS/m) of water layer
    # Soil water content specification method
    soil_water_content_type: int = 0,  # 0: for specific layers, 1: at particular depths
    # Soil water and salinity content data
    soil_data: Optional[List[Dict[str, float]]] = None,
) -> str:
    """
    Generate an AquaCrop initial conditions file (.SW0) with all possible parameters

    Args:
        file_path: Path to write the file
        description: Description of the initial conditions

        # Initial crop conditions
        initial_canopy_cover: Canopy cover (%) at start of simulation period
                            (-9.00 = use maximum possible without water stress)
        initial_biomass: Biomass (ton/ha) produced before the start of the simulation period
        initial_rooting_depth: Effective rooting depth (m) at start of simulation period
                            (-9.00 = use maximum possible without water stress)

        # Surface water conditions (if soil bunds present)
        water_layer: Water layer (mm) stored between soil bunds (if present)
        water_layer_ec: Electrical conductivity (dS/m) of water layer

        # Soil water content specification method
        soil_water_content_type: Method to specify soil water content
                               (0: for specific layers, 1: at particular depths)

        # Soil water and salinity content data
        soil_data: List of dicts with soil data. For type 0 (layers), each dict should have:
                   - 'thickness': Thickness of soil layer (m)
                   - 'water_content': Soil water content (vol%)
                   - 'ec': Soil salinity (ECe) in dS/m
                   For type 1 (depths), each dict should have:
                   - 'depth': Soil depth (m)
                   - 'water_content': Soil water content (vol%)
                   - 'ec': Soil salinity (ECe) in dS/m

    Returns:
        The path to the generated file
    """
    # Initialize soil data if not provided
    if soil_data is None:
        soil_data = []

    # Generate initial conditions file content
    lines = [
        f"{description}",
        f" {Constants.AQUACROP_VERSION_NUMBER} : AquaCrop Version ({Constants.AQUACROP_VERSION_DATE})",
        f"{initial_canopy_cover:.2f} : {'initial canopy cover (%) at start of simulation period' if initial_canopy_cover > 0 else 'initial canopy cover that can be reached without water stress will be used as default'}",
        f"{initial_biomass:.3f} : biomass (ton/ha) produced before the start of the simulation period",
        f"{initial_rooting_depth:.2f} : {'initial effective rooting depth (m)' if initial_rooting_depth > 0 else 'initial effective rooting depth that can be reached without water stress will be used as default'}",
        f"{water_layer:.1f} : water layer (mm) stored between soil bunds (if present)",
        f"{water_layer_ec:.2f} : electrical conductivity (dS/m) of water layer stored between soil bunds (if present)",
        f"{soil_water_content_type} : soil water content specified for {'specific layers' if soil_water_content_type == 0 else 'particular depths'}",
        f"{len(soil_data)} : number of {'layers' if soil_water_content_type == 0 else 'soil depths'} considered",
        f"",
    ]

    # Add soil data table based on type
    if soil_water_content_type == 0:  # For specific layers
        lines.extend(
            [
                f"Thickness layer (m) Water content (vol%) ECe(dS/m)",
                f"==============================================================",
            ]
        )

        # Add soil layer data
        for layer in soil_data:
            lines.append(
                f"{layer['thickness']:.2f} {layer['water_content']:.2f} {layer['ec']:.2f}"
            )

    else:  # For particular depths
        lines.extend(
            [
                f"Soil depth (m) Water content (vol%) ECe (dS/m)",
                f"==============================================================",
            ]
        )

        # Add soil depth data
        for point in soil_data:
            lines.append(
                f"{point['depth']:.2f} {point['water_content']:.2f} {point['ec']:.2f}"
            )

    # Write the content to file
    content = "\n".join(lines)

    if file_path:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)

    return file_path


# Example usage
if __name__ == "__main__":
    # Example 1: Water stored between bunds (Table 2.23u - 2)
    layer_data = [{"thickness": 4.00, "water_content": 43.00, "ec": 0.00}]

    generate_initial_conditions_file(
        file_path="example_water_between_bunds.sw0",
        description="uniform silty soil at saturation with water between soil bunds",
        initial_canopy_cover=-9.00,
        initial_biomass=0.000,
        initial_rooting_depth=-9.00,
        water_layer=150.0,
        water_layer_ec=0.00,
        soil_water_content_type=0,  # For specific layers
        soil_data=layer_data,
    )

    # Example 2: Initial conditions for specific soil layers (Table 2.23u - 3)
    layer_data = [
        {"thickness": 0.40, "water_content": 30.00, "ec": 1.00},
        {"thickness": 0.40, "water_content": 20.00, "ec": 2.00},
        {"thickness": 0.40, "water_content": 18.00, "ec": 2.50},
    ]

    generate_initial_conditions_file(
        file_path="example_soil_layers.sw0",
        description="Soil water and salinity content in Field AZ123 on 21 March 2010",
        initial_canopy_cover=-9.00,
        initial_biomass=0.000,
        initial_rooting_depth=-9.00,
        water_layer=0.0,
        water_layer_ec=0.00,
        soil_water_content_type=0,  # For specific layers
        soil_data=layer_data,
    )

    # Example 3: Initial conditions at particular soil depths (Table 2.23u - 4)
    depth_data = [
        {"depth": 0.10, "water_content": 23.00, "ec": 0.00},
        {"depth": 0.29, "water_content": 15.00, "ec": 0.00},
        {"depth": 0.45, "water_content": 34.00, "ec": 0.00},
        {"depth": 0.66, "water_content": 15.00, "ec": 0.00},
        {"depth": 1.00, "water_content": 10.00, "ec": 0.00},
    ]

    generate_initial_conditions_file(
        file_path="example_soil_depths.sw0",
        description="example with soil water content at particulars depths",
        initial_canopy_cover=-9.00,
        initial_biomass=0.000,
        initial_rooting_depth=-9.00,
        water_layer=0.0,
        water_layer_ec=0.00,
        soil_water_content_type=1,  # At particular depths
        soil_data=depth_data,
    )

    # Example 4: Initial conditions one month after planting (Table 2.23u - 5)
    depth_data = [
        {"depth": 0.10, "water_content": 10.00, "ec": 0.00},
        {"depth": 0.40, "water_content": 15.00, "ec": 0.00},
        {"depth": 0.60, "water_content": 30.00, "ec": 0.00},
        {"depth": 0.80, "water_content": 30.00, "ec": 0.00},
        {"depth": 1.00, "water_content": 33.00, "ec": 0.00},
        {"depth": 1.20, "water_content": 25.00, "ec": 0.00},
    ]

    generate_initial_conditions_file(
        file_path="example_after_planting.sw0",
        description="initial conditions 1 month after planting",
        initial_canopy_cover=31.00,  # Actual value provided
        initial_biomass=0.150,
        initial_rooting_depth=-9.00,
        water_layer=0.0,
        water_layer_ec=0.00,
        soil_water_content_type=1,  # At particular depths
        soil_data=depth_data,
    )
