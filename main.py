import pygame
import time

width = 800
height = 600
cellSize = 5

xCellCount = int(width / cellSize)
yCellCount = int(height / cellSize)

aliveCells = {}

def DrawCells():
    for cell in aliveCells:
        rect = pygame.Rect(cell[0] * cellSize, cell[1] * cellSize, cellSize, cellSize)
        pygame.draw.rect(screen, "white", rect)


def CreateCell(x, y):
    aliveCells[(x, y)] = 1

def KillCell(x, y):
    aliveCells.pop((x, y), 0)

def IsCellAlive(x, y):
    if (x, y) in aliveCells:
        return 1

def GetFieldCount(x, y):
    x = x - 1
    y = y - 1
    count = 0
    for i in range(3):
        for j in range(3):
            if IsCellAlive(x + j, y + i):
                count += 1
    return count


def Glider():
    CreateCell(39,27)
    CreateCell(40,28)
    CreateCell(38,29)
    CreateCell(39,29)
    CreateCell(40,29)

def ManyGliders(amount):
    offset = 5
    for i in range(amount):
        for j in range(amount):
            CreateCell(1 + (offset * i), 0 + (offset * j))
            CreateCell(2 + (offset * i), 1 + (offset * j))
            CreateCell(0 + (offset * i), 2 + (offset * j))
            CreateCell(1 + (offset * i), 2 + (offset * j))
            CreateCell(2 + (offset * i), 2 + (offset * j))

ManyGliders(20)
#Glider()

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    tic = 0
    toc = 0
    tic = time.perf_counter()

    nextGeneration = aliveCells.copy()

    for aliveCell in aliveCells:
        neighbours = GetNeighbours(aliveCell[0], aliveCell[1])

        if not (neighbours == 2 or neighbours == 3):
            nextGeneration.pop(aliveCell)

        # check all dead cells
        if neighbours > 2:
            for i in range(3):
                nY = (aliveCell[1]-1) + i
                for j in range(3):
                    nX = (aliveCell[0]-1) + j
                    if IsCellAlive(nX, nY):
                        continue
                    else:
                        if GetNeighbours(nX, nY) == 3:
                            nextGeneration[(nX, nY)] = 1
    
    aliveCells = nextGeneration.copy()

    DrawCells()
    
    toc = time.perf_counter()
    print(f"Generation in {toc - tic:0.4f} seconds")

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()