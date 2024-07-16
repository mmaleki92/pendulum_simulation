import numpy as np

# Constants
m = 1  # mass in kg
L = 1  # length in meters
g = 9.81  # acceleration due to gravity in m/s^2

# Function to calculate derivatives of theta and theta_dot
def pendulum_derivatives(theta, W):
    dtheta_dt = W
    dW_dt = -(g / L) * np.sin(theta)
    return [dtheta_dt, dW_dt]

# Function to perform the Euler-Cromer simulation
def run_simulation(theta0, W0, delta_t, duration):
    t = np.arange(0, duration, delta_t)

    # Initialize arrays to store results
    theta_values = np.zeros_like(t)
    W_values = np.zeros_like(t)
    energy_values = np.zeros_like(t)

    # Initial conditions
    theta_values[0] = theta0
    W_values[0] = W0
    energy_values[0] = 0.5 * m * L**2 * W0**2 - m * g * L * np.cos(theta0)

    # Euler-Cromer method
    for i in range(1, len(t)):
        W_values[i] = W_values[i - 1] + delta_t * pendulum_derivatives(theta_values[i - 1], W_values[i - 1])[1]
        theta_values[i] = theta_values[i - 1] + delta_t * W_values[i]
        energy_values[i] = 0.5 * m * L**2 * W_values[i]**2 - m * g * L * np.cos(theta_values[i])

    return theta_values, W_values, energy_values, t
