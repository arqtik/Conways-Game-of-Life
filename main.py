import pygame
import time

width = 800
height = 600
cellSize = 5

xCellCount = int(width / cellSize)
yCellCount = int(height / cellSize)

cells = [[None] * xCellCount for _ in range(yCellCount)]
aliveCells = []

def DrawCells():
    for cell in aliveCells:
        rect = pygame.Rect(cell[0] * cellSize, cell[1] * cellSize, cellSize, cellSize)
        pygame.draw.rect(screen, "white", rect)

def CreateCell(x, y):
    #cells[y][x] = tkc.create_rectangle((x * cellSize, y * cellSize), ((x + 1) * cellSize, (y + 1) * cellSize), outline='black', fill='white')
    aliveCells.append((x, y))

def KillCell(x, y):
    aliveCells.remove((x, y))

def IsCellAlive(x, y):
    return (x, y) in aliveCells

def GetNeighbours(x, y):
    count = 0
    for i in range(3):
        nY = (y-1) + i
        for j in range(3):
            nX = (x-1) + j
            if i == 1 and j == 1: # Checking the called cell
                continue
            elif nX < 0 or nX > xCellCount - 1: # Out of bounds X
                continue
            elif nY < 0 or nY > yCellCount - 1: # Out of bounds Y
                continue
            elif IsCellAlive(nX, nY):
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
            CreateCell(1 + (offset * i),0 + (offset * j))
            CreateCell(2 + (offset * i),1 + (offset * j))
            CreateCell(0 + (offset * i),2 + (offset * j))
            CreateCell(1 + (offset * i),2 + (offset * j))
            CreateCell(2 + (offset * i),2 + (offset * j))

ManyGliders(20)

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

    cellsToKill = []
    cellsToCreate = []

    for aliveCell in aliveCells:
        neighbours = GetNeighbours(aliveCell[0], aliveCell[1])

        if not (neighbours == 2 or neighbours == 3):
            cellsToKill.append(aliveCell)

        # check all dead cells
        if neighbours > 2:
            for i in range(3):
                nY = (aliveCell[1]-1) + i
                for j in range(3):
                    nX = (aliveCell[0]-1) + j
                    if nX < 0 or nX > xCellCount - 1: # Out of bounds X
                        continue
                    elif nY < 0 or nY > yCellCount - 1: # Out of bounds Y
                        continue
                    elif IsCellAlive(nX, nY):
                        continue
                    else:
                        if GetNeighbours(nX, nY) == 3 and (nX, nY) not in cellsToCreate:
                            cellsToCreate.append((nX, nY))

    # Create next generation
    for cell in cellsToKill:
        KillCell(cell[0], cell[1])
    
    for cell in cellsToCreate:
        CreateCell(cell[0], cell[1])


    toc = time.perf_counter()
    print(f"Generation in {toc - tic:0.4f} seconds")
    DrawCells()


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()


'''
canvas = sg.Canvas(size=(width, height), background_color='black', key='canvas')

layout = [[canvas]]

window = sg.Window("Conway's Game of Life", layout=layout, finalize=True)

tkc = canvas.TKCanvas

cells = [[None] * xCellCount for _ in range(yCellCount)]
aliveCells = []

def CreateCell(x, y):
    cells[y][x] = tkc.create_rectangle((x * cellSize, y * cellSize), ((x + 1) * cellSize, (y + 1) * cellSize), outline='black', fill='white')
    aliveCells.append((x, y))

def KillCell(x, y):
    tkc.delete(cells[y][x])
    cells[y][x] = None
    aliveCells.remove((x, y))

def IsCellAlive(x, y):
    return cells[y][x] != None

def GetNeighbours(x, y):
    count = 0
    for i in range(3):
        nY = (y-1) + i
        for j in range(3):
            nX = (x-1) + j
            if i == 1 and j == 1: # Checking the called cell
                continue
            elif nX < 0 or nX > xCellCount - 1: # Out of bounds X
                continue
            elif nY < 0 or nY > yCellCount - 1: # Out of bounds Y
                continue
            elif IsCellAlive(nX, nY):
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
            CreateCell(1 + (offset * i),0 + (offset * j))
            CreateCell(2 + (offset * i),1 + (offset * j))
            CreateCell(0 + (offset * i),2 + (offset * j))
            CreateCell(1 + (offset * i),2 + (offset * j))
            CreateCell(2 + (offset * i),2 + (offset * j))

ManyGliders(20)


while True:
    

    event, values = window.read(timeout=1)
    if event == sg.WIN_CLOSED:
        break
    
    tic = 0
    toc = 0

    tic = time.perf_counter()

    cellsToKill = []
    cellsToCreate = []



    for aliveCell in aliveCells:
        neighbours = GetNeighbours(aliveCell[0], aliveCell[1])

        if not (neighbours == 2 or neighbours == 3):
            cellsToKill.append(aliveCell)

        # check all dead cells
        if neighbours > 2:
            for i in range(3):
                nY = (aliveCell[1]-1) + i
                for j in range(3):
                    nX = (aliveCell[0]-1) + j
                    if nX < 0 or nX > xCellCount - 1: # Out of bounds X
                        continue
                    elif nY < 0 or nY > yCellCount - 1: # Out of bounds Y
                        continue
                    elif IsCellAlive(nX, nY):
                        continue
                    else:
                        if GetNeighbours(nX, nY) == 3 and (nX, nY) not in cellsToCreate:
                            cellsToCreate.append((nX, nY))

    # Create next generation
    for cell in cellsToKill:
        KillCell(cell[0], cell[1])
    
    for cell in cellsToCreate:
        CreateCell(cell[0], cell[1])

    #print("Killed " + str(len(cellsToKill)) + ", Created: " + str(len(cellsToCreate)))

    toc = time.perf_counter()
    print(f"Generation in {toc - tic:0.4f} seconds")

'''
