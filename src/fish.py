import pygame
import math


class Fish:
    def __init__(self, screen, x, y, orientation = 0, color=(0, 0, 255), size=(50, 30)):
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
        self.color = color
        self.size = size

    def rotate(self, angle):
        """
        Rotate the fish by a given angle.
        
        :param angle: The angle to rotate the fish by.
        """
        self.orientation += angle

    def draw(self, screen_position=(0, 0)):
        """
        Draw the fish on the screen at its current position and orientation.
        """
        width, height = self.size
    
        self.x = self.x - screen_position[0]
        self.y = self.y - screen_position[1]

        body = pygame.Rect(self.x, self.y, width, height)
        pygame.draw.ellipse(self.screen, self.color, body)

        # Draw the tail

        tail_points = [
            (0, height // 2),
            (- width // 2, 0),
            (- width // 2, height)
        ]

        # Rotate tail points by the orientation angle
        rotated_tail_points = []
        for point in tail_points:
            rotated_x = point[0] * math.cos(math.radians(self.orientation)) - point[1] * math.sin(math.radians(self.orientation))
            rotated_y = point[0] * math.sin(math.radians(self.orientation)) + point[1] * math.cos(math.radians(self.orientation))
            rotated_tail_points.append((rotated_x + self.x, rotated_y + self.y))

        tail_points = rotated_tail_points

        pygame.draw.polygon(self.screen, self.color, tail_points)

        self.x = self.x + screen_position[0]
        self.y = self.y + screen_position[1]
