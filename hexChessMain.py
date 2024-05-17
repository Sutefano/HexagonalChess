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
    loadImages()
    hexSelected = () #
    playerClick = [] #2 Values , keeps tracks of players clicks
    running = True
    while running:
        # Event handling
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
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
                                hexSelected = (row_idx, col_idx)
                                playerClick.append(hexSelected)
                            if len(playerClick) == 2:
                                move = hexChessEngine.Move(playerClick[0], playerClick[1], gs.fullBoard)
                                gs.makeMove(move)
                                hexSelected = ()
                                playerClick = []

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen,gs.fullBoard) #draw hexagons on board
    drawPieces(screen,gs.fullBoard)#draw pieces on top of those hexagons

"""
Draw Squares On board
"""
def drawBoard(screen,fullBoard):
    colors = [p.Color(GREEN1),p.Color(GREEN2),p.Color(GREEN3)]
    for x in range(11):
        num = 0
        if x < 6:
            for i in range(6 - x, 12):
                color = colors[(i%3)-(x%3)]
                pos = ((800 + (52*x)),(275 + (60 * (i-6)) + (28 * x)))
                points = draw_hexagon(screen, color, pos,35)
                fullBoard[1][x][num] = points
                num += 1
        if x > 5:
            for j in range(10 - (x - 6), 0, -1):
                color = colors[(j%3)-(x%3)]
                pos = ((800 + (52*x)),(275 + (60 * (j-6)) + (28 * x)))
                points = draw_hexagon(screen, color, pos,35)
                fullBoard[1][x][num] = points
                num += 1
    
"""
Try locating the hexSelected 
"""

def drawPieces(screen,fullBoard):
    for x in range(11):
        num = 0
        if x < 6:
            for i in range(6 - x, 12):
                piece = fullBoard[0][x][num]
                if piece != "_":
                    screen.blit(IMAGES[piece], p.Rect((771 + (52*x)),(245 + (60 * (i - 6)) + (28 * x)), 35 ,35))
                num += 1

        elif x > 5:
            for j in range(10 - (x - 6), 0, -1):
                piece = fullBoard[0][x][num]
                if piece != "_":
                    screen.blit(IMAGES[piece], p.Rect((771 + (52*x)),(245 + (60 * (j-6)) + (28 * x)), 35 ,35))
                num += 1  
            


if __name__ == "__main__":
    main()