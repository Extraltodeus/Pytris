#!/usr/bin/env python3
from os import environ, system
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from tetris import tetris
from random import randint
from time import sleep
from math import floor,ceil
from colorsys import hsv_to_rgb
from datetime import datetime

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h,s,v))

t = tetris()

class TextPrint:
    def __init__(self):
        self.font_size = 42
        self.font = pygame.font.Font(pygame.font.match_font('itwasntme'), self.font_size)
    def print(self, screen, textString, x=20, y=20, p=0):
        textBitmap = self.font.render(textString, True, WHITE)
        screen.blit(textBitmap, [x, y+int(self.font_size*p/1.2)])

pygame.init()
tp = TextPrint()
res    = 920
size   = [res, res]
screen = pygame.display.set_mode(size)
clock  = pygame.time.Clock()
fps    = 50
pygame.display.set_caption("Tetris")

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY  = (40,40,42)
BLUE  = (0,0,150)
DARK_GREY   = (30,30,30)
RED   = (100,50,50)

color_c = randint(0,1000)
c_c = hsv2rgb(color_c/1000,0.85,0.85)
c_b = hsv2rgb(color_c/1000,1,0.5)
colors = [GREY,c_c]

ym2  = 10
cell = floor((res-ym2*2) / t.Y)
ym   = floor((res-(cell * t.Y))/2)
xm   = floor((res-(cell * t.X))/2)

prevX = xm+cell*(t.X)+int(cell/2)
prevY = ym+cell

reserveX = xm-3*cell-int(cell/2)
reserveY = ym+cell

textY = ym+cell*5

margin = 4

surf1  = pygame.surface.Surface((cell*t.X+margin,cell*t.Y+margin))
surf1.set_alpha(125)


def print_stats():
    now = datetime.now().strftime("%H : %M : %S")
    pygame.draw.rect(screen,BLACK,(prevX-int(ym/2),prevY+4*cell*5-int(cell/1.5),300,tp.font_size*4))
    tp.print(screen,"Lines          : "+str(t.lines),prevX,prevY+4*cell*5-int(cell/2),0)
    tp.print(screen,"Score         : "+str(t.score),prevX,prevY+4*cell*5-int(cell/2),1)
    tp.print(screen,"Max score : "+str(t.max_score),prevX,prevY+4*cell*5-int(cell/2),2)
    tp.print(screen,now,prevX,prevY+4*cell*5-int(cell/2),3)
    # tp.print(screen,now,reserveX,prevY+4*cell*5-int(cell/2),2)
    # pygame.draw.rect(screen,BLACK,(reserveX-int(ym/2),prevY+4*cell*5-int(cell/1.5),125,tp.font_size*3))


def draw_grid():
    grid  = t.grids()
    ghost = t.ghost()
    pygame.draw.rect(screen,c_b,(xm-margin,ym-margin,cell*t.X+margin,cell*t.Y+margin))
    pygame.draw.rect(screen,BLACK,(xm,ym,cell*t.X-margin,cell*t.Y-margin))
    pygame.draw.rect(screen,RED,(xm,ym,cell*t.X-margin,cell*4))
    for y in range(t.Y):
            for x in range(t.X):
                x1 = x*cell+xm
                y1 = y*cell+ym
                if grid[y,x] >= 1:
                    col = c_c
                elif ghost[y,x] > 0:
                    col = BLUE
                elif y < 4:
                    col = DARK_GREY
                else:
                    col = GREY
                pygame.draw.rect(screen,col,(x1,y1,cell-margin,cell-margin))
    # pygame.draw.rect(surf1,c_b,(xm-margin,ym-margin,cell*t.X+margin,cell*t.Y+margin))

def show_preview_reserve(xo,yo,p):
    pygame.draw.rect(screen,BLACK,(xo,yo,cell*3,cell*4))
    for y in range(p[0][0]):
        for x in range(p[0][1]):
            x1 = x*cell+xo
            y1 = y*cell+yo
            if p[1][y,x] >= 1:
                pygame.draw.rect(screen,c_c,(x1,y1,cell-margin,cell-margin))
            # else:
            #     pygame.draw.rect(screen,colors[0],(x1,y1,cell-margin,cell-margin))

def move_with_mouse(pos):
    sl = ((res/cell - xm/cell) * (pos[0]-xm)/cell)/(cell/2)
    if pos[0] > xm/2 and pos[0] < res-xm/2:
        if t.left > int(sl) :
            t.move_tetromino(-1)
        if t.left < int(sl) :
            t.move_tetromino(1)

def colorcycle():
    global color_c,colors,c_c,c_b
    max_c = ceil(t.get_speed()*t.get_speed()/15)+30
    if color_c < max_c:
        color_c = color_c +1
    else :
        color_c = 0
    c_c = hsv2rgb(color_c/max_c,0.85,0.90)
    c_b = hsv2rgb((max_c-color_c)/max_c,0.85,0.7)

def run_game():
    move = 0
    adv  = 1
    done = False
    iter = 0
    while not done:
        iter += 1
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            # move_with_mouse(pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                t.pause = False
                if event.button == 1:
                    t.rotate_tetromino()
                elif event.button == 2:
                    t.fast_fall()
                elif event.button == 3:
                    t.rotate_tetromino(3)
                elif event.button == 4:
                    t.swap_reserve()
                elif event.button == 5:
                    t.advance()
                    t.refresh()

            if event.type == pygame.KEYDOWN:
                t.pause = False
                if event.key == pygame.K_ESCAPE:
                    done=True
                elif event.key == pygame.K_SPACE:
                    if t.pause == False:
                        t.pause = True
                    else:
                        t.pause = False
                elif event.key == pygame.K_r:
                    t.reset_game()
                elif event.key == pygame.K_a or event.key == pygame.K_RCTRL:
                    t.swap_reserve()
                elif event.key == pygame.K_d or event.key == pygame.K_KP0:
                    t.rotate_tetromino(3)
                elif event.key == pygame.K_s:
                    t.rotate_tetromino()
                elif event.key == pygame.K_w:
                    t.rotate_tetromino(2)
                elif event.key == pygame.K_UP or event.key == pygame.K_y:
                    t.fast_fall()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_x:
                    move = 1
                    iter = 0
                    t.move_tetromino(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_c:
                    move = 1
                    iter = 0
                    t.move_tetromino()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if iter % 6 == 0:
                if move == 0:
                    t.move_tetromino(-1)
                else:
                    move = 0
        if keys[pygame.K_RIGHT]:
            if iter % 6 == 0:
                if move == 0:
                    t.move_tetromino()
                else:
                    move = 0
        if keys[pygame.K_DOWN]:
            if iter % 3 == 0:
                adv = 0
                t.advance()
                t.refresh()

        if t.pause == False:
            if iter % t.get_speed() == 0 and adv == 1:
                t.advance()
            if adv == 0:
                adv = 1
            colorcycle()
            t.refresh()
        if not t.pause :
            draw_grid()
        show_preview_reserve(reserveX,reserveY,t.show_reserve())
        for i in range(0,4):
            show_preview_reserve(prevX,prevY+i*cell*5,t.preview(i))

        # t.print_grid()
        # screen.blit(surf1, (xm-margin, ym-margin))
        print_stats()
        pygame.display.update()
        clock.tick(fps)

if __name__ == '__main__':
    run_game()
