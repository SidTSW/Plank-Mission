import pygame
import csv
import random
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cosmic Symphony: CMB Data Visualizer")
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 10)
PURPLE = (160, 100, 255)
CYAN = (100, 255, 255)
ORANGE = (255, 180, 100)
WHITE = (255, 255, 255)

# Load CMB flux data for visual intensity
data = []
try:
    with open("planck_cleaned (1).csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                flux = float(row.get('flux', 1.0))
            except:
                flux = random.uniform(0.5, 1.5)
            data.append(flux)
except FileNotFoundError:
    print("Warning: cleaned_data.csv not found, using random data.")
    data = [random.uniform(0.5, 2.0) for _ in range(1000)]

# Normalize flux
max_flux = max(data)
data = [val / max_flux for val in data]

# Particle system
particles = []
for i in range(800):
    radius = random.uniform(50, WIDTH//2)
    angle = random.uniform(0, math.tau)
    speed = random.uniform(0.0006, 0.002)
    depth = random.uniform(0.3, 1.0)
    brightness = random.choice(data)
    particles.append([radius, angle, speed, depth, brightness])

# Nebula fog effect using transparent surfaces
fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for _ in range(300):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(50, 150)
    alpha = random.randint(10, 40)
    color = (random.randint(100, 255), random.randint(50, 150), random.randint(200, 255), alpha)
    pygame.draw.circle(fog, color, (x, y), size)

# Starfield (background)
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)] for _ in range(150)]

running = True
t = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    t += 1
    screen.fill(BLACK)

    # Twinkling stars
    for sx, sy, sr in stars:
        color_shift = 200 + int(55 * math.sin(t * 0.05 + sx))
        pygame.draw.circle(screen, (color_shift, color_shift, 255), (sx, sy), sr)

    # Nebula layer
    screen.blit(fog, (0, 0))

    # Galaxy core glow
    for i in range(200, 0, -5):
        pygame.draw.circle(screen, (255, 240 - i, 240 - i), (WIDTH//2, HEIGHT//2), i, width=2)

    # Spiral galaxy particles
    for p in particles:
        r, a, s, d, b = p
        a += s
        p[1] = a

        # spiral arm distortion
        arm_offset = math.sin(a * 2 + d * 3) * 100 * d
        x = WIDTH//2 + (r + arm_offset) * math.cos(a)
        y = HEIGHT//2 + (r + arm_offset) * math.sin(a)

        # brightness-based color
        color_intensity = min(255, int(150 + 100 * b))
        color = (color_intensity, int(80 + 100 * d), 255 - int(100 * d))

        size = max(1, int(3 * d))
        pygame.draw.circle(screen, color, (int(x), int(y)), size)

    # Floating cosmic dust particles
    for _ in range(3):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, (255, 255, 255), (x, y), 1)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
