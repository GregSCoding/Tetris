import random
import pygame
from helpers_pygame import *
from copy import deepcopy
score = 0
TILE_SIZE = 25
WIDTH = 12
HEIGHT = 25
INTERFACE_WIDTH = 7
GRAY = (80, 80, 80)
FPS = 60
pygame.init()
display = pygame.display.set_mode(size=(TILE_SIZE*(WIDTH + INTERFACE_WIDTH), TILE_SIZE*HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
figure_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)

        
    
class Figure:
    FALL_SPEED, FALL_LIMIT, FALL_COUNT = 60, 2000, 0
    figures_positions = [[(1, 0), (0, 0), (2, 0), (3, 0)],
                     [(1, 0), (0, 0), (0, -1), (1, -1)],
                     [(0, 0), (1, 0), (0, 1), (1, -1)],
                     [(0, 0), (1, 0), (1, 1), (0, -1)],
                     [(1, 0), (0, 0), (2, 0), (1, -1)],
                     [(1, 0), (0, 0), (2, 0), (2, 1)],
                     [(1, 0), (0, 0), (2, 0), (0, 1)]]
    figures = [[pygame.Rect((x + WIDTH//2), y, TILE_SIZE, TILE_SIZE) for x,y in fig_pos] for fig_pos in figures_positions]
    figures_next = [[pygame.Rect((WIDTH + 2 + x), y + 4, TILE_SIZE, TILE_SIZE) for x,y in fig_pos] for fig_pos in figures_positions]
    def __init__(self, figure_idx):
        self.figure = deepcopy(Figure.figures[figure_idx])
        self.colors = [random_color() for i in range(4)]
        self.next_figure = Next_figure()
    def rotate(self, field):
        old_figure = deepcopy(self.figure)
        centerx = self.figure[0].x
        centery = self.figure[0].y
        for rect in self.figure:
            x = rect.x
            y = rect.y
            newx = -(y - centery) + centerx
            newy = (x - centerx) + centery
            if newx >= WIDTH or newx < 0 or newy >= HEIGHT or field[newy][newx]:
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
            if part.y == HEIGHT or field[part.y][part.x]:
                self.figure = deepcopy(old_figure)
                for part, color in zip(self.figure, self.colors):
                    field[part.y][part.x] = color
                check_rows(field)
                self.change_to_next()
                return
    def change_to_next(self):
        self.figure = deepcopy(Figure.figures[self.next_figure.idx])
        self.colors = self.next_figure.colors
        self.next_figure.__init__()
    def draw_figure(self):
            for part, color in zip(self.figure, self.colors):
                figure_rect.x = part.x * TILE_SIZE
                figure_rect.y = part.y * TILE_SIZE
                pygame.draw.rect(display, color, figure_rect)
class Next_figure(Figure):
    def __init__(self):
        self.idx = random.randrange(0, len(Figure.figures_next))
        self.figure = Figure.figures_next[self.idx]
        self.colors = [random_color() for i in range(4)]
def all_filed(field):
    for row in field:
        if not all(row):
            return False
    return True
def fill_anim(field):
    anim_field = deepcopy(field)
    draw_grid()
    while not all_filed(anim_field):
        i = random.randrange(0, HEIGHT)
        j = random.randrange(0, WIDTH)
        while all(anim_field[i]):
            i = random.randrange(0, HEIGHT)
        while anim_field[i][j] != None:
            j = random.randrange(0, WIDTH)
        anim_field[i][j] = random_color()
        draw_field(anim_field)
        draw_grid()
        pygame.display.flip()
        pygame.time.wait(6)
    pygame.time.wait(1000)
    
    pygame.display.flip()
def game_over(field):
    global high_score
    fill_anim(field)
    display_text(display, WIDTH//2*TILE_SIZE, HEIGHT//2*TILE_SIZE, "--GAME OVER--", txt_size=38, txt_color=pygame.Color("white"))
    pygame.display.flip()
    if score > high_score:
        save_higscore(score)
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
def check_rows(field):
    flag = False
    global score
    multi = 0
    if any(field[0]):
        game_over(field)
    old_field = deepcopy(field)
    for i, row in enumerate(field):
        if all(row):
            multi += 1
            flag = True
            old_field[i] = [pygame.Color("white") for i in range(WIDTH)]
            del(field[i])
            field.insert(0, [None for i in range(WIDTH)])
    if flag:
        score += 100*multi**2
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
                    elif event.key == pygame.K_ESCAPE:
                        pause()
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
    # Loop for drawing the grid for the gameplay
    for i in range(WIDTH):
        for j in range(HEIGHT):
            pygame.draw.rect(display, GRAY, pygame.Rect(TILE_SIZE*i, TILE_SIZE*j, TILE_SIZE, TILE_SIZE), width=1)
    # Loop for drawing the grid for the next piece
    for i in range(1, INTERFACE_WIDTH-1):
        for j in range(4):
            pygame.draw.rect(display, GRAY, pygame.Rect(TILE_SIZE*(i + WIDTH), TILE_SIZE*(j+2), TILE_SIZE, TILE_SIZE), width=1)
def draw_field(field):
    for i, row in enumerate(field):
        for j in range(WIDTH):
            if row[j]:
                color = row[j]
                figure_rect.x = j * TILE_SIZE
                figure_rect.y = i * TILE_SIZE
                pygame.draw.rect(display, color, figure_rect)        
def pause():
    display_text(display, WIDTH//2*TILE_SIZE, HEIGHT//2*TILE_SIZE, "--PAUSED--", txt_size=32)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
def save_higscore(score):
    with open("save.txt", "w") as f:
        f.write(str(score))
def load_highscore():
    with open("save.txt", "r+") as f:
        high_score = f.readline()
        if not high_score:
            high_score = 0
            f.write(str(high_score))
            return high_score
        else:
            return int(high_score)
def draw_score(high_score):
    display_text(display, (WIDTH+INTERFACE_WIDTH//2)*TILE_SIZE, (-5+HEIGHT//2)*TILE_SIZE, "Score:", txt_size=24, txt_color=pygame.Color("yellow"))
    display_text(display, (WIDTH+INTERFACE_WIDTH//2)*TILE_SIZE, (-4+HEIGHT//2)*TILE_SIZE, str(score) , txt_size=24, txt_color=pygame.Color("yellow"))
    display_text(display, (WIDTH+INTERFACE_WIDTH//2)*TILE_SIZE, (-3+HEIGHT//2)*TILE_SIZE, "Highscore:" , txt_size=24, txt_color=pygame.Color("yellow"))
    display_text(display, (WIDTH+INTERFACE_WIDTH//2)*TILE_SIZE, (-2+HEIGHT//2)*TILE_SIZE, str(high_score) , txt_size=24, txt_color=pygame.Color("yellow"))
def main():
    global high_score 
    high_score = load_highscore()
    field = [[None for i in range(WIDTH)] for j in range(HEIGHT)]
    current_fig = Figure(random.randrange(0, len(Figure.figures)))
    while True:
        process_events(current_fig, field)
        display.fill((pygame.Color("black")))
        current_fig.draw_figure()
        current_fig.next_figure.draw_figure()
        draw_field(field)
        draw_grid()
        draw_score(high_score)
        pygame.display.flip()
        clock.tick(FPS)
if __name__ == "__main__":
    main()