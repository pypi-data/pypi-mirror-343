from typing import List


def total_energy(energy: List[float], sample_time: int = 60) -> float:
    """
    Calculate the total energy consumption in kilowatt-hours (kWh).

    Args:
        energy (List[float]): A list of power values in watts (W).
        sample_time (int, optional): The time interval between samples in seconds. Defaults to 60.

    Returns:
        float: The total energy consumption in kilowatt-hours (kWh).
    """
    return sum(energy) * sample_time / 3600000  # Convert J to kWh



def total_energy_cost(energy: List[float], price: List[float], sample_time: int = 60) -> float:
    """
    Calculate the total energy cost based on power consumption and price per kWh.

    Args:
        energy (List[float]): A list of power values in watts (W).
        price (List[float]): A list of price values in DKK per kWh.
        sample_time (int, optional): The time interval between samples in seconds. Defaults to 60.

    Returns:
        float: The total energy cost in DKK.
    """
    if len(energy) != len(price):
        raise ValueError("Energy and price lists must have the same length.")
    
    total_cost = sum(e * p for e, p in zip(energy, price)) * (sample_time / 3600000)
    
    return total_cost



def temperature_violations(temperature: List[float], constraint: List[float], 
                           type: str = "lower_bound", sample_time: int = 60) -> float:
    """
    Calculate temperature violations in Kelvin-hours.

    Args:
        temperature (List[float]): A list of recorded temperature values (°C or K).
        constraint (List[float]): A list of temperature constraints (same unit as temperature).
        type (str, optional): "lower_bound" to sum violations below the constraint, 
                              "upper_bound" to sum violations above it. Defaults to "lower_bound".
        sample_time (int, optional): The time interval between samples in seconds. Defaults to 60.

    Returns:
        float: The total temperature violation in Kelvin-hours (K·h).
    """
    if len(temperature) != len(constraint):
        raise ValueError("Temperature and constraint lists must have the same length.")
    
    # Compute constraint minus temperature differences
    violations = [c - t for c, t in zip(constraint, temperature)]
    
    if type == "lower_bound":
        total_violation = sum(v for v in violations if v > 0)  # Sum positive values
    elif type == "upper_bound":
        total_violation = sum(abs(v) for v in violations if v < 0)  # Sum absolute values of negative values
    else:
        raise ValueError("Type must be 'lower_bound' or 'upper_bound'.")
    
    # Scale to Kelvin-hours
    return total_violation * (sample_time / 3600)
