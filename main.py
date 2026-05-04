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
DIRECTION_CHANGE_INTERVAL = 4000
FLEE_DISTANCE = 120
RANDOM_DIRECTION_STRENGTH = 0.35
MIN_LIFESPAN_MS = 5000
MAX_LIFESPAN_MS = 12000


class Square:
    def __init__(self, size):
        self.size = size

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
        return self.x + self.size / 2, self.y + self.size / 2

    @staticmethod
    def handle_fleeing(squares):
        for square in squares:
            flee_x = 0
            flee_y = 0

            sx, sy = square.center()

            for other in squares:
                if square is other:
                    continue

                if square.size < other.size:
                    ox, oy = other.center()

                    dx = sx - ox
                    dy = sy - oy
                    distance = vector_length(dx, dy)

                    if 0 < distance < FLEE_DISTANCE:
                        strength = (FLEE_DISTANCE - distance) / FLEE_DISTANCE
                        away_x, away_y = normalize_vector(dx, dy)

                        flee_x += away_x * strength
                        flee_y += away_y * strength

            flee_length = vector_length(flee_x, flee_y)

            if flee_length > 0:
                flee_x, flee_y = normalize_vector(flee_x, flee_y)

                random_angle = random.uniform(0, 2 * math.pi)
                rand_x = math.cos(random_angle)
                rand_y = math.sin(random_angle)

                final_x = flee_x + rand_x * RANDOM_DIRECTION_STRENGTH
                final_y = flee_y + rand_y * RANDOM_DIRECTION_STRENGTH

                final_length = vector_length(final_x, final_y)

                if final_length > 0:
                    final_x, final_y = normalize_vector(final_x, final_y)

                    square.vx = final_x * square.speed
                    square.vy = final_y * square.speed


def vector_length(x, y):
    return math.hypot(x, y)


def normalize_vector(x, y):
    length = vector_length(x, y)

    if length == 0:
        return 0, 0

    return x / length, y / length


def handle_chasing(squares):
    for square in squares:
        chase_x = 0
        chase_y = 0

        sx, sy = square.center()

        for other in squares:
            if square is other:
                continue

            if square.size > other.size:
                ox, oy = other.center()

                dx = ox - sx
                dy = oy - sy
                distance = vector_length(dx, dy)

                if distance > 0:
                    strength = 1 / distance
                    toward_x, toward_y = normalize_vector(dx, dy)

                    chase_x += toward_x * strength
                    chase_y += toward_y * strength

        chase_length = vector_length(chase_x, chase_y)

        if chase_length > 0:
            chase_x, chase_y = normalize_vector(chase_x, chase_y)

            square.vx = chase_x * square.speed
            square.vy = chase_y * square.speed


def create_mixed_squares():
    squares = []

    for _ in range(5):
        squares.append(Square(25))

    for _ in range(10):
        squares.append(Square(10))

    for _ in range(30):
        squares.append(Square(4))

    return squares


def draw_fps(surface, clock, font):
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.1f}", True, FPS_COLOR)
    surface.blit(fps_text, (10, 10))


def main():
    squares = create_mixed_squares()
    font = pygame.font.SysFont("Arial", 18)

    running = True
    last_direction_change = pygame.time.get_ticks()

    while running:
        delta_time = CLOCK.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()

        if current_time - last_direction_change >= DIRECTION_CHANGE_INTERVAL:
            for square in squares:
                square.set_random_direction()

            last_direction_change = current_time

        handle_chasing(squares)
        Square.handle_fleeing(squares)

        for square in squares:
            square.move(delta_time)

        new_squares = []

        for square in squares:
            if square.is_expired(current_time):
                new_squares.append(Square(square.size))
            else:
                new_squares.append(square)

        squares = new_squares

        SCREEN.fill(BACKGROUND_COLOR)

        for square in squares:
            square.draw(SCREEN)

        draw_fps(SCREEN, CLOCK, font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()