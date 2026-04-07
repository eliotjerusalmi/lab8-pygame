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
SQUARE_SIZE = 30
MAX_SPEED = 5

# Changement de direction toutes les 4 secondes
DIRECTION_CHANGE_INTERVAL = 4000  # en millisecondes


class Square:
    def __init__(self):
        self.size = random.randint(20, 80)

        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

        self.set_random_direction()

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

    def set_random_direction(self):
        speed_factor = max(1, int(80 / self.size))
        self.dx = random.choice([-1, 1]) * random.randint(1, speed_factor)
        self.dy = random.choice([-1, 1]) * random.randint(1, speed_factor)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x + self.size >= WIDTH:
            self.dx *= -1

        if self.y <= 0 or self.y + self.size >= HEIGHT:
            self.dy *= -1

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

    def handle_fleeing(squares):
    
        for i in range(len(squares)):
            for j in range(i + 1, len(squares)):
                s1 = squares[i]
            s2 = squares[j]

            dx = s1.x - s2.x
            dy = s1.y - s2.y

            # distance simple
            if abs(dx) < 50 and abs(dy) < 50:

                # IMPORTANT : éviter de changer direction tout le temps
                if random.random() < 0.02:  # 2% de chance seulement

                    if dx > 0:
                        s1.dx = 2
                        s2.dx = -2
                    else:
                        s1.dx = -2
                        s2.dx = 2

                    if dy > 0:
                        s1.dy = 2
                        s2.dy = -2
                    else:
                        s1.dy = -2
                        s2.dy = 2

def main():
    squares = [Square() for _ in range(NUM_SQUARES)]
    running = True

    last_direction_change = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        if current_time - last_direction_change >= DIRECTION_CHANGE_INTERVAL:
            for square in squares:
                square.set_random_direction()
            last_direction_change = current_time

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