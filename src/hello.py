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

fishes = [
    Fish(scrn, random.randint(500, 1400), random.randint(1200, 6000), speed=scroll_speed)
    for _ in range(random.randint(30, 50))
]
test_fish = min(fishes, key=lambda x: x.pos[1])

bg_img = pygame.image.load("src/data/bg.png").convert()
background = GameObject(bg_img, 0, scroll_speed)

clock = pygame.time.Clock()

random.shuffle(fishes)

r = Rod(scrn, 0, -955.4000000000042)
print(r.pos)

r.trigger_reel()

status = True
while status:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            status = False

    # Clear the screen
    scrn.fill((255, 255, 255))
    scrn.blit(background.image, (background.pos[0] + scrn_pos[0], background.pos[1] + scrn_pos[1]))

    scrn_pos = r.reel_and_drop_itr()
    

    # Draw the fish
    for fish in fishes:
        fish.draw(scrn_pos)
        fish.draw_AABB(scrn_pos)
        fish.hang_dead()
        
        if collides(fish, r, scrn_pos):    
            fish.hooked()

        

    r.draw()
    r.draw_AABB()

    # update_screen_position()

    # Update the display

    clock.tick(60)
    pygame.display.flip()
