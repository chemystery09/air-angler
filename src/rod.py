import os
import random
from pathlib import Path

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
        return x_col and y_col and x_col2 and y_col2


def load_image(name):
    path = os.path.join(main_dir, "data", name)
    return pygame.image.load(path).convert()


class Rod(GameObject):
    def __init__(self, *args, **kwargs) -> None:
        super(*args, **kwargs)
        self.is_dropping = False


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    fish1_img = load_image("fish1.png")
    fish2_img = load_image("fish2.png")
    fish3_img = load_image("fish3.png")

    # background = load_image("allfish.png")  # change me!

    # background = pygame.transform.scale2x(background)
    # background = pygame.transform.scale2x(background)

    # screen.blit(background, (0, 0))

    fish_objects = []

    for _ in range(random.randint(MIN_FISH, MAX_FISH)):
        img = random.choice((fish1_img, fish2_img, fish3_img))
        x = random.randint(0, 10)
        fish_objects.append(GameObject(img, x * 40, x))

    chosen_fish_tmp = random.choice(fish_objects)
    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            chosen_fish_tmp.move(up=True)
        if keys[pygame.K_DOWN]:
            chosen_fish_tmp.move(down=True)
        if keys[pygame.K_LEFT]:
            chosen_fish_tmp.move(left=True)
        if keys[pygame.K_RIGHT]:
            chosen_fish_tmp.move(right=True)

        # screen.blit(background, (0, 0))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        # for o in fish_objects:
        #     screen.blit(background, o.pos)
        for o in fish_objects:
            screen.blit(o.image, o.pos)
        clock.tick(60)
        pygame.display.update()
        pygame.time.delay(100)


if __name__ == "__main__":
    main()
    pygame.quit()
