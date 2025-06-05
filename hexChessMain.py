"""
Main Driver File. Responsible for handling user inputs and displaying the current GameState object
"""
import pygame as p
import math
import hexChessEngine
#Sound imports
from playsound import playsound

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
    moveSound = p.mixer.Sound("./sounds/Move.mp3")
    screen = p.display.set_mode((WIDTH, HEIGHT),p.RESIZABLE)
    clock = p.time.Clock()
    gs = hexChessEngine.gameState()
    validMoves = gs.getValidMovesCHECK()
    moveMade = False #Flag variable for when a move is made
    
    loadImages()
    hexSelected = () #
    drawBoardState = True
    playerClick = [] #2 Values , keeps tracks of players clicks
    running = True
    while running:
        # Event handling
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #if len(validMoves) == 0:
            #   running = False
            #

            #Mouse Handlers
            #___________________________
            #Move Pieces
            if e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                posX = location[0]
                posY = location[1]
                if len(validMoves) == 0:
                    gs.checkMate = True
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
                                for i in range(len(validMoves)):
                                    if move == validMoves[i]:
                                        print(move.getChessNotation())
                                        #print(move)
                                        #print(move.startCol,move.endCol)
                                        #print(move.startRow,move.endRow)
                                        gs.makeMove(validMoves[i])
                                        moveSound.play()
                                        moveMade = True
                                        drawBoardState = True
                                        hexSelected = ()
                                        playerClick = []
                                        

                                if not moveMade:
                                    playerClick = [hexSelected]


            #Key Handler
            #___________________________
            #Undo
            if e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    if (len(gs.moveLog)) != 0:
                        moveSound.play()
                    gs.undo()
                    moveMade = True
                    drawBoardState = True

            if e.type == p.VIDEORESIZE:  # Detect window resize
                print ("true")
                screen = p.display.set_mode((600,600), p.RESIZABLE)
                screen = e.screen
                    
                    
        if moveMade:
            validMoves = gs.getValidMovesCHECK()
            moveMade = False

        if drawBoardState:
            drawGameState(screen,gs, validMoves, hexSelected)

        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, validMoves, hexSelected):
    drawBoard(screen,gs.fullBoard)
    highlightHex(screen, gs, validMoves, hexSelected)
    drawPieces(screen,gs.fullBoard)#draw pieces on top of those hexagons

"""
Highlight Moves
"""
def highlightHex(screen, gs, validMoves, hexSelected):
    if hexSelected != ():
        row, col = hexSelected
        if gs.fullBoard[0][row][col][0] == ('w' if gs.whiteToMove else 'b'):
            p.draw.polygon(screen,p.Color('blue'),gs.fullBoard[1][row][col],3)
            for move in validMoves:
                if move.startRow == row and move.startCol == col:
                    p.draw.polygon(screen,p.Color((215, 224, 117, 128)),gs.fullBoard[1][move.endRow][move.endCol],3)

"""
Draw Hexes On board
"""
def drawBoard(screen,fullBoard):
    
    screen.fill(p.Color(BACKGROUND))
    p.draw.rect(screen, p.Color("DARKGREEN"), (0,0,500,900))
    p.draw.rect(screen, p.Color("WHITE"), (50,50,400,800))
    colors = [p.Color(GREEN1),p.Color(GREEN2),p.Color(GREEN3)]
    xNeg = 4
    for x in range(11):
        num = 0
        width = 0
        if x < 6:
            width = 0 + x
            for i in range(6 - x, 12):
                color = colors[(i%3)-(x%3)]
                pos = ((800 + (52*x)),(590 - (60 * (width)) + (88 * x)))
                points = draw_hexagon(screen, color, pos,35)
                fullBoard[1][x][num] = points
                num += 1
                width += 1
        if x > 5:
            width = xNeg
            for j in range(10 - (x - 6), 0, -1):
                color = colors[((x-1)%3)-(j%3)]
                pos = ((800 + (52*x)),(590 - (60 * (width)) + (88 * xNeg)))
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
                    screen.blit(IMAGES[piece], p.Rect((771 + (52*x)),(565 - (60 * (width)) + (88 * x)), 35 ,35))
                width += 1
                num += 1

        elif x > 5:
            width = xNeg
            for j in range(10 - (x - 6), 0, -1):
                piece = fullBoard[0][x][num]
                if piece != "_":
                    screen.blit(IMAGES[piece], p.Rect((771 + (52*x)),(565 - (60 * (width)) + (88 * xNeg)), 35 ,35))
                num += 1
                width += 1
            xNeg += -1
    
def show_promotion_popup(screen):
    screen_width, screen_height = screen.get_size()

    # Draw popup background
    popup_width, popup_height = 300, 100
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    popup_rect = p.Rect(popup_x, popup_y, popup_width, popup_height)
    p.draw.rect(screen, (200, 200, 200), popup_rect)
    p.draw.rect(screen, (0, 0, 0), popup_rect, 2)

    # Load images for promotion options
    queen_img = p.image.load("images/wQ.png")  # Adjust paths accordingly
    rook_img = p.image.load("images/wR.png")
    bishop_img = p.image.load("images/wB.png")
    knight_img = p.image.load("images/wN.png")

    piece_images = [queen_img, rook_img, bishop_img, knight_img]
    option_rects = []
    # Draw piece options
    for i, img in enumerate(piece_images):
        img = p.transform.scale(img, (60, 60))
        x = popup_x + 20 + i * 70
        y = popup_y + 20
        screen.blit(img, (x, y))
        option_rects.append(p.Rect(x, y, 60, 60))

    p.display.flip()

    # Wait for user selection
    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                return "Q"  # Default fallback
            if event.type == p.MOUSEBUTTONDOWN:
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(event.pos):
                        return ["Q", "R", "B", "N"][i]
            


if __name__ == "__main__":
    main()