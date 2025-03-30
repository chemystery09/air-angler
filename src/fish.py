import math
import random

import pygame

from rod import *


def ellipse_perimeter_points(center_x, center_y, width, height, num_points=10):
    """
    Generate points around the perimeter of an ellipse.

    :param center_x: The x-coordinate of the ellipse center.
    :param center_y: The y-coordinate of the ellipse center.
    :param width: The width of the ellipse.
    :param height: The height of the ellipse.
    :param num_points: The number of points to generate around the perimeter.
    :return: A list of (x, y) points around the ellipse.
    """
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + (width / 2) * math.cos(angle)
        y = center_y + (height / 2) * math.sin(angle)
        points.append((x, y))
    return points


class Fish(GameObject):
    def __init__(
        self, screen, x, y, orientation=0, speed=10, direction=True, aimless_speed=7
    ) -> None:
        """
        Initialize the Fish object.

        :param screen: The pygame screen object to draw on.
        :param x: The x-coordinate of the fish.
        :param y: The y-coordinate of the fish.
        :param orientation: The orientation of the fish ('right' or 'left').
        :param color: The color of the fish (default is blue).
        :param size: The size of the fish as a tuple (width, height).
        :param screen_position: The position of the screen to adjust drawing.
        """
        self.id = random.randint(1, 3)
        super().__init__(
            pygame.image.load(f"src/data/fish{self.id}.png").convert_alpha(), 0, 0
        )

        self.flipped = False
        if random.random() > 0.5:
            self.flipped = True
            self.image = pygame.transform.flip(self.image, True, False)

        self.screen = screen
        self.orientation = orientation
        self.aleph = random.random() + 1
        self.omega = 0

        self.pos = [x, y]

        # Set the size for the image

        SCALE_FAC = 5

        DEFAULT_IMAGE_SIZE = (
            self.image.get_width() // SCALE_FAC,
            self.image.get_height() // SCALE_FAC,
        )

        # Scale the image to your needed size
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)

        # Choose a random color
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        self.dead = False

        self.size = (self.image.get_width(), self.image.get_height())

        self.speed = speed
        self.aimless_swim_speed = aimless_speed
        self.direction = direction

    def move(self, *, up=False, down=False, left=False, right=False) -> None:  # noqa: ANN001
        if right:
            self.pos[0] += self.speed
        if left:
            self.pos[0] -= self.speed
        if down:
            self.pos[1] += self.speed
        if up:
            self.pos[1] -= self.speed

        if self.direction:
            self.pos[0] += self.aimless_swim_speed
        else:
            self.pos[0] -= self.aimless_swim_speed

    def pts(self):
        return self.id * 1.34

    def draw(self, screen_position=(0, 0), fine=(0, 0)) -> None:
        """
        Draw the fish on the screen at its current position and orientation.
        """

        width, height = self.size

        rotated_image = pygame.transform.rotate(
            self.image, math.degrees(self.orientation)
        )

        new_rect = rotated_image.get_rect(
            center=self.image.get_rect(topleft=self.pos).center
        )

        # Show the image
        if not self.dead:
            self.screen.blit(
                rotated_image,
                [screen_position[0] + new_rect[0], screen_position[1] + new_rect[1]],
            )
        else:
            screen_rect = self.screen.get_rect()
            new_rect.center = screen_rect.center
            self.screen.blit(rotated_image, (new_rect[0] - fine[0], new_rect[1] - 200))

    def rotate(self, theta):
        """
        Rotate the fish by a given angle in radians.

        :param theta: The angle in radians to rotate the fish by.
        """
        self.orientation += theta

    def hooked(self):
        self.dead = True

    def hang_dead(self):
        """
        Hang the fish upside down.
        """
        if self.dead:
            desired_orientation = math.pi / 2 * (-1, 1)[self.flipped]

            self.omega += (
                self.orientation - desired_orientation
            ) * 0.01 - self.omega * 0.025 * self.aleph

        self.orientation -= self.omega * 0.1
        # print(self.orientation)

    def draw_AABB(self, screen_position=(0, 0)) -> None:
        """
        Draw the Axis-Aligned Bounding Box (AABB) around the fish.
        """
        width, height = self.size
        x, y = self.pos

        x += screen_position[0]
        y += screen_position[1]

        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)

    def get_corr_pos(self, screen_pos):
        return (self.pos[0] + screen_pos[0], self.pos[1] + screen_pos[1])

    def get_corr_size(self):
        return self.size
