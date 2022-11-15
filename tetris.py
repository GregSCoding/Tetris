import random
import pygame
from helpers_pygame import random_color
from copy import deepcopy

TILE_SIZE = 25
WIDTH = 8
HEIGHT = 25
GRAY = (80, 80, 80)
FPS = 60
pygame.init()
display = pygame.display.set_mode(size=(TILE_SIZE*WIDTH, TILE_SIZE*HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
figure_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)

class Figure:
    FALL_SPEED, FALL_LIMIT, FALL_COUNT = 60, 2000, 0
    figures_positions = [[(1, 0), (0, 0), (2, 0), (3, 0)],
                     [(1, 0), (0, 0), (0, -1), (1, -1)],
                     [(0, 0), (1, 0), (0, 1), (1, -1)],
                     [(0, 0), (1, 0), (1, 1), (0, -1)],
                     [(0, 0), (1, 0), (2, 0), (1, -1)],
                     [(1, 0), (0, 0), (2, 0), (2, 1)],
                     [(1, 0), (0, 0), (2, 0), (1, -1)]]
    figures = [[pygame.Rect((x + WIDTH//2), y + 1, TILE_SIZE, TILE_SIZE) for x,y in fig_pos] for fig_pos in figures_positions]
    def __init__(self):
        #self.figure =deepcopy(Figure.figures[0])
        self.figure =deepcopy(random.choice(Figure.figures))
        self.colors = [random_color() for i in range(4)]
    def rotate(self, field):
        old_figure = deepcopy(self.figure)
        centerx = self.figure[0].x
        centery = self.figure[0].y
        for rect in self.figure:
            x = rect.x
            y = rect.y
            newx = -(y - centery) + centerx
            newy = (x - centerx) + centery
            if newx >= WIDTH or newx < 0 or newy >= HEIGHT or newy < 0 or field[newy][newx]:
                self.figure = old_figure
                return
            rect.x = newx
            rect.y = newy
    def move_hori(self, dx, field):
        old_figure = deepcopy(self.figure)
        for part in self.figure:
            part.x += dx
            if part.x >= WIDTH or part.x < 0 or field[part.y][part.x]:
                self.figure = deepcopy(old_figure)
                return
    def move_verti(self, field):
        old_figure = deepcopy(self.figure)
        for part in self.figure:
            part.y += 1
            if part.y == HEIGHT or field[part.y][part.x] :
                self.figure = deepcopy(old_figure)
                for part, color in zip(self.figure, self.colors):
                    field[part.y][part.x] = color
                check_rows(field)
                self.__init__()
                return
    def draw_figure(self):
            for part, color in zip(self.figure, self.colors):
                figure_rect.x = part.x * TILE_SIZE
                figure_rect.y = part.y * TILE_SIZE
                pygame.draw.rect(display, color, figure_rect)
def check_rows(field):
    flag = False
    old_field = deepcopy(field)
    for i, row in enumerate(field):
        if all(row):
            flag = True
            old_field[i] = [(255,255,255) for i in range(WIDTH)]
            del(field[i])
            field.insert(0, [None for i in range(WIDTH)])
    if flag:
        draw_field(old_field)
        draw_grid()
        pygame.display.flip()
        pygame.time.wait(400)
def process_events(current_fig, field):
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_fig.move_hori(-1, field)
                    elif event.key == pygame.K_RIGHT:
                        current_fig.move_hori(1, field)
                    elif event.key == pygame.K_UP:
                        current_fig.rotate(field)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        Figure.FALL_LIMIT = 200
    else:
        Figure.FALL_LIMIT = 2000
    if Figure.FALL_COUNT > Figure.FALL_LIMIT:
        Figure.FALL_COUNT = 0
        current_fig.move_verti(field)
    Figure.FALL_COUNT += 60
def draw_grid():
    for i in range(WIDTH):
        for j in range(HEIGHT):
            pygame.draw.rect(display, GRAY, pygame.Rect(TILE_SIZE*i, TILE_SIZE*j, TILE_SIZE, TILE_SIZE), width=1)
def draw_field(field):
    for i, row in enumerate(field):
        for j in range(WIDTH):
            if row[j]:
                color = row[j]
                figure_rect.x = j * TILE_SIZE
                figure_rect.y = i * TILE_SIZE
                pygame.draw.rect(display, color, figure_rect)        
def main():
    field = [[None for i in range(WIDTH)] for j in range(HEIGHT)]
    current_fig = Figure()
    while True:
        process_events(current_fig, field)
        display.fill((pygame.Color("black")))
        current_fig.draw_figure()
        draw_field(field)
        draw_grid()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()