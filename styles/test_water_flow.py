"""
water Flow Project

Enhancement:
This program defines constants for the physical properties of water
and Earth instead of repeating numbers inside the functions. It also
includes a function that converts the final water pressure from
kilopascals (kPa) to pounds per square inch (psi) and displays both
values.
"""

# Physical constants
EARTH_ACCELERATION_OF_GRAVITY = 9.8066500
WATER_DENSITY = 998.2000000
WATER_DYNAMIC_VISCOSITY = 0.0010016


def water_column_height(tower_height, tank_height):
    """
    Calculate the height of the water column.

    Parameters:
        tower_height: Height of the water tower in meters.
        tank_height: Height of the tank walls in meters.

    Returns:
        Height of the water column in meters.
    """
    water_height = tower_height + (3 * tank_height / 4)
    return water_height


def pressure_gain_from_water_height(height):
    """
    Calculate the pressure gain from the height of the water.

    Parameters:
        height: Height of the water column in meters.

    Returns:
        Pressure gain in kilopascals.
    """
    pressure = (
        WATER_DENSITY
        * EARTH_ACCELERATION_OF_GRAVITY
        * height
        / 1000
    )
    return pressure


def pressure_loss_from_pipe(
    pipe_diameter,
    pipe_length,
    friction_factor,
    fluid_velocity
):
    """
    Calculate the pressure loss caused by friction in a pipe.

    Parameters:
        pipe_diameter: Inside diameter of the pipe in meters.
        pipe_length: Length of the pipe in meters.
        friction_factor: Friction factor of the pipe.
        fluid_velocity: Velocity of the water in meters per second.

    Returns:
        Pressure loss in kilopascals.
    """
    pressure_loss = (
        -friction_factor
        * pipe_length
        * WATER_DENSITY
        * fluid_velocity ** 2
        / (2000 * pipe_diameter)
    )
    return pressure_loss


def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """
    Calculate pressure loss caused by pipe fittings.

    Parameters:
        fluid_velocity: Velocity of the water in meters per second.
        quantity_fittings: Number of fittings in the pipe.

    Returns:
        Pressure loss in kilopascals.
    """
    pressure_loss = (
        -0.04
        * WATER_DENSITY
        * fluid_velocity ** 2
        * quantity_fittings
        / 2000
    )
    return pressure_loss


def reynolds_number(hydraulic_diameter, fluid_velocity):
    """
    Calculate the Reynolds number.

    Parameters:
        hydraulic_diameter: Hydraulic diameter of the pipe in meters.
        fluid_velocity: Velocity of the water in meters per second.

    Returns:
        Reynolds number.
    """
    reynolds = (
        WATER_DENSITY
        * hydraulic_diameter
        * fluid_velocity
        / WATER_DYNAMIC_VISCOSITY
    )
    return reynolds


def pressure_loss_from_pipe_reduction(
    larger_diameter,
    fluid_velocity,
    reynolds_number,
    smaller_diameter
):
    """
    Calculate pressure loss caused by a pipe diameter reduction.

    Parameters:
        larger_diameter: Diameter of the larger pipe in meters.
        fluid_velocity: Water velocity in meters per second.
        reynolds_number: Reynolds number of the water flow.
        smaller_diameter: Diameter of the smaller pipe in meters.

    Returns:
        Pressure loss in kilopascals.
    """
    k = (
        0.1
        + 50 / reynolds_number
    ) * (larger_diameter / smaller_diameter) ** 4 - 1

    pressure_loss = (
        -k
        * WATER_DENSITY
        * fluid_velocity ** 2
        / 2000
    )

    return pressure_loss


def pressure_kpa_to_psi(pressure_kpa):
    """
    Convert pressure from kilopascals to pounds per square inch.

    Parameters:
        pressure_kpa: Pressure in kilopascals.

    Returns:
        Pressure in pounds per square inch.
    """
    pressure_psi = pressure_kpa * 0.1450377377
    return pressure_psi


def main():
    """Run the water flow pressure calculation program."""

    tower_height = float(
        input("Height of water tower (meters): ")
    )

    tank_height = float(
        input("Height of water tank walls (meters): ")
    )

    supply_pipe_length = float(
        input("Length of supply pipe from tank to lot (meters): ")
    )

    fittings = int(
        input("Number of 90° angles in supply pipe: ")
    )

    house_pipe_length = float(
        input("Length of pipe from supply to house (meters): ")
    )

    # Pipe dimensions and flow properties
    pipe_diameter = 0.28687
    pipe_reduction_diameter = 0.048692
    friction_factor = 0.013
    fluid_velocity = 1.65

    # Calculate the water column height.
    water_height = water_column_height(
        tower_height,
        tank_height
    )

    # Calculate pressure gained from water height.
    pressure = pressure_gain_from_water_height(
        water_height
    )

    # Calculate pressure loss from the supply pipe.
    pressure += pressure_loss_from_pipe(
        pipe_diameter,
        supply_pipe_length,
        friction_factor,
        fluid_velocity
    )

    # Calculate pressure loss from fittings.
    pressure += pressure_loss_from_fittings(
        fluid_velocity,
        fittings
    )

    # Calculate Reynolds number.
    reynolds = reynolds_number(
        pipe_diameter,
        fluid_velocity
    )

    # Calculate pressure loss from the pipe reduction.
    pressure += pressure_loss_from_pipe_reduction(
        pipe_diameter,
        fluid_velocity,
        reynolds,
        pipe_reduction_diameter
    )

    # Calculate pressure loss from the pipe going to the house.
    pressure += pressure_loss_from_pipe(
        pipe_reduction_diameter,
        house_pipe_length,
        friction_factor,
        fluid_velocity
    )

    # Convert final pressure to psi.
    pressure_psi = pressure_kpa_to_psi(pressure)

    print(f"Pressure at house: {pressure:.1f} kilopascals")
    print(f"Pressure at house: {pressure_psi:.1f} psi")


if __name__ == "__main__":
    main()