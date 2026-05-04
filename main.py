import random
import math
import pygame

pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab - Animated Growth")

CLOCK = pygame.time.Clock()
FPS = 60

# Colors
BACKGROUND_COLOR = (30, 30, 30)
FPS_COLOR = (255, 255, 255)

# Settings
DIRECTION_CHANGE_INTERVAL = 4000
FLEE_DISTANCE = 15
RANDOM_DIRECTION_STRENGTH = 0.35
MIN_LIFESPAN_MS = 5000
MAX_LIFESPAN_MS = 12000

# Eating++
GROWTH_FACTOR = 0.4
MAX_SIZE = 120

# Animated growth
GROWTH_SPEED = 500  # ms

# Trails
TRAILS_LENGTH = 30


class Square:
    def __init__(self, size):
        self.original_size = size
        self.size = size

        self.target_size = size
        self.growth_start_time = None

        self.x = random.uniform(0, WIDTH - self.size)
        self.y = random.uniform(0, HEIGHT - self.size)

        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255),
        )

        self.trail = []

        self.update_speed()

        self.birth_time = pygame.time.get_ticks()
        self.lifespan_ms = random.randint(MIN_LIFESPAN_MS, MAX_LIFESPAN_MS)

        self.vx = 0
        self.vy = 0
        self.set_random_direction()

    def update_speed(self):
        self.speed = max(40, 220 - self.size * 2)

    def start_growth(self, prey_size):
        growth_amount = prey_size * GROWTH_FACTOR
        self.target_size = min(MAX_SIZE, self.size + growth_amount)
        self.growth_start_time = pygame.time.get_ticks()

    def update_growth(self, current_time):
        if self.growth_start_time is None:
            return

        elapsed = current_time - self.growth_start_time

        if elapsed >= GROWTH_SPEED:
            self.size = self.target_size
            self.growth_start_time = None
        else:
            t = elapsed / GROWTH_SPEED
            self.size = self.size + (self.target_size - self.size) * t

        self.update_speed()

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), int(self.size), int(self.size))

    def is_expired(self, current_time):
        return current_time - self.birth_time >= self.lifespan_ms

    def set_random_direction(self):
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

    def move(self, delta_time):
        old_center = self.center()

        self.x += self.vx * delta_time
        self.y += self.vy * delta_time

        wrapped = False

        if self.x > WIDTH:
            self.x = -self.size
            wrapped = True
        elif self.x + self.size < 0:
            self.x = WIDTH
            wrapped = True

        if self.y > HEIGHT:
            self.y = -self.size
            wrapped = True
        elif self.y + self.size < 0:
            self.y = HEIGHT
            wrapped = True

        if wrapped:
            self.trail.clear()
        else:
            self.trail.append(old_center)

        if len(self.trail) > TRAILS_LENGTH:
            self.trail.pop(0)

    def draw_trail(self, surface):
        for i in range(1, len(self.trail)):
            pygame.draw.line(surface, self.color, self.trail[i - 1], self.trail[i], 2)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.get_rect())

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

            if vector_length(flee_x, flee_y) > 0:
                flee_x, flee_y = normalize_vector(flee_x, flee_y)

                rand_angle = random.uniform(0, 2 * math.pi)
                final_x = flee_x + math.cos(rand_angle) * RANDOM_DIRECTION_STRENGTH
                final_y = flee_y + math.sin(rand_angle) * RANDOM_DIRECTION_STRENGTH

                final_x, final_y = normalize_vector(final_x, final_y)

                square.vx = final_x * square.speed
                square.vy = final_y * square.speed


def check_collision(a, b):
    return a.get_rect().colliderect(b.get_rect())


def vector_length(x, y):
    return math.hypot(x, y)


def normalize_vector(x, y):
    length = vector_length(x, y)
    return (0, 0) if length == 0 else (x / length, y / length)


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
                dist = vector_length(dx, dy)

                if dist > 0:
                    strength = 1 / dist
                    tx, ty = normalize_vector(dx, dy)
                    chase_x += tx * strength
                    chase_y += ty * strength

        if vector_length(chase_x, chase_y) > 0:
            chase_x, chase_y = normalize_vector(chase_x, chase_y)
            square.vx = chase_x * square.speed
            square.vy = chase_y * square.speed


def create_mixed_squares():
    return (
        [Square(25) for _ in range(5)] +
        [Square(10) for _ in range(10)] +
        [Square(4) for _ in range(30)]
    )


def handle_eating(squares):
    new = squares.copy()
    eaten = set()

    for i in range(len(squares)):
        for j in range(i + 1, len(squares)):
            if i in eaten or j in eaten:
                continue

            a, b = squares[i], squares[j]

            if check_collision(a, b):
                if a.size > b.size:
                    a.start_growth(b.size)
                    new[j] = Square(b.original_size)
                    eaten.add(j)
                elif b.size > a.size:
                    b.start_growth(a.size)
                    new[i] = Square(a.original_size)
                    eaten.add(i)

    return new


def main():
    squares = create_mixed_squares()
    font = pygame.font.SysFont("Arial", 18)

    running = True
    last_dir_change = pygame.time.get_ticks()

    while running:
        delta_time = CLOCK.tick(FPS) / 1000.0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        now = pygame.time.get_ticks()

        if now - last_dir_change >= DIRECTION_CHANGE_INTERVAL:
            for s in squares:
                s.set_random_direction()
            last_dir_change = now

        handle_chasing(squares)
        Square.handle_fleeing(squares)

        for s in squares:
            s.move(delta_time)
            s.update_growth(now)

        squares = handle_eating(squares)

        squares = [
            Square(s.original_size) if s.is_expired(now) else s
            for s in squares
        ]

        SCREEN.fill(BACKGROUND_COLOR)

        for s in squares:
            s.draw_trail(SCREEN)
        for s in squares:
            s.draw(SCREEN)

        fps_text = font.render(f"FPS: {CLOCK.get_fps():.1f}", True, FPS_COLOR)
        SCREEN.blit(fps_text, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()