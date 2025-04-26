import pytest
from norconsult.all_formulas import  swamee_jain, colebrook_white , frictions_factor, haaland
from norconsult.all_simple import area, velocity, reynolds_number
import math

def test_area():
    """
    Test that the area function returns the correct calculation.
    """
    # Test with a diameter of 1000mm (1m), expecting area = π * (0.5^2)
    assert math.isclose(area(1000), math.pi * 0.5**2, rel_tol=1e-4)

def test_velocity():
    """
    Test that the velocity function returns the correct calculation.
    """
    # Test with a flow of 1000L/s and diameter of 1000mm (1m)
    # Expected velocity = flow / area / 1000 = 1000 / (π * (0.5^2)) / 1000
    expected_velocity = 1000 / (math.pi * 0.5**2) / 1000
    assert math.isclose( velocity(1000, 1000), expected_velocity, rel_tol=1e-4)

def test_reynolds_number():
    # Test with known values
    flow = 110.25  # L/s
    diameter = 350 # mm
    velocity =  (flow/1000)/(math.pi*(diameter/2/1000)**2)


    viscosity = 1.31 * 10**-6  # m^2/s
    expected_result = 306160.6539



    assert pytest.approx(reynolds_number(velocity, diameter,viscosity), 0.0001) == expected_result

    # Test with default viscosity
    expected_result_default_viscosity = 306160.6539

    assert pytest.approx(reynolds_number(velocity, diameter), 0.0001) == expected_result_default_viscosity

def test_swamee_jain():
    # Test with known values
    flow = 110.25  # L/s
    diameter = 350  # mm
    ruhet = 0.5 # mm to m
    reynolds_number = 306160.6539
    expected_result = 0.02235040

    assert pytest.approx(swamee_jain(diameter, ruhet, reynolds_number), 0.001) == expected_result



def test_colebrook_white():
    # Test with known values
    diameter = 300  # m
    roughness = 0.5  # mm
    reynolds_number = 306160
    expected_result = 0.023
    assert pytest.approx(colebrook_white(diameter, roughness, reynolds_number), 0.001) == expected_result

def test_frictions_factor():
    # Test with known values
    diameter = 350
    roughness = 0.5
    reynolds_number = 306160.6539
    expected_result_default = 0.02235040
    expected_result_colebrook = 0.0222044
    expected_result_haaland = 0.0221553
    assert (pytest.approx(frictions_factor(diameter, roughness, reynolds_number), 0.0001)
            == expected_result_default)
    assert (pytest.approx(frictions_factor(diameter, roughness, reynolds_number, method= 'colebrook_white' ), 0.0001)
            == expected_result_colebrook)
    assert (pytest.approx(frictions_factor(diameter, roughness, reynolds_number, method= 'haaland' ), 0.0001)
            == expected_result_haaland)

def test_haaland():
    # Test with known values
    diameter = 350  # m
    roughness = 0.5  # mm
    reynolds_number = 306160
    expected_result = 0.0221553
    assert pytest.approx(haaland(diameter, roughness, reynolds_number), 0.0001) == expected_result

 #mass_density, dynamic_viscosity,specific_heat,kinematic_viscosity






