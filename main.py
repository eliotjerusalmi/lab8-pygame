import random
import pygame


pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab 8 - Moving Squares")


CLOCK = pygame.time.Clock()
FPS = 60

# Colors
BACKGROUND_COLOR = (30, 30, 30)

# Square settings
NUM_SQUARES = 10
SQUARE_SIZE = 40
MAX_SPEED = 4


class Square:
    def __init__(self):
        self.size = SQUARE_SIZE
        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

        self.dx = random.choice([-1, 1]) * random.randint(1, MAX_SPEED)
        self.dy = random.choice([-1, 1]) * random.randint(1, MAX_SPEED)

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def move(self):
        self.x += self.dx
        self.y += self.dy

        
        if self.x <= 0 or self.x + self.size >= WIDTH:
            self.dx *= -1

       
        if self.y <= 0 or self.y + self.size >= HEIGHT:
            self.dy *= -1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))


def main():
    squares = [Square() for _ in range(NUM_SQUARES)]
    running = True

    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
        for square in squares:
            square.move()

        
        SCREEN.fill(BACKGROUND_COLOR)
        for square in squares:
            square.draw(SCREEN)

        
        pygame.display.flip()

        
        CLOCK.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()