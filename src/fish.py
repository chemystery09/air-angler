import pygame
import math
import random
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
        self,
        screen,
        x,
        y,
        orientation=0,
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
        super().__init__(pygame.image.load(f'fish{random.randint(1,3)}.png'), 0 , 0)

        self.flipped = False
        if random.random() > .5:
            self.flipped = True
            self.image = pygame.transform.flip(self.image, True, False)

        self.screen = screen
        self.orientation = orientation
        self.aleph = random.random() + 1
        self.omega = 0

        self.pos = [x,y]

        # Set the size for the image

        SCALE_FAC = 5

        DEFAULT_IMAGE_SIZE = (self.image.get_width() // SCALE_FAC, self.image.get_height() // SCALE_FAC)
        
        # Scale the image to your needed size
        self.image = pygame.transform.scale(self.image, DEFAULT_IMAGE_SIZE)

        # Choose a random color
        self.color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )

        # Choose size using a Gaussian distribution
        width = max(10, int(random.gauss(30, 15)))
        height = (width * 2) // 3
        self.size = (width, height)

    def draw(self, screen_position=(0, 0)) -> None:
        """
        Draw the fish on the screen at its current position and orientation.
        """
        width, height = self.size
       
        rotated_image = pygame.transform.rotate(self.image, math.degrees(self.orientation))
        new_rect = rotated_image.get_rect(center = self.image.get_rect(topleft = self.pos).center)

        # Show the image
        self.screen.blit(rotated_image, new_rect)


    def rotate(self, theta):
        """
        Rotate the fish by a given angle in radians.

        :param theta: The angle in radians to rotate the fish by.
        """
        self.orientation += theta

    def hang_dead(self):
        """
        Hang the fish upside down.
        """

        desired_orientation = math.pi / 2 * (-1, 1)[self.flipped]

        self.omega += (
            self.orientation - desired_orientation
        ) * 0.001 - self.omega * 0.0025 * self.aleph

        self.orientation -= self.omega * 0.1
        #print(self.orientation)
