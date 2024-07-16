import pygame
import math
import matplotlib.pyplot as plt
from pendulum_simulation import run_simulation

# Pygame Initialization
pygame.init()
width, height = 800, 400
background = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# COLORS
white = (255, 255, 255)
black = (0, 0, 0)
gray = (150, 150, 150)
Dark_red = (150, 0, 0)

# Simulation parameters
theta0 = (3.141592653589793) / 2  # initial angle in radians
W0 = 0  # initial angular velocity in radians/s
delta_t = 0.01
duration = 10
length = 200  # length of the pendulum in pixels

# Run the simulation
theta_values, W_values, energy_values, t = run_simulation(theta0, W0, delta_t, duration)
sim_index = 0

class Ball(object):
    def __init__(self, XY, radius):
        self.x = XY[0]
        self.y = XY[1]
        self.radius = radius

    def draw(self, bg):
        pygame.draw.lines(bg, black, False, [(width / 2, 50), (self.x, self.y)], 2)
        pygame.draw.circle(bg, black, (self.x, self.y), self.radius)
        pygame.draw.circle(bg, Dark_red, (self.x, self.y), self.radius - 2)

def grid():
    for x in range(50, width, 50):
        pygame.draw.lines(background, gray, False, [(x, 0), (x, height)])
        for y in range(50, height, 50):
            pygame.draw.lines(background, gray, False, [(0, y), (width, y)])
    pygame.draw.circle(background, black, (int(width / 2), 50), 5)

def get_path(angle, length):
    x = width / 2 + length * math.sin(angle)
    y = 50 + length * math.cos(angle)
    return int(x), int(y)

def redraw():
    background.fill(white)
    grid()
    pendulum.draw(background)
    pygame.display.update()

# Initialize the pendulum
pendulum = Ball((int(width / 2), -100), 15)

# Plot initialization
plt.ion()  # Interactive mode on
fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.set_xlim(0, duration)
ax1.set_ylim(min(energy_values), max(energy_values))
ax1.set_ylabel('Energy (J)')
line1, = ax1.plot([], [], 'r-')

ax2.set_xlim(0, duration)
ax2.set_ylim(min(theta_values), max(theta_values))
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Theta (rad)')
line2, = ax2.plot([], [], 'b-')

Out = False
while not Out:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Out = True

    if sim_index < len(theta_values):
        angle = theta_values[sim_index]
        pendulum.x, pendulum.y = get_path(angle, length)
        
        # Update plots
        line1.set_data(t[:sim_index], energy_values[:sim_index])
        line2.set_data(t[:sim_index], theta_values[:sim_index])
        ax1.draw_artist(line1)
        ax2.draw_artist(line2)
        fig.canvas.flush_events()
        
        sim_index += 1

    redraw()

plt.ioff()  # Interactive mode off
plt.show()
pygame.quit()
