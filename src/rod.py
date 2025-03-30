import os
import random

import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]

WIDTH, HEIGHT = 1920, 1080
MIN_FISH, MAX_FISH = 10, 20


def in_range(x, a, b):
    return max(a, min(x, b)) == x


class GameObject:
    def __init__(self, image, height, speed) -> None:
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)
        self.size = self.image.get_size()

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
        x_col2 = in_range(
            self.pos[0] + self.size[0], other.pos[0], other.pos[0] + other.size[0]
        )

        y_col = in_range(self.pos[1], other.pos[1], other.pos[1] + other.size[1])
        y_col2 = in_range(
            self.pos[1] + self.size[1], other.pos[1], other.pos[1] + other.size[1]
        )
        return (x_col or x_col2) and (y_col or y_col2)
    


def load_image(name):
    path = os.path.join(main_dir, "data", name)
    return pygame.image.load(path).convert_alpha()


class Rod(GameObject):
    def __init__(self, screen, x, y) -> None:
        
        super().__init__(
            load_image("fishingLine.png"), 0, 0
        )

        self.is_dropping = False
        
        self.size = self.image.get_size()

        self.pos = [x,y]
        self.screen = screen
        self.is_dropping, self.is_reeling, self.is_waiting = False, False, True

        self.fine = [0, 0]
        self.v = 0


    def draw(self, screen_position = (0, 0)) -> None:
        """
        Draw the fish on the screen at its current position and orientation.
        """
        width, height = self.size

        bobber_pos = (width // 2 + self.fine[0], height * 1.3)

        screen_center = (HEIGHT // 2, WIDTH // 2)
        render_pos = (screen_center[0] - bobber_pos[0], screen_center[1] - bobber_pos[1])

        # Show the image
        self.screen.blit(self.image, render_pos)

    def trigger_reel(self):
        self.is_waiting = False

    def reel_and_drop_itr(self):

        if (self.is_waiting):
            return self.pos

        if (not self.is_dropping and not self.is_reeling):
            self.v = -15


        if (self.v < 0):
            self.v += 0.1
            self.pos[1] += self.v
            self.is_dropping = True
            self.is_reeling = True
        else:
            self.is_dropping = False
            self.is_reeling = True
            # collision handling
            self.pos[1] += 1.

        if (self.pos[1] >= 0):
            self.is_reeling = False
            self.is_waiting = True

        return self.pos
        
