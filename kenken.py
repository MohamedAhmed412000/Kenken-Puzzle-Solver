import pygame
from input import N, grid

WIDTH = 550
BG_COLOR = (251, 247, 245)
LINE_COLOR = (0, 0, 0)
NUM_COLOR = (52, 31, 151)
LOWER_NUM_COLOR = (52, 31, 151)
MARGIN = (WIDTH - 100) / N
BOARD = [[0 for i in range(N)] for j in range(N)]

def coordinates(x, y):
    return ((50+(x-1)*MARGIN, 50+(y-1)*MARGIN), (50+(x-1)*MARGIN, 50+y*MARGIN)), \
            ((50+x*MARGIN, 50+(y-1)*MARGIN), (50+x*MARGIN, 50+y*MARGIN)), \
            ((50+(x-1)*MARGIN, 50+(y-1)*MARGIN), (50+x*MARGIN, 50+(y-1)*MARGIN)), \
            ((50+(x-1)*MARGIN, 50+y*MARGIN), (50+x*MARGIN, 50+y*MARGIN))

def clear(win, x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return
    pygame.draw.rect(win, BG_COLOR, (100+x*MARGIN, 100+y*MARGIN, MARGIN-60, MARGIN-60))
    pygame.display.update()
    return

def insert(win, x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return
    FONT = pygame.font.SysFont("Comic Sans MS", 20 + 10 * N)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if 0 < event.key - 48 < N + 1:
                    BOARD[x][y] = event.key - 48
                    pygame.draw.rect(win, BG_COLOR, (100+x*MARGIN, 100+y*MARGIN, MARGIN-60, MARGIN-60))
                    text = FONT.render(str(BOARD[x][y]), True, NUM_COLOR)
                    win.blit(text, (50+MARGIN*(x+0.5), 50+MARGIN*(y+0.35)))
                    pygame.display.update()
                    return
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    insert(win, int((pos[0]-50)//MARGIN), int((pos[1]-50)//MARGIN))
                if event.button == 3:
                    clear(win, int((pos[0]-50)//MARGIN), int((pos[1]-50)//MARGIN))

            

def main(grid):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Kenken")
    screen.fill(BG_COLOR)
    FONT = pygame.font.SysFont("Comic Sans MS", 20 + 5 * N)

    # grid lines
    for i in range(N+1):
        width = 2
        if i % N == 0:
            width = 4
        pygame.draw.line(screen, LINE_COLOR, (50+MARGIN*i, 50), (50+MARGIN*i, 500), width)
        pygame.draw.line(screen, LINE_COLOR, (50, 50+MARGIN*i), (500, 50+MARGIN*i), width)

    # grid
    border = {}
    for item in grid:
        dimensions = {}
        for i in item[1]:
            l, r, n, s = coordinates((i-1)%N+1, (i-1)//N+1)
            for element in [l, r, n, s]:
                if element not in dimensions.keys():
                    dimensions[element] = 1
                else:
                    dimensions[element] += 1
            if i == min(item[1]):
                text = FONT.render(item[0], True, NUM_COLOR)
                screen.blit(text, (50+MARGIN*((i-1)%N) + 7, 50+MARGIN*((i-1)//N)))
        for k, v in dimensions.items():
            if v == 1:
                border[k] = dimensions[k]

    for k, v in border.items():
        if v == 1:
            pygame.draw.line(screen, LINE_COLOR, k[0], k[1], 4)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.WINDOWRESTORED:
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if event.button == 1:
                    insert(screen, int((pos[0]-50)//MARGIN), int((pos[1]-50)//MARGIN))
                if event.button == 3:
                    clear(screen, int((pos[0]-50)//MARGIN), int((pos[1]-50)//MARGIN))

main(grid)