"""
Calculate the quantum phase shift and entanglement lag time for a photon
passing through a beam splitter, based on the velocity of the photon,
wavelength, and angle of incidence.

Parameters:
v_mps : float
    Target velocity (m/s).
wavelength_nm : float
    Wavelength of the photon (nm). Default: 500 nm.
angle_deg : float
    Angle of incidence (degrees). Default: 0°.

Returns:
delta_phi : float
    Phase shift (radians).
delta_t_ent : float
    Entanglement lag time (seconds).
"""

import numpy as np

def calculate_phase_shift(v_mps, wavelength_nm=500, angle_deg=0):
    c = 3e8  # Speed of light (m/s)
    lambda_m = wavelength_nm * 1e-9  # Convert wavelength to meters
    theta_rad = np.radians(angle_deg)  # Convert angle to radians

    # Quantum phase shift
    delta_phi = (2 * np.pi / lambda_m) * (v_mps / c) * np.cos(theta_rad)

    # Entanglement lag time
    f = c / lambda_m  # Frequency of the photon
    omega = 2 * np.pi * f  # Angular frequency
    delta_t_ent = delta_phi / omega

    return delta_phi, delta_t_ent

# Example usage with suggested values
v_mps = 1.0  # Target velocity in m/s
wavelength_nm = 500  # Wavelength in nm
angle_deg = 0  # Angle of incidence in degrees

delta_phi, delta_t_ent = calculate_phase_shift(v_mps, wavelength_nm, angle_deg)
print(f"Phase Shift (rad): {delta_phi}")
print(f"Entanglement Lag Time (s): {delta_t_ent}")