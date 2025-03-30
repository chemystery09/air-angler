# importing required library
import math

import pygame

from fish import *
import random

# activate the pygame library .
pygame.init()
X = 500
Y = 500

# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y))

# Import the Fish class


# Create a list of Fish instances
fishes = [
    Fish(scrn, x=100, y=100),
    Fish(scrn, x=200, y=200),
    Fish(scrn, x=300, y=300),
    Fish(scrn, x=400, y=400)
]

test_fish = Fish(scrn, x=200, y=400)

# Create a screen position array
scrn_pos = [0, 0]

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

random.shuffle(fishes)
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
        if (test_fish.collides(fish)):
            fish.hang_dead()
        
    # update_screen_position()

    # Update the display
    pygame.display.flip()
