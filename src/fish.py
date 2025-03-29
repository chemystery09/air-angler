import pygame


class Fish:
    def __init__(
        self,
        screen,
        x,
        y,
        orientation="right",
        color=(0, 0, 255),
        size=(50, 30),
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
        self.color = color
        self.size = size

    def draw(self, screen_position=(0, 0)) -> None:
        """
        Draw the fish on the screen at its current position and orientation.
        """
        width, height = self.size

        self.x -= screen_position[0]
        self.y -= screen_position[1]

        body = pygame.Rect(self.x, self.y, width, height)
        pygame.draw.ellipse(self.screen, self.color, body)

        # Draw the tail
        if self.orientation == "right":
            tail_points = [
                (self.x, self.y + height // 2),
                (self.x - width // 2, self.y),
                (self.x - width // 2, self.y + height),
            ]
        else:  # orientation == 'left'
            tail_points = [
                (self.x + width, self.y + height // 2),
                (self.x + width + width // 2, self.y),
                (self.x + width + width // 2, self.y + height),
            ]
        pygame.draw.polygon(self.screen, self.color, tail_points)

        self.x += screen_position[0]
        self.y += screen_position[1]
