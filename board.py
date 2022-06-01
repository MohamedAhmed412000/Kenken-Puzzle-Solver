import pygame
import os

class Board:
    def __init__(self, solver = 'user', n = 3, algorithm = 'BT'):
        self.solver = solver
        self.N = n
        self.algorithm = algorithm
        self.WIDTH = 550
        self.BG_COLOR = (251, 247, 245)
        self.LINE_COLOR = (0, 0, 0)
        self.NUM_COLOR = (10, 10, 10)
        self.LOWER_NUM_COLOR = (52, 31, 151)
        self.MARGIN = (self.WIDTH - 100) / self.N
        self.BOARD = [[0 for _ in range(self.N)] for _ in range(self.N)]
        self.continous = False
        
    def set_inputs(self, filepath: str):
        OP = {'add': '+', 'sub': '-', 'mul': '*', 'div': '\\', "''": ''}
        fh = open(f'Input/{filepath}', 'r')
        lines = fh.readlines()
        fh.close()
        self.N = int(lines[0])
        self.grid = []
        for line in lines[1:]:
            k, op, v = line.strip().split(' ')
            v = f'{v}{OP[op]}'
            cells = k[1:-1].replace('),(', '-').replace('(', '').replace(')', '').split('-')
            vals = []
            for cell in cells:
                x, y = cell.split(',')
                val = int(x) * self.N + int(y) + 1
                vals.append(val)
            self.grid.append([v, vals])
        self.MARGIN = (self.WIDTH - 100) / self.N
        self.BOARD = [[0 for i in range(self.N)] for j in range(self.N)]
        return self.N, self.grid

    def get_inputs(self, grid):
        self.grid = grid

    def coordinates(self, x, y):
        return ((50+(x-1)*self.MARGIN, 50+(y-1)*self.MARGIN), (50+(x-1)*self.MARGIN, 50+y*self.MARGIN)),\
                ((50+x*self.MARGIN, 50+(y-1)*self.MARGIN), (50+x*self.MARGIN, 50+y*self.MARGIN)),\
                ((50+(x-1)*self.MARGIN, 50+(y-1)*self.MARGIN), (50+x*self.MARGIN, 50+(y-1)*self.MARGIN)),\
                ((50+(x-1)*self.MARGIN, 50+y*self.MARGIN), (50+x*self.MARGIN, 50+y*self.MARGIN))

    
    def clear(self, win, x, y):
        if x < 0 or x >= self.N or y < 0 or y >= self.N:
            return
        pygame.draw.rect(win, self.BG_COLOR, (50+(x+0.5)*self.MARGIN, 50+(y+0.4)*self.MARGIN, 0.5*self.MARGIN-10, 0.6*self.MARGIN-10))
        pygame.display.update()
        return

    def insert(self, win, x, y):
        if x < 0 or x >= self.N or y < 0 or y >= self.N:
            return
        FONT = pygame.font.SysFont("Verdana", (10-self.N)*5+7)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if 0 < event.key - 48 < self.N + 1:
                        self.BOARD[y][x] = event.key - 48
                        pygame.draw.rect(win, self.BG_COLOR, (50+(x+0.5)*self.MARGIN, 50+(y+0.4)*self.MARGIN, 0.5*self.MARGIN-10, 0.6*self.MARGIN-10))
                        text = FONT.render(str(self.BOARD[y][x]), True, self.LOWER_NUM_COLOR)
                        win.blit(text, (50+self.MARGIN*(x+0.5), 50+self.MARGIN*(y+0.35)))
                        pygame.display.update()
                        # print(self.BOARD)
                        if self.soln == self.BOARD:
                            print('game Solved')
                            return True
                        return False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        return self.insert(win, int((pos[0]-50)//self.MARGIN), int((pos[1]-50)//self.MARGIN))
                    if event.button == 3:
                        self.clear(win, int((pos[0]-50)//self.MARGIN), int((pos[1]-50)//self.MARGIN))

    def close(self):
        pygame.quit()
    
    def fill_board(self, win, soln):
        FONT = pygame.font.SysFont("Verdana", (10-self.N)*5+7)
        for i in range(len(soln)):
            for j in range(len(soln[i])):
                text = FONT.render(str(soln[i][j]), True, self.LOWER_NUM_COLOR)
                win.blit(text, (50+self.MARGIN*(j+0.5), 50+self.MARGIN*(i+0.35)))
                pygame.display.update()
    
    def set_output(self, soln):
        self.soln = soln
                
    def run(self, soln = ''):
        self.close()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "700,100"
        pygame.init()
        screen = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        pygame.display.set_caption("Kenken")
        screen.fill(self.BG_COLOR)
        FONT = pygame.font.SysFont("Comic Sans MS", (10-self.N)*5)
        # grid lines
        for i in range(self.N+1):
            width = 2
            if i % self.N == 0:
                width = 4
            pygame.draw.line(screen, self.LINE_COLOR, (50+self.MARGIN*i, 50), (50+self.MARGIN*i, 500), width)
            pygame.draw.line(screen, self.LINE_COLOR, (50, 50+self.MARGIN*i), (500, 50+self.MARGIN*i), width)
        # grid
        border = {}
        for item in self.grid:
            dimensions = {}
            for i in item[1]:
                l, r, n, s = self.coordinates((i-1)%self.N+1, (i-1)//self.N+1)
                for element in [l, r, n, s]:
                    if element not in dimensions.keys():
                        dimensions[element] = 1
                    else:
                        dimensions[element] += 1
                if i == min(item[1]):
                    text = FONT.render(item[0], True, self.NUM_COLOR)
                    screen.blit(text, (50+self.MARGIN*((i-1)%self.N) + 7, 50+self.MARGIN*((i-1)//self.N)))
            for k, v in dimensions.items():
                if v == 1:
                    border[k] = dimensions[k]

        for k, v in border.items():
            if v == 1:
                pygame.draw.line(screen, self.LINE_COLOR, k[0], k[1], 5)
        self.continous = True

        pygame.display.update()

        if soln != '':
            self.fill_board(screen, soln)

        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.WINDOWRESTORED:
                    pygame.display.update()
                if event.type == pygame.MOUSEBUTTONUP and self.continous:
                    if self.solver == 'user':
                        pos = pygame.mouse.get_pos()
                        if event.button == 1:
                            check = self.insert(screen, int((pos[0]-50)//self.MARGIN), int((pos[1]-50)//self.MARGIN))
                            if check:
                                FONT = pygame.font.SysFont("Verdana", 23)
                                text = FONT.render("Game Solved", True, (255, 0, 0))
                                screen.blit(text, (200, 10))
                                pygame.display.update()
                                self.continous = False
                        if event.button == 3:
                            self.clear(screen, int((pos[0]-50)//self.MARGIN), int((pos[1]-50)//self.MARGIN))


