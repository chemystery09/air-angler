# importing required library
import math

import pygame

from fish import *
import random

# activate the pygame library .
pygame.init()
X = 1920
Y = 1080

# create the display surface object
# of specific dimension..e(X, Y).
scrn = pygame.display.set_mode((X, Y))

# Import the Fish class


# Create a list of Fish instances
# fishes = [
#     Fish(scrn, x=100, y=100),
#     Fish(scrn, x=200, y=200),
#     Fish(scrn, x=300, y=300),
#     Fish(scrn, x=400, y=400),
# ]

# test_fish = Fish(scrn, x=350, y=400)

# Create a screen position array
scrn_pos = [0, 0]

# Define parameters for circular motion
# radius = 100
# angle = 0
# angle_increment = 0.005  # Speed of rotation


# Update the screen position in a circular motion
# def update_screen_position() -> None:
#     global angle, scrn_pos
#     scrn_pos[0] = int(radius * math.cos(angle))
#     scrn_pos[1] = int(radius * math.sin(angle))
#     angle += angle_increment


# Replace the single fish instance with the list
# Main loop

scroll_speed = 5
fish_x_bounds = (500, 1400)
fish_y_bounds = (1200, 5500)

fishes = [
    Fish(
        scrn,
        random.randint(*fish_x_bounds),
        random.randint(*fish_y_bounds),
        speed=scroll_speed,
        direction=random.choice((True, False)),
        aimless_speed=random.uniform(scroll_speed * 0.5, scroll_speed * 1.5),
    )
    for _ in range(random.randint(30, 50))
]
test_fish = min(fishes, key=lambda x: x.pos[1])

bg_img = pygame.image.load("src/data/bg.png").convert()
background = GameObject(bg_img, 0, scroll_speed)
going_down = True


clock = pygame.time.Clock()

random.shuffle(fishes)
status = True
while status:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False

    # Clear the screen
    scrn.fill((255, 255, 255))
    scrn.blit(background.image, background.pos)

    if going_down:
        background.move(up=True)
    else:
        background.move(down=True)

    if background.pos[1] < -4800:
        going_down = False

    # Draw the fish
    for fish in fishes:
        if going_down:
            fish.move(up=True)
        else:
            fish.move(down=True)
        
        fish.draw(scrn_pos)
        if any(f.collides(fish) for f in fishes):
            fish.hooked()
            fish.hang_dead()
        if fish.pos[0] < fish_x_bounds[0] or fish.pos[0] > fish_x_bounds[1]:
            fish.direction = not fish.direction

    # update_screen_position()

    # Update the display

    clock.tick(60)
    pygame.display.flip()
