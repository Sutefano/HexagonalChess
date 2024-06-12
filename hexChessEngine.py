"""
This classi responsible for storing all the information about the curent state of the chess game
Also responsible for determinating valid moves on current state
Also keeps a move log
"""
import copy
import numpy as np

class gameState():

    
    """
    The 3D array in which the gamestate is held
    """

    def __init__(self):
        board_tuple = (
            ["_","_","_","_","_","_"],
            ["wp","_","_","_","_","_","bp"],
            ["wR","wp","_","_","_","_","bp","bR"],
            ["wN","_","wp","_","_","_","bp","_","bN"],
            ["wQ","_","_","wp","_","_","bp","_","_","bQ"],
            ["wB","wB","wB","_","wp","_","bp","_","bB","bB","bB"],
            ["wK","_","_","wp","_","_","bp","_","_","bK"],
            ["wN","_","wp","_","_","_","bp","_","bN"],
            ["wR","wp","_","_","_","_","bp","bR"],
            ["wp","_","_","_","_","_","bp"],
            ["_","_","_","_","_","_"],
        )
        board_tuple_test = (
            ["_","_","_","_","_","_"],
            ["_","_","_","_","_","_","_"],
            ["_","_","_","bK","_","_","_","_"],
            ["_","_","_","_","_","_","_","_","_"],
            ["_","_","_","_","_","_","_","_","_","_"],
            ["_","_","_","_","_","_","_","_","_","_","_"],
            ["wK","_","_","_","_","_","_","_","_","_"],
            ["bQ","_","_","_","_","_","_","_","_"],
            ["_","_","bN","_","_","_","_","_"],
            ["_","_","_","_","_","_","_"],
            ["_","_","_","_","_","_"],
        )
        board = [list(row) for row in board_tuple]    
        depth = 2
        self.fullBoard = [copy.deepcopy(board) for _ in range(depth)]
        self.lastColIndex = [6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6]
        self.whiteToMove = True
        self.moveLog = []
        #White pawn position for any pawn that cane move 2 hexes as the starting white pawns on hexagons all start on diff columns     
        self.positions_to_check_white = [(1, 0),(2, 1),(3, 2),(4, 3),(5, 4),(6, 3),(7, 2),(8, 1),(9, 0)]

        #King Position and checkmate variables
        self.wKLocation = (6,0)
        self.bKLocation = (6,9)
        self.checkMate = False
        self.staleMate = False
        self.enPassnt = ()#Coordinates for the hex where en passant is possible

    """
    Make a move
    """
    def makeMove(self , move):
        self.fullBoard[0][move.startRow][move.startCol] = "_"
        self.fullBoard[0][move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        #Update King Pos
        if move.pieceMoved == "wK":
            self.wKLocation = (move.endRow,move.endCol)
        elif  move.pieceMoved == "bK":
            self.bKLocation  = (move.endRow,move.endCol)

        #Pawn Promotion
        if move.isPawnPromotion:
            self.fullBoard[0][move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

    """
    Undo a move
    """
    def undo(self):
        if len(self.moveLog) != 0: #Make sure theres a move to undo
            move = self.moveLog.pop()
            self.fullBoard[0][move.startRow][move.startCol] = move.pieceMoved
            self.fullBoard[0][move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Swap Turns again
            #Update King Pos
            if move.pieceMoved == "wK":
                self.wKLocation = (move.startRow,move.startCol)
            elif  move.pieceMoved == "bK":
                self.bKLocation  = (move.startRow,move.startCol)

    """
    All moves considering checks
    """

    def getValidMovesCHECK(self):
        #1) generate all possible moves
        moves = self.getAllValidMoves()
        #2) for each move, make this move
        for i in range(len(moves) - 1 , -1 , -1):
            self.makeMove(moves[i])
            print(self.bKLocation)
            #3) generate all opponet's moves
            #4) for each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove #swap turns again as the moveMove function swaps turns inherently
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undo()
        return moves
    
    """
    Moves that put you in check
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.hexUnderAttack(self.wKLocation[0],self.wKLocation[1])
        else:
            return self.hexUnderAttack(self.bKLocation[0],self.bKLocation[1])

    """
    Determine if enemy attack hex r,c
    """
    def hexUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove #switch to opponents turn
        oppMoves = self.getAllValidMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col: #hex is under attack
                return True
        return False
        

    """
    All moves without considering checks
    """

    def getAllValidMoves(self):
        moves  = []
        for row,r in enumerate(self.fullBoard[0]):
            for col,c in enumerate(r):
                turn = self.fullBoard[0][row][col][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.fullBoard[0][row][col][1]
                    if piece == 'p':
                        self.getPawnMoves(row,col,moves)
                    
                    if piece == 'R':
                        self.getRookMoves(row,col,moves)
                            
                    if piece == 'N':
                        self.getKnightMoves(row,col,moves)
                            
                    if piece == 'B':
                        self.getBishopMoves(row,col,moves)
                            
                    if piece == 'Q':
                        self.getBishopMoves(row,col,moves)
                        self.getRookMoves(row,col,moves)

                    if piece == 'K':
                        self.getKingMoves(row,col,moves)
        return moves

    """
    Get all Pawn moves
    """    
    
    def getPawnMoves(self,row,col,moves):
        #White Pawn Moves                  
        if self.whiteToMove:
            #Move On board
            if ((col + 1) < self.lastColIndex[row]):
                if (self.fullBoard[0][row][col + 1] == "_"):
                        moves.append(Move((row,col),(row,col + 1),self.fullBoard))
                        for check_row, check_col in self.positions_to_check_white:
                            if (row == check_row and col == check_col) and (col + 2 < len(self.fullBoard[0][row])) and self.fullBoard[0][row][col + 2] == "_":
                                moves.append(Move((row, col), (row, col + 2), self.fullBoard))
                #Captrue Moves
                if row > 5:
                    #Left Capture White
                    if (row - 1) >= 0:  
                        if (self.fullBoard[0][row - 1][col + 1] != "_") and (self.fullBoard[0][row - 1][col + 1][0] != 'w') :
                            moves.append(Move((row,col),(row - 1,col + 1),self.fullBoard))
                    
                    #Right Capture Right
                    if (row + 1) <= 10:
                        if (self.fullBoard[0][row + 1][col] != "_") and (self.fullBoard[0][row + 1][col][0] != 'w'):
                            moves.append(Move((row,col),(row + 1,col),self.fullBoard))
                
                if row < 5:
                    #Left Capture White
                    if (row - 1) >= 0:
                        if (self.fullBoard[0][row - 1][col] != "_") and (self.fullBoard[0][row - 1][col][0] != 'w'):
                            moves.append(Move((row,col),(row - 1,col),self.fullBoard))
                    
                    #Right Capture Right
                    if (row + 1) <= 10:
                        if (self.fullBoard[0][row + 1][col + 1] != "_") and (self.fullBoard[0][row + 1][col + 1][0] != 'w'):
                            moves.append(Move((row,col),(row + 1,col + 1),self.fullBoard))

                if row == 5:
                    #Left Capture White
                    if (row - 1) >= 0:
                        if (self.fullBoard[0][row - 1][col] != "_") and (self.fullBoard[0][row - 1][col][0] != 'w'):
                            moves.append(Move((row,col),(row - 1,col),self.fullBoard))
                    
                    #Right Capture Right
                    if (row + 1) <= 10:
                        if (self.fullBoard[0][row + 1][col] != "_") and (self.fullBoard[0][row + 1][col][0] != 'w'):
                            moves.append(Move((row,col),(row + 1,col),self.fullBoard))

        #Black Pawn Moves
        else:
            if (col >= 0):
                #Move on board
                if (self.fullBoard[0][row][col - 1] == "_") and (col >= 0):
                    moves.append(Move((row,col),(row,col - 1),self.fullBoard))
                    for check_row in range(1,10):
                        if row == check_row and col == 6 and self.fullBoard[0][row][col - 2] == "_":
                            moves.append(Move((row, col), (row, col - 2), self.fullBoard))
                
                #Capture moves
                if row > 5:
                    #Left Capture Black
                    if (row - 1) >= 0:
                        if (self.fullBoard[0][row - 1][col] != "_") and (self.fullBoard[0][row - 1][col][0] != 'b'): 
                            moves.append(Move((row,col),(row - 1,col),self.fullBoard))

                    #Right capture Black
                    if (row + 1) <= 10:
                        if (self.fullBoard[0][row + 1][col - 1] != "_") and (self.fullBoard[0][row + 1][col - 1][0] != 'b'): 
                            moves.append(Move((row,col),(row + 1,col - 1),self.fullBoard))

                if row < 5:
                    #Left Capture Black
                    if (row - 1) >= 0:
                        if (self.fullBoard[0][row - 1][col - 1]!= "_") and (self.fullBoard[0][row - 1][col - 1][0]!= 'b'): 
                            moves.append(Move((row,col),(row - 1,col - 1),self.fullBoard))

                    #Right capture Black
                    if (row + 1) <= 10:
                        if (self.fullBoard[0][row + 1][col] != "_") and (self.fullBoard[0][row + 1][col][0] != 'b'): 
                            moves.append(Move((row,col),(row + 1,col),self.fullBoard))

                if row == 5:
                    #Left Capture Black
                    if (row - 1) >= 0:
                        if (self.fullBoard[0][row - 1][col - 1] != "_") and (self.fullBoard[0][row - 1][col - 1][0] != 'b'): 
                            moves.append(Move((row,col),(row - 1,col - 1),self.fullBoard))

                    #Right capture Black
                    if (row + 1) <= 10:
                        if (self.fullBoard[0][row + 1][col - 1] != "_") and (self.fullBoard[0][row + 1][col - 1][0] != 'b'): 
                            moves.append(Move((row,col),(row + 1,col - 1),self.fullBoard))
       
    """
    Get all Rook moves
    """
    def getRookMoves(self,row,col,moves):
        enemyColor = "b" if self.whiteToMove else "w"
        
        #If starting row is left of the middle
        if row < 5:
            movementDirection = ((0,-1),(0,1),(-1,-1),(1,0),(-1,0),(1,1))#Down, Up, Down-Left, Down-Right, Up-Left, Up-Right
            for d in movementDirection:
                tempNum = 0
                for moveRange in range(1,11):
                    endRow = row + d[0] * moveRange
                    endCol = col + d[1] * moveRange
                    if endRow > 5:
                        tempNum += 1
                        if d == (1,0):
                            endCol -= tempNum
                        if d == (1,1):
                            endCol -= tempNum

                    if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                        endPiece = self.fullBoard[0][endRow][endCol]
                        if endPiece == "_":
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                            break
                        else:
                            break
                    else:
                        break
        
        #If starting row is right of the middle
        if row > 5:
            
            movementDirection = ((0,-1),(0,1),(-1,0),(1,-1),(-1,1),(1,0))#Down, Up, Down-Left, Down-Right, Up-Left, Up-Right 
            for d in movementDirection:
                tempNum = 0
                for moveRange in range(1,11):
                    endRow = row + d[0] * moveRange
                    endCol = col + d[1] * moveRange
                    if endRow < 5:
                        tempNum += 1
                        if d == (-1,0):
                            endCol -= tempNum
                        if d == (-1,1):
                            endCol -= tempNum
                    if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                        endPiece = self.fullBoard[0][endRow][endCol]
                        if endPiece == "_":
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                            break
                        else:
                            break
                    else:
                        break 
        
        #If Starting row is the middle
        if row == 5:
            movementDirection = ((0,-1),(0,1),(-1,-1),(1,-1),(-1,0),(1,0))#Down, Up, Down-Left, Down-Right, Up-Left, Up-Right
            for d in movementDirection:
                for moveRange in range(1,11):
                    endRow = row + d[0] * moveRange
                    endCol = col + d[1] * moveRange 
                    if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                        endPiece = self.fullBoard[0][endRow][endCol]
                        if endPiece == "_":
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                            break
                        else:
                            break
                    else:
                        break 

    """
    Get all Bishop moves
    """
    def getBishopMoves(self,row,col,moves):
        enemyColor = "b" if self.whiteToMove else "w"
        if row < 5:
            movementDirection = ((-2,-1),(2,1),#Left, Right
                                 (-1,1),(1,2),#Up-Left, Up-Right
                                 (-1,-2),(1,-1))#Down-Left, Down-Right
            for d in movementDirection:
                tempNum = 0
                for moveRange in range(1,11):
                    endRow = row + d[0] * moveRange
                    endCol = col + d[1] * moveRange
                    if (row%2) == 0:
                        if endRow >= 6:
                            if d == (1,2):
                                tempNum += 1
                                endCol -= tempNum
                            if d == (1,-1):
                                tempNum += 1
                                endCol -= tempNum
                            if d == (2,1):
                                tempNum += 1
                                endCol -= tempNum
                                tempNum += 1
                                
                    else:
                        if endRow > 5:
                            if d == (1,2):
                                tempNum += 1
                                endCol -= tempNum
                            if d == (1,-1):
                                tempNum += 1
                                endCol -= tempNum
                            if d == (2,1):
                                tempNum += 2
                                endCol -= tempNum

                    if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                        endPiece = self.fullBoard[0][endRow][endCol]
                        if endPiece == "_":
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                            break
                        else:
                            break
                    else:
                        break
            
        if row > 5:
            movementDirection = ((-2,1),(2,-1),#Left, Right
                                 (-1,2),(1,1),#Up-Left, Up-Right
                                 (-1,-1),(1,-2))#Down-Left, Down-Right
            for d in movementDirection:
                tempNum = 0
                for moveRange in range(1,11):
                    endRow = row + d[0] * moveRange
                    endCol = col + d[1] * moveRange
                    if (row%2) == 0:
                        if endRow <= 4:
                            if d == (-1,2):
                                tempNum += 1
                                endCol -= tempNum
                            if d == (-1,-1):
                                tempNum += 1
                                endCol -= tempNum
                            if d == (-2,1):
                                tempNum += 1
                                endCol -= tempNum
                                tempNum += 1
                                
                    else:
                        if endRow < 5:
                            if d == (-1,2):
                                tempNum += 1
                                endCol -= tempNum
                            if d == (-1,-1):
                                tempNum += 1
                                endCol -= tempNum
                            if d == (-2,1):
                                tempNum += 2
                                endCol -= tempNum

                    if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                        endPiece = self.fullBoard[0][endRow][endCol]
                        if endPiece == "_":
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                            break
                        else:
                            break
                    else:
                        break

        if row == 5:
            movementDirection = ((-2,-1),(2,-1),#Left, Right
                                 (-1,1),(1,1),#Up-Left, Up-Right
                                 (-1,-2),(1,-2))#Down-Left, Down-Right
            for d in movementDirection:
                tempNum = 0
                for moveRange in range(1,11):
                    endRow = row + d[0] * moveRange
                    endCol = col + d[1] * moveRange
                    if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                        endPiece = self.fullBoard[0][endRow][endCol]
                        if endPiece == "_":
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                            break
                        else:
                            break
                    else:
                        break
                                
    """
    Get all Queen moves
    """            
    def getKnightMoves(self,row,col,moves):
        enemyColor = "b" if self.whiteToMove else "w"
        if row > 5:
            movementDirection = ((-3,1),(-3,2), #Left
                                 (3,-1),(3,-2), #Right
                                 (-1,3),(-2,3), #Top-Left
                                 (1,2),(2,1), #Top-Right
                                 (-1,-2),(-2,-1), #Bottom-Left
                                 (1,-3),(2,-3) #Bottom-Right
                                 )
            for d in movementDirection:
                endRow = row + d[0] * 1
                endCol = col + d[1] * 1 
                if endRow in [3, 4]:
                    if d in [(-3, 1), (-3, 2), (-2, 3),(-2,-1)]:
                        adjustment = 1 if endRow == 4 else 2
                        endCol -= adjustment

                if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                    endPiece = self.fullBoard[0][endRow][endCol]
                    if endPiece == "_":
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))

        if row < 5:
            movementDirection = ((-3,-1),(-3,-2), #Left
                                 (3,1),(3,2), #Right
                                 (-1,2),(-2,1), #Top-Left
                                 (1,3),(2,3), #Top-Right
                                 (-1,-3),(-2,-3), #Bottom-Left
                                 (1,-2),(2,-1) #Bottom-Right
                                 )
            for d in movementDirection: 
                endRow = row + d[0] * 1
                endCol = col + d[1] * 1
                if endRow in [6, 7]:
                    if d in [(3, 1), (3, 2),(2,-1),(2,3)]:
                        adjustment = 1 if endRow == 6 else 2
                        endCol -= adjustment
                if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                    endPiece = self.fullBoard[0][endRow][endCol]
                    if endPiece == "_":
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
        
        if row == 5:
            movementDirection = ((-3,-1),(-3,-2), #Left
                                 (3,-1),(3,-2), #Right
                                 (-1,2),(-2,1), #Top-Left
                                 (1,2),(2,1), #Top-Right
                                 (-1,-3),(-2,-3), #Bottom-Left
                                 (1,-3),(2,-3) #Bottom-Right
                                 )
            for d in movementDirection: 
                endRow = row + d[0] * 1
                endCol = col + d[1] * 1
                if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                    endPiece = self.fullBoard[0][endRow][endCol]
                    if endPiece == "_":
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))

    """
    Get all King moves
    """ 
    def getKingMoves(self,row,col,moves):
        enemyColor = "b" if self.whiteToMove else "w"
        if row > 5:
            movementDirection = (#Inner 6 Hexes
                                 (-1,0),(-1,1), 
                                 (1,0),(1,-1), 
                                 (0,-1),(0,1), 

                                 #Outer 6 Hexes
                                 (-2,1),(2,-1), 
                                 (-1,2),(-1,-1), 
                                 (1,1),(1,-2) 
                                 )
            for d in movementDirection:
                endRow = row + d[0] * 1
                endCol = col + d[1] * 1 
                if endRow == 4:
                    endCol = endCol - 1
                if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                    endPiece = self.fullBoard[0][endRow][endCol]
                    if endPiece == "_":
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))

        if row < 5:
            movementDirection = (#Inner 6 Hexes
                                 (-1,0),(-1,-1), 
                                 (1,0),(1,1),   
                                 (0,-1),(0,1), 

                                 #Outer 6 Hexes
                                 (-2,-1),(2,1), 
                                 (-1,-2),(-1,1), 
                                 (1,-1),(1,2) 
                                 )
            for d in movementDirection: 
                endRow = row + d[0] * 1
                endCol = col + d[1] * 1
                if endRow == 6:
                    endCol = endCol - 1
                if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                    endPiece = self.fullBoard[0][endRow][endCol]
                    if endPiece == "_":
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
        
        if row == 5:
            movementDirection = (#Inner 6 Hexes
                                 (-1,0),(-1,-1), 
                                 (1,0),(1,-1),   
                                 (0,-1),(0,1), 

                                 #Outer 6 Hexes
                                 (-2,-1),(2,-1), 
                                 (-1,-2),(-1,1), 
                                 (1,1),(1,-2) 
                                 )
            for d in movementDirection: 
                endRow = row + d[0] * 1
                endCol = col + d[1] * 1
                if 0 <= endRow < (len(self.lastColIndex)) and 0 <= endCol < (self.lastColIndex[endRow]):
                    endPiece = self.fullBoard[0][endRow][endCol]
                    if endPiece == "_":
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row,col),(endRow,endCol),self.fullBoard))


class Move():

    # map keys to values
    # key : value
    filesToRows = {"A": 0,"B": 1,"C": 2,"D": 3,
                   "E": 4,"F": 5,"G": 6,"H": 7,
                   "I": 8,"J": 9,"K": 10}

    rowsToFiles = {v: k for k, v in filesToRows.items()}

    ranksToCols = {"1": 0,"2": 1,"3": 2,"4": 3,
                   "5": 4,"6": 5,"7": 6,"8": 7,
                   "9": 8,"10": 9,"11": 10}
    
    colsToRanks = {v: k for k, v in ranksToCols.items()}
    lastColIndex = [6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6]




    def __init__(self, firstHex, secondHex, fullBoard):
        self.startRow = firstHex[0]
        self.startCol = firstHex[1]
        self.endRow = secondHex[0]
        self.endCol = secondHex[1]
        self.pieceMoved = fullBoard[0][self.startRow][self.startCol]
        self.pieceCaptured = fullBoard[0][self.endRow][self.endCol]
        #Pawn Promo
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endCol == (self.lastColIndex[self.endRow] - 1)) or (self.pieceMoved == "bp" and self.endCol == 0):
            self.isPawnPromotion = True
            print("true")

        #En Passant
        self.isEnPassantMove = False
        
        #Move ID
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self,row,col):
        return self.rowsToFiles[row] + self.colsToRanks[col]


