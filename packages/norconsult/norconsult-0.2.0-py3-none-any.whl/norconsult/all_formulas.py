import math
from scipy.optimize import brentq

from .all_simple import area , velocity , flow , reynolds_number

def swamee_jain(diameter, roughness, reynolds_number):
    """
    Calculates the friction factor using the Swamee-Jain equation.

    Parameters:
    - diameter (float): The diameter of the pipe (in mm).
    - ruhet (float): The roughness height of the pipe (in mm).
    - reynolds_number (float): The Reynolds number calculated using the flow rate, diameter, and viscosity.

    Returns:
    - friction_factor (float): The friction factor calculated using the Swamee-Jain equation.

    Formula:
    The Swamee-Jain equation is given by:
    f = 0.25 / (math.log10((ruhet / (3.7 * diameter)) + (5.74 / reynolds_number**0.9))) ** 2

    Note:
    - This equation is used to estimate the friction factor in fully developed turbulent flow in pipes.
    if the flow is laminar, the friction factor is calculated using the Poiseuille's equation.

    - The equation assumes that the flow is turbulent and the pipe is smooth.
    """
    if not isinstance(reynolds_number, (int, float)):
        raise TypeError("Reynolds number must be a number (int or a float)")
    if not isinstance(diameter, (int, float)):
        raise TypeError("Diameter must be a number (int or a float)")
    if not isinstance(roughness, (int, float)):
        raise TypeError("Roughness height (ruhet) must be a number (int or a float)")
 
   
    if reynolds_number < 4000: 
        return 64 / reynolds_number
    else:
        return 0.25 / (math.log10((roughness / (3.7 * diameter)) + (5.74 / reynolds_number ** 0.9)) ** 2)

    
 
    

def darcy_weisbach(frictions_factor, length, diameter, velocity):
    """
    Calculates the Darcy-Weisbach friction factor for fluid flow in a pipe.

    Parameters:
    frictions_factor (float): The friction factor of the pipe.
    length (float): The length of the pipe (in meters).
    diameter (float): The diameter of the pipe (in millimeters).
    velocity (float): The velocity of the fluid flow (in meters per second).

    Returns:
    float: The Darcy-Weisbach friction factor.

    Formula:
    The Darcy-Weisbach friction factor is calculated using the following formula:
    frictions_factor * length * velocity ** 2 / (2 * diameter / 1000 * 9.81)
    """
    return (
        frictions_factor * length * velocity ** 2 / (2 * diameter / 1000 * 9.81)
    )


# ! tested with just one value , we need to test with multiple values

def colebrook_white(diameter, roughness, reynolds_number):

    """Calculates the friction factor for pipe flow using the Colebrook-White equation.

    Parameters:
    - diameter (float): The inner diameter of the pipe (in meters).
    - roughness (float): The absolute roughness of the pipe's inner surface (in meters).
    - reynolds_number (float): The Reynolds number of the flow, which is a dimensionless quantity.

    Returns:
    - friction_factor (float): The friction factor calculated using the Colebrook-White equation.

    Formula:
    The Colebrook-White equation is an implicit equation given by:
    1/sqrt(f) = -2 * log10((roughness/(3.7*diameter)) + (2.51/(reynolds_number*sqrt(f))))

   

    Note:
    - This function uses the Brent's method to solve the implicit Colebrook-White equation.
    - The function assumes that the flow is fully turbulent.
    - The Brent's method requires initial bracketing values, which are provided within a typical range for turbulent flow.
    - The viscosity parameter is not required because the Reynolds number is used directly.

    Exceptions:
    - ValueError: If the Brent's method fails to find a solution within the provided bracketing values, an error is raised.

    Example usage:
    friction_factor = colebrook_white(diameter=0.1, roughness=1e-5, reynolds_number=10000)
    """
   
  
    
    # Function to find root
    def f_zero(f):
        return   1.0 / math.sqrt(f) + 2.0 * math.log10(
            roughness / (3.7 * diameter) + 2.51 / (reynolds_number * math.sqrt(f))
        )
        
        

    # Initial bracketing values for f
    f_l = 0.008  # A reasonable lower bound for turbulent flow
    f_u = 0.08  # A reasonable upper bound for turbulent flow

    # Use Brent's method to find the root
    try:
        # Use Brent's method to find the root
        f = brentq(f_zero, f_l, f_u)
    except ValueError as e:
        raise ValueError("The Brent method failed to find a root: " + str(e))

    return f

def haaland(diameter, roughness, reynolds_number):
    """Calculate the friction factor for fluid flow in a pipe using the Haaland equation.

    Args:
        diameter (float): The diameter of the pipe in mm.
        roughness (float): The roughness height of the pipe in mm.
        reynolds_number (float): The Reynolds number of the flow.

    Returns:
        float: The friction factor.

    Formula:
        The Haaland equation is given by:
        1/sqrt(f) = (-1.8 * math.log10((roughness / (3.7 * diameter)) ** 1.11 + 6.9 / reynolds_number))

    Note:
        The Haaland equation is an approximation of the Colebrook-White equation and is commonly used in practice.

    Examples:
        >>> haaland(100, 0.1, 10000)
        0.025

    """
    return (-1.8 * math.log10((roughness / (3.7 * diameter)) ** 1.11 + 6.9 / reynolds_number)) ** -2


def frictions_factor(diameter, roughness, reynolds_number, method="swamee_jain"):
    """Calculate the friction factor for fluid flow in a pipe.

    Args:
        diameter (float): The diameter of the pipe in mm .
        roughness (float): The roughness height of the pipe in mm .
        reynolds_number (float): The Reynolds number of the flow.
        method (str, optional): The method to use for calculating the friction factor.
            Defaults to "swamee_jain".
            other methods are "colebrook_white" and "haaland"

    Returns:
        float: The friction factor.

    Raises:
        ValueError: If an invalid method is specified.

    Examples:
        >>> frictions_factor(100, 0.1, 10000)
        0.025

    """
    match method:
        case "swamee_jain":
            return swamee_jain(diameter, roughness, reynolds_number)
        case "colebrook_white":
            return colebrook_white(diameter, roughness, reynolds_number)
        case "haaland":
            return haaland(diameter, roughness, reynolds_number)
        case _:
            raise ValueError("Invalid method specified.")
        
# ! test code not written yet
def mass_density(temperature):
    """
    Calculate the mass density of water at a given temperature.

    Parameters:
    temperature (float): The temperature of water in degrees Celsius.

    Returns:
    float: The mass density of water at the given temperature.

    Raises:
    TypeError: If the temperature is not a number (int or float).
    ValueError: If the temperature is not within the range of 0 to 100 degrees Celsius.


    Formula:
    The mass density of water is calculated using the following formula:
    mass_density = 1000 - 0.019549 * (abs(temperature - 3.98)) ** 1.68

    References:
    - Heggen (1983) and  Physical Hydrology, Third Edition, page 545.
    """

    if not isinstance(temperature, (int, float)):
        raise TypeError("Temperature must be a number (int or a float)")

    if temperature < 0 or temperature > 100:
        raise ValueError("Temperature must be within the range of 0 to 100 degrees Celsius")

    return 1000 - 0.019549 * (abs(temperature - 3.98)) ** 1.68

# ! test code not written yet
def dynamic_viscosity(temperature):
    """
    Calculate the dynamic viscosity of water at a given temperature.

    Parameters:
    temperature (float): The temperature of water in degrees Celsius.

    Returns:
    float: The dynamic viscosity of water at the given temperature.

    Raises:
    TypeError: If the temperature is not a number (int or float).
    ValueError: If the temperature is not within the range of 0 to 100 degrees Celsius.

   
    Formula:
    The dynamic viscosity of water is calculated using the following formula:
    dynamic_viscosity = 0.001 * (20987 - 92.613 * temperature) ** 0.4348

    References:
    - Heggen (1983) and  Physical Hydrology, Third Edition, page 545.
    """

    if not isinstance(temperature, (int, float)):
        raise TypeError("Temperature must be a number (int or a float)")

    if temperature < 0 or temperature > 100:
        raise ValueError("Temperature must be within the range of 0 to 100 degrees Celsius")

    return 2.0319 *10**-4 +1.5883*10^-3 *math.exp(-((temperature**0.9)/22))

# ! test code not written yet
def specific_heat(temperature):
    """
    Calculate the specific heat of water at a given temperature.

    Parameters:
    temperature (float): The temperature of water in degrees Celsius.

    Returns:
    float: The specific heat of water at the given temperature.

    Raises:
    TypeError: If the temperature is not a number (int or float).
    ValueError: If the temperature is not within the range of 0 to 100 degrees Celsius.

    Formula:
    The specific heat of water is calculated using the following formula:
    specific_heat = 4.175 +1.666*[exp((34.5-temperature)/10.6)+exp(-(34.5-temperature)/10.6) ]

    References:
    - Heggen (1983) and  Physical Hydrology, Third Edition, page 545.
    """

    if not isinstance(temperature, (int, float)):
        raise TypeError("Temperature must be a number (int or a float)")

    if temperature < 0 or temperature > 100:
        raise ValueError("Temperature must be within the range of 0 to 100 degrees Celsius")

    return 4.175 +1.666*(math.exp((34.5-temperature)/10.6)+math.exp(-(34.5-temperature)/10.6))

#! test code not writen yet 

def kinematic_viscosity(temperature):
    """
    Calculate the kinematic viscosity of water at a given temperature.

    Parameters:
    temperature (float): The temperature of water in degrees Celsius.

    Returns:
    float: The kinematic viscosity of water at the given temperature.

    Raises:
    TypeError: If the temperature is not a number (int or float).
    ValueError: If the temperature is not within the range of 0 to 100 degrees Celsius.

    Formula:
    The kinematic viscosity of water is calculated using the following formula:
    kinematic_viscosity = dynamic_viscosity(temperature) / mass_density(temperature)

   
    """

    if not isinstance(temperature, (int, float)):
        raise TypeError("Temperature must be a number (int or a float)")

    if temperature < 0 or temperature > 100:
        raise ValueError("Temperature must be within the range of 0 to 100 degrees Celsius")

    return dynamic_viscosity(temperature) / mass_density(temperature)


def tau_max(diameter, vannføring, helning_value, manning):
    """
    Calculate the kinematic viscosity of water at a given temperature.

    Parameters:
    Diameter (float): The diameter of the pipe in mm.
    vannføring (float): The water flow rate in the pipe in L/S.
    manning (float): The Manning's roughness coefficient for the pipe material.(1/n)
    helning_value (float): The slope or inclination of the pipe. It's a dimensionless value.
    Returns:
    tau_maks (float): The maximum shear stress in the pipe.
    """
    h_d = np.linspace(0, 1, 10000)
    q_qfylt = (
        0.46 - 0.5 * np.cos(np.pi * h_d) + 0.04 * np.cos(2 * np.pi * h_d)
    )  # Formel fra Marius Møller Rokstad
    
    
    Q_fylt = (
            manning
            * (diameter / 4000) ** (2 / 3)
            * helning_value ** (1 / 2)
            * 1000
            * np.pi
            * (diameter / 2000) ** 2
        )
    q_del_på_qfylt = vannføring / Q_fylt
    tau_fylt = 1000 * 9.81 * diameter / 4 * helning_value
    idx = (np.abs(q_qfylt - q_del_på_qfylt)).argmin()
    tau_maks = 4 * h_d[idx] * (1 - h_d[idx]) * tau_fylt
        
    return tau_maks


