from os import system
from random import shuffle
from math import floor,ceil
import numpy as np

class tetris():
    def __init__(self):
        self.max_speed = 110
        self.fast  = 0
        self.lines = 0
        self.max_lines = 0
        self.score = 0
        self.max_score = 0
        self.X = 10
        self.Y = 24
        self.shape = (self.Y,self.X)
        self.gp = self.new_grid(self.shape)
        self.gt = self.new_grid(self.shape)
        self.gh = self.new_grid(self.shape)
        t = np.array([[1,1,1],[0,1,0]])
        c = np.array([[1,1],[1,1]])
        i = np.array([[1],[1],[1],[1]])
        l = np.array([[1,0],[1,0],[1,1]])
        j = np.array([[0,1],[0,1],[1,1]])
        s = np.array([[0,1,1],[1,1,0]])
        z = np.array([[1,1,0],[0,1,1]])
        self.tetrominos = [t,c,i,l,j,s,z]
        self.reset_game()
        self.pause = False

    def new_grid(self,shape):
        return np.zeros(shape, dtype='int32')

    def generate_tetrominos(self):
        self.pretetrominos = []
        for x in range(3000):
            pretetrominos = list(range(0, len(self.tetrominos)))*3
            shuffle(pretetrominos)
            self.pretetrominos.extend(pretetrominos)

    def reset_position(self):
        self.left = floor(self.shape[1]/2)-ceil(self.t.shape[1]/2)
        self.down = 0

    def new_tetromino(self):
        i = self.pretetrominos[self.tetrominos_index]
        self.reserve_cache_2 = i
        self.tetrominos_index += 1
        self.t = self.tetrominos[i]
        self.reset_position()
        self.reserve_lock   = 0
        self.reserve_lock2 -= 1

    def swap_reserve(self):
        if self.reserve_lock == 0 and self.reserve_lock2 <= 0:
            self.reserve_lock = 1
            self.reserve_cache_1 = self.reserve
            self.reserve = self.reserve_cache_2
            if self.reserve_cache_1 != 8:
                self.t = self.tetrominos[self.reserve_cache_1]
                self.reset_position()
            else:
                self.reserve_lock2 = 2
                self.new_tetromino()

    def show_reserve(self):
        if self.reserve == 8:
            return self.new_grid((3,3))
        return [self.tetrominos[self.reserve].shape, self.tetrominos[self.reserve]]

    def rotate_tetromino(self,r=1):
        ft = np.rot90(np.copy(self.t),r)
        s  = self.get_slice(ft.shape)
        if s[3] <= self.X and s[1] <= self.Y:
            if not self.check_contact(s,ft):
                self.t = np.rot90(self.t,r)

    def move_tetromino(self,m=1):
        ft = np.copy(self.t)
        s = self.get_slice(ft.shape,0,m)
        if s[2] >= 0 and s[3] <= self.X:
            if not self.check_contact(s,self.t):
                self.left = self.left + m

    def fast_fall(self):
        self.fast = 1
        while self.fast == 1:
            self.advance()
            self.refresh()

    def register_tetromino(self,f=0):
        s = self.get_slice(self.t.shape,f)
        self.gp[s[0]:s[1],s[2]:s[3]] += self.t
        self.fast = 0
        self.check_line()
        self.check_game_over()
        self.new_tetromino()

    def ghost(self):
        self.gh = self.new_grid(self.shape)
        for x in range(0,self.Y):
            s = self.get_slice(self.t.shape,f=x)
            if s[1]<self.Y:
                if self.check_contact(s,self.t) :
                    self.gh[s[0]-1:s[1]-1,s[2]:s[3]] += self.t
                    return self.gh
            else:
                if self.check_contact(s,self.t) :
                    self.gh[s[0]-1:s[1]-1,s[2]:s[3]] += self.t
                    return self.gh
                else:
                    self.gh[s[0]:s[1],s[2]:s[3]] += self.t
                    return self.gh

    def get_speed(self):
        speed = self.max_speed-floor(self.lines/1.5)
        if speed < 2:
            speed = 2
        return speed

    def check_line(self):
        total_lines = 0
        for l, i in enumerate(self.gp):
            if sum(i) == self.X:
                self.gp[1:l+1, 0:self.X] = self.gp[0:l, 0:self.X]
                self.lines  += 1
                total_lines += 1
        self.score += total_lines*total_lines
        if self.lines > self.max_lines : self.max_lines = self.lines
        if self.score > self.max_score : self.max_score = self.score

    def reset_game(self):
        self.gp = self.new_grid(self.shape)
        self.gt = self.new_grid(self.shape)
        self.reserve          = 8
        self.reserve_lock     = 0
        self.reserve_lock2    = 0
        self.reserve_cache_1  = 0
        self.reserve_cache_2  = 8
        self.tetrominos_index = 0
        self.game_over        = False
        self.generate_tetrominos()
        self.new_tetromino()
        self.lines = 0
        self.score = 0
        self.pause = True

    def check_game_over(self):
        danger_zone = self.gp[0:4,0:self.X]
        if np.amax(danger_zone) > 0:
            self.game_over = True
            self.reset_game()

    def check_eol(self,f=0):
        if (self.down+f) > (self.shape[0]-self.t.shape[0]):
            self.register_tetromino(-1)

    def check_contact(self,s,piece):
        if not self.check_eol():
            t =  np.copy(piece)
            t += np.copy(self.gp[s[0]:s[1],s[2]:s[3]])
            return np.amax(t) > 1

    def get_slice(self,shape,f=0,m=0):
        return [self.down+f,
                self.down+f+shape[0],
                self.left+m,
                self.left+m+shape[1]]

    def advance(self):
        self.down += 1

    def refresh(self):
        self.check_eol()
        if self.check_contact(self.get_slice(self.t.shape),self.t):
            self.register_tetromino(-1)
        self.gt = np.copy(self.gp)
        s = self.get_slice(self.t.shape)
        self.gt[s[0]:s[1],s[2]:s[3]] += self.t

    def grids(self):
        return np.copy(self.gp) + np.copy(self.gt)

    def preview(self,d=0):
        i = self.pretetrominos[self.tetrominos_index+d]
        return [self.tetrominos[i].shape,self.tetrominos[i]]

    def print_grid(self):
        system("clear")
        print(self.gt)
        print("Lines :", self.lines)
        print("Score :", self.score)
