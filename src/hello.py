# importing required library
import math

import pygame

from fish import Fish

# activate the pygame library .
pygame.init()
X = 1000
Y = 1000

# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y))

# Import the Fish class

# Create a Fish instance
fish = Fish(scrn, x=500, y=500)
# Create a list of Fish instances
fishes = [
    Fish(scrn, x=200, y=200, orientation=math.pi/2),
    Fish(scrn, x=400, y=300, orientation=math.pi/2),
    Fish(scrn, x=600, y=400, orientation=math.pi/2),
    Fish(scrn, x=800, y=500, orientation=math.pi/2)
]

# Create a screen position array
scrn_pos = [500, 500]

# Define parameters for circular motion
radius = 100
angle = 0
angle_increment = 0.005  # Speed of rotation


# Update the screen position in a circular motion
def update_screen_position() -> None:
    global angle, scrn_pos
    scrn_pos[0] = int(radius * math.cos(angle))
    scrn_pos[1] = int(radius * math.sin(angle))
    angle += angle_increment


# Replace the single fish instance with the list
# Main loop

status = True
while status:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False

    # Clear the screen
    scrn.fill((255, 255, 255))

    # Draw the fish
    for fish in fishes:
        fish.draw(scrn_pos)
        fish.hang_dead()
        
    update_screen_position()

    # Update the display
    pygame.display.flip()
