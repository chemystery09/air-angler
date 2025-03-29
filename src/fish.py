import pygame
import math
import random

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

class Fish:
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
        self.screen = screen
        self.x = x
        self.y = y
        self.orientation = orientation
        self.aleph = random.random() + .01
        self.omega = 0
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

        self.x -= screen_position[0]
        self.y -= screen_position[1]

        body = pygame.Rect(self.x, self.y, width, height)
        

        # Draw the tail

        tail_points = [
            (self.x + width, self.y + height // 2),
            (self.x + width + width // 2, self.y),
            (self.x + width + width // 2, self.y + height),
        ]



        # Example usage of the function to trace the fish's body
        ellipse_points = ellipse_perimeter_points(
            self.x + width // 2, self.y + height // 2, width, height
        )

        points = tail_points + ellipse_points

        # Rotate points by orientation
        rotated_points = []
        for px, py in points:
            # Translate point to origin
            translated_x = px - (self.x + width // 2)
            translated_y = py - (self.y + height // 2)

            # Apply rotation
            rotated_x = (
            translated_x * math.cos(self.orientation)
            - translated_y * math.sin(self.orientation)
            )
            rotated_y = (
            translated_x * math.sin(self.orientation)
            + translated_y * math.cos(self.orientation)
            )

            # Translate point back
            final_x = rotated_x + (self.x + width // 2)
            final_y = rotated_y + (self.y + height // 2)

            rotated_points.append((final_x, final_y))

        # Draw the rotated fish
        pygame.draw.polygon(self.screen, self.color, rotated_points)

        self.x += screen_position[0]
        self.y += screen_position[1]
    
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

        desired_orientation = -math.pi / 2 + math.pi

        self.omega += (self.orientation - desired_orientation) * .001 - self.omega * .0025 * self.aleph

        self.orientation -= self.omega * .1
