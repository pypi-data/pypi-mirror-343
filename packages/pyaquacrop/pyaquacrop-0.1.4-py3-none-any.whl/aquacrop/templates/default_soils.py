from aquacrop import Soil, SoilLayer

# Ottawa Sandy Loam soil profile based on test reference
ottawa_sandy_loam = Soil(
    name="Ottawa Sandy Loam",
    description="Ottawa, Canada - sandy loam - Field of the Canadian Food Inspection Agency (CFIA)",
    soil_layers=[
        SoilLayer(
            thickness=1.50,
            sat=46.0,
            fc=29.0,
            wp=13.0,
            ksat=1200.0,
            penetrability=100,
            gravel=0,
            cra=-0.390600,
            crb=1.255639,
            description="sandy loam"
        )
    ],
    curve_number=46,
    readily_evaporable_water=7
)

# Generic Sandy soil profile
sandy_soil = Soil(
    name="Sandy Soil",
    description="Generic sandy soil profile",
    soil_layers=[
        SoilLayer(
            thickness=1.20,
            sat=36.0,
            fc=13.0,
            wp=6.0,
            ksat=1500.0,
            penetrability=100,
            gravel=0,
            cra=-0.3906,
            crb=1.2556,
            description="sandy"
        )
    ],
    curve_number=61,
    readily_evaporable_water=8
)

# Generic Loam soil profile
loam_soil = Soil(
    name="Loam Soil",
    description="Generic loam soil profile",
    soil_layers=[
        SoilLayer(
            thickness=1.20,
            sat=46.0,
            fc=31.0,
            wp=15.0,
            ksat=250.0,
            penetrability=100,
            gravel=0,
            cra=-0.3906,
            crb=1.2556,
            description="loam"
        )
    ],
    curve_number=72,
    readily_evaporable_water=10
)

# Generic Clay soil profile
clay_soil = Soil(
    name="Clay Soil",
    description="Generic clay soil profile",
    soil_layers=[
        SoilLayer(
            thickness=1.20,
            sat=50.0,
            fc=39.0,
            wp=27.0,
            ksat=15.0,
            penetrability=100,
            gravel=0,
            cra=-0.3906,
            crb=1.2556,
            description="clay"
        )
    ],
    curve_number=82,
    readily_evaporable_water=12
)