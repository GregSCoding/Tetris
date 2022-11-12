import random
import pygame
from helpers_pygame import random_color
from copy import deepcopy

TILE_SIZE = 25
WIDTH = 12
HEIGHT = 25
GRAY = (80, 80, 80)
FPS = 60
pygame.init()
display = pygame.display.set_mode(size=(TILE_SIZE*WIDTH, TILE_SIZE*HEIGHT))
clock = pygame.time.Clock()

current_fig = None
figure_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
dx, dy = 0, 0
FALL_SPEED, FALL_LIMIT, FALL_COUNT = 60, 2000, 0
class Figure:
    figures_positions = [[(0, 0), (1, 0), (2, 0), (3, 0)],
                     [(0, 0), (1, 0), (0, -1), (1, -1)],
                     [(0, 0), (1, 0), (0, 1), (1, -1)],
                     [(0, 0), (1, 0), (1, 1), (0, -1)],
                     [(0, 0), (1, 0), (2, 0), (1, -1)]]
    figures = [[pygame.Rect((x + WIDTH//2), y + 1, TILE_SIZE, TILE_SIZE) for x,y in fig_pos] for fig_pos in figures_positions]
    def __init__(self):
        self.figure = random.choice(Figure.figures)
        self.colors = [random_color() for i in range(4)]
def process_events():
    global current_fig, dx, dy, FALL_SPEED, FALL_LIMIT, FALL_COUNT
    if not current_fig:
        current_fig = Figure()
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx -= 1
                    elif event.key == pygame.K_RIGHT:
                        dx += 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        FALL_LIMIT = 200
    else:
        FALL_LIMIT = 2000
    if FALL_COUNT > FALL_LIMIT:
        dy += 1
        FALL_COUNT = 0
    FALL_COUNT += 60
                
def draw_grid():
    for i in range(WIDTH):
        for j in range(HEIGHT):
            pygame.draw.rect(display, GRAY, pygame.Rect(TILE_SIZE*i, TILE_SIZE*j, TILE_SIZE, TILE_SIZE), width=1)

def draw_figure(figure):
    global dx, dy
    old_figure = deepcopy(figure.figure)
    for part in figure.figure:
        part.x += dx
        part.y += dy
        if part.x >= WIDTH or part.x < 0:
            figure.figure = deepcopy(old_figure)
            break
    for part in figure.figure:
        pass
    dx = 0
    dy = 0
    for part, color in zip(figure.figure, figure.colors):
        figure_rect.x = part.x * TILE_SIZE
        figure_rect.y = part.y * TILE_SIZE
        pygame.draw.rect(display, color, figure_rect)

def main():
    while True:
        process_events()
        display.fill((pygame.Color("black")))
        draw_figure(current_fig)
        draw_grid()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()