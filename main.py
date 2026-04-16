import random
import math
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
FPS_COLOR = (255, 255, 255)

# Square settings
NUM_SQUARES = 20
DIRECTION_CHANGE_INTERVAL = 4000  # milliseconds
FLEE_DISTANCE = 120
RANDOM_DIRECTION_STRENGTH = 0.35
MIN_LIFESPAN_MS = 5000
MAX_LIFESPAN_MS = 12000


class Square:
    def __init__(self):
        self.size = random.randint(20, 80)

        self.x = random.uniform(0, WIDTH - self.size)
        self.y = random.uniform(0, HEIGHT - self.size)

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

        # Smaller squares move faster than bigger ones
        self.speed = max(60, 220 - self.size * 2)

        self.birth_time = pygame.time.get_ticks()
        self.lifespan_ms = random.randint(MIN_LIFESPAN_MS, MAX_LIFESPAN_MS)

        self.vx = 0
        self.vy = 0
        self.set_random_direction()

    def is_expired(self, current_time):
        return current_time - self.birth_time >= self.lifespan_ms

    def set_random_direction(self):
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

    def move(self, delta_time):
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        # Bounce on window borders
        if self.x <= 0:
            self.x = 0
            self.vx *= -1
        elif self.x + self.size >= WIDTH:
            self.x = WIDTH - self.size
            self.vx *= -1

        if self.y <= 0:
            self.y = 0
            self.vy *= -1
        elif self.y + self.size >= HEIGHT:
            self.y = HEIGHT - self.size
            self.vy *= -1

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            (int(self.x), int(self.y), self.size, self.size)
        )

    def center(self):
        return (self.x + self.size / 2, self.y + self.size / 2)

    @staticmethod
    def handle_fleeing(squares):
        for square in squares:
            flee_x = 0
            flee_y = 0

            sx, sy = square.center()

            for other in squares:
                if square is other:
                    continue

                # Only smaller squares flee bigger ones
                if square.size < other.size:
                    ox, oy = other.center()

                    dx = sx - ox
                    dy = sy - oy
                    distance = math.hypot(dx, dy)

                    if 0 < distance < FLEE_DISTANCE:
                        strength = (FLEE_DISTANCE - distance) / FLEE_DISTANCE
                        flee_x += (dx / distance) * strength
                        flee_y += (dy / distance) * strength

            # If there is something to flee from, combine fleeing with randomness
            flee_length = math.hypot(flee_x, flee_y)
            if flee_length > 0:
                flee_x /= flee_length
                flee_y /= flee_length

                random_angle = random.uniform(0, 2 * math.pi)
                rand_x = math.cos(random_angle)
                rand_y = math.sin(random_angle)

                final_x = flee_x + rand_x * RANDOM_DIRECTION_STRENGTH
                final_y = flee_y + rand_y * RANDOM_DIRECTION_STRENGTH

                final_length = math.hypot(final_x, final_y)
                if final_length > 0:
                    final_x /= final_length
                    final_y /= final_length

                    square.vx = final_x * square.speed
                    square.vy = final_y * square.speed


def draw_fps(surface, clock, font):
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.1f}", True, FPS_COLOR)
    surface.blit(fps_text, (10, 10))


def main():
    squares = [Square() for _ in range(NUM_SQUARES)]
    font = pygame.font.SysFont("Arial", 18)

    running = True
    last_direction_change = pygame.time.get_ticks()

    while running:
        # delta_time in seconds
        delta_time = CLOCK.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()

        # Random direction refresh every 4 seconds
        if current_time - last_direction_change >= DIRECTION_CHANGE_INTERVAL:
            for square in squares:
                square.set_random_direction()
            last_direction_change = current_time

        Square.handle_fleeing(squares)

        for square in squares:
            square.move(delta_time)

        # Keep the same amount of squares by replacing expired ones.
        squares = [square if not square.is_expired(current_time) else Square() for square in squares]

        SCREEN.fill(BACKGROUND_COLOR)

        for square in squares:
            square.draw(SCREEN)

        draw_fps(SCREEN, CLOCK, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()