"""
Main Driver File. Responsible for handling user inputs and displaying the current GameState object
"""
import pygame as p
import math
import hexChessEngine

# Set up the display
WIDTH, HEIGHT = 1600, 900
HEX_SIZE = 50
MAX_FPS = 30
IMAGES = {}

# Define colors
GREEN1 = (8, 168, 76)
GREEN2 = (182, 227, 201)
GREEN3 = (121, 209, 158)
BACKGROUND = (173, 155, 114)

#loadImages
def loadImages():
    pieces = ["bB", "bK", "bN", "bp", "bQ", "bR", "wB", "wK", "wN", "wp", "wQ","wR"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("./images/" + piece + ".png"), (55,55))
    #Image can be accessed by 'IMAGES['wp']'

# Function to draw a single hexagon at a specific point
def draw_hexagon(surface, color, center, size):
    points = []
    for i in range(6):
        angle_deg = 60 * i
        angle_rad = math.radians(angle_deg)
        x = center[0] + size * math.cos(angle_rad)
        y = center[1] + size * math.sin(angle_rad)
        points.append((x, y))
    p.draw.polygon(surface, color, points)
    return points

def isClickInHexagon(point, vertices):
    x, y = point
    n = len(vertices)
    inside = False

    p1x, p1y = vertices[0]
    for i in range(n + 1):
        p2x, p2y = vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

# Main loop
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color(BACKGROUND))
    gs = hexChessEngine.gameState()

    validMoves = gs.getAllValidMoves()
    moveMade = False #Flag variable for when a move is made
 
    loadImages()
    hexSelected = () #
    playerClick = [] #2 Values , keeps tracks of players clicks
    running = True
    while running:
        # Event handling
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

            #Mouse Handlers
            #___________________________
            #Move Pieces
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                posX = location[0]
                posY = location[1] 
                for row_idx, row in enumerate(gs.fullBoard[1]):
                    for col_idx, hexagon in enumerate(row):
                        if hexagon and isClickInHexagon((posX, posY), hexagon):
                            if hexSelected == (row_idx, col_idx):
                                hexSelected = ()
                                playerClick = []
                            else:
                                if(gs.fullBoard[0][row_idx][col_idx]!="_"):
                                    hexSelected = (row_idx, col_idx)
                                    playerClick.append(hexSelected)
                                elif(gs.fullBoard[0][row_idx][col_idx]!="_" or len(playerClick) > 0):
                                    hexSelected = (row_idx, col_idx)
                                    playerClick.append(hexSelected)
                                else:
                                    hexSelected = ()
                                    playerClick = []
                            if len(playerClick) == 2:
                                move = hexChessEngine.Move(playerClick[0], playerClick[1], gs.fullBoard)
                                if move in validMoves:
                                    print(move.getChessNotation())
                                    gs.makeMove(move)
                                    moveMade = True
                                hexSelected = ()
                                playerClick = []


            #Key Handler
            #___________________________
            #Undo
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undo()
                    moveMade = True

        if moveMade:
            validMoves = gs.getAllValidMoves()
            moveMade = False

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen,gs.fullBoard)
    drawPieces(screen,gs.fullBoard)#draw pieces on top of those hexagons

"""
Draw Squares On board
"""
def drawBoard(screen,fullBoard):
    colors = [p.Color(GREEN1),p.Color(GREEN2),p.Color(GREEN3)]
    xNeg = 4
    for x in range(11):
        num = 0
        width = 0
        colorX = 1
        if x < 6:
            width = 0 + x
            for i in range(6 - x, 12):
                color = colors[(i%3)-(x%3)]
                pos = ((800 + (52*x)),(545 - (60 * (width)) + (88 * x)))
                points = draw_hexagon(screen, color, pos,35)
                fullBoard[1][x][num] = points
                num += 1
                width += 1
        if x > 5:
            width = xNeg
            for j in range(10 - (x - 6), 0, -1):
                color = colors[((x-1)%3)-(j%3)]
                pos = ((800 + (52*x)),(545 - (60 * (width)) + (88 * xNeg)))
                points = draw_hexagon(screen, color, pos,35)
                fullBoard[1][x][num] = points
                num += 1
                width += 1
            xNeg += -1
    
"""
Draw the pieces on the board
"""

def drawPieces(screen,fullBoard):
    xNeg = 4
    for x in range(11):
        num = 0
        width = 0
        
        if x < 6:
            width = 0 + x
            for i in range(6 - x, 12):
                piece = fullBoard[0][x][num]
                if piece != "_":
                    screen.blit(IMAGES[piece], p.Rect((771 + (52*x)),(520 - (60 * (width)) + (88 * x)), 35 ,35))
                width += 1
                num += 1

        elif x > 5:
            width = xNeg
            for j in range(10 - (x - 6), 0, -1):
                piece = fullBoard[0][x][num]
                if piece != "_":
                    screen.blit(IMAGES[piece], p.Rect((771 + (52*x)),(520 - (60 * (width)) + (88 * xNeg)), 35 ,35))
                num += 1
                width += 1
            xNeg += -1
            


if __name__ == "__main__":
    main()