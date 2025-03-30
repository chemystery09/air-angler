import os
from pathlib import Path

import pygame

#main_dir = os.path.split(Path.resolve(__file__))[0]

def in_range(x, a, b):
    return max(a, min(x, b)) == x

class GameObject:
    def __init__(self, image, height, speed) -> None:
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    # move the object.
    def move(self, *, up=False, down=False, left=False, right=False) -> None:  # noqa: ANN001
        if right:
            self.pos.right += self.speed
        if left:
            self.pos.right -= self.speed
        if down:
            self.pos.top += self.speed
        if up:
            self.pos.top -= self.speed

        # controls the object such that it cannot leave the screen's viewpoint
        # if self.pos.right > WIDTH:
        #     self.pos.left = 0
        # if self.pos.top > HEIGHT - SPRITE_HEIGHT:
        #     self.pos.top = 0
        # if self.pos.right < SPRITE_WIDTH:
        #     self.pos.right = WIDTH
        # if self.pos.top < 0:
        #     self.pos.top = HEIGHT - SPRITE_HEIGHT

    def collides(self, other):
        x_col = in_range(self.pos[0], other.pos[0], other.pos[0] + other.size[0])
        x_col2 = in_range(self.pos[0] + self.size[0], other.pos[0], other.pos[0] + other.size[0])
        
        y_col =  in_range(self.pos[1], other.pos[1], other.pos[1] + other.size[1])
        y_col2 = in_range(self.pos[1] + self.size[1], other.pos[1], other.pos[1] + other.size[1])
        return x_col and y_col and x_col2 and y_col2

        

#def load_image(name):
#    path = os.path.join(main_dir, "data", name)
#    return pygame.image.load(path).convert()


class Rod(GameObject):
    def __init__(self, *args, **kwargs) -> None:
        super(*args, **kwargs)
        self.is_dropping = False

        
