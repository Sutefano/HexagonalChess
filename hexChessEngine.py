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
        board = [list(row) for row in board_tuple]    
        depth = 2
        self.fullBoard = [copy.deepcopy(board) for _ in range(depth)]

        self.whiteToMove = True
        self.moveLog = []

    """
    Make a move
    """
    def makeMove(self , move):
        self.fullBoard[0][move.startRow][move.startCol] = "_"
        self.fullBoard[0][move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    """
    Undo a move
    """
    def undo(self):
        if len(self.moveLog) != 0: #Make sure theres a move to undo
            move = self.moveLog.pop()
            self.fullBoard[0][move.startRow][move.startCol] = move.pieceMoved
            self.fullBoard[0][move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #Swap Turns again

    """
    All moves considering checks
    """
    def getValidMovesCHECK(self):
        return self.getAllValidMoves()
    
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
                        pass
                            
                    if piece == 'B':
                        pass
                            
                    if piece == 'Q':
                        pass
        return moves

    """
    Get all pawn moves
    """
    def getPawnMoves(self,row,col,moves):
        if self.whiteToMove:
            if self.fullBoard[0][row][col + 1] == "_":
                moves.append(Move((row,col),(row,col + 1),self.fullBoard))
                for i in range(1,10,1):
                    if row == i and self.fullBoard[0][row][col + 2] == "_":
                        moves.append(Move((row,col),(row,col + 2),self.fullBoard))
            
            #Left Capture White
            if (row - 1) >= 0:
                if self.fullBoard[0][row - 1][col] != "_":
                    moves.append(Move((row,col),(row - 1,col),self.fullBoard))
            
            #Right Capture Right
            if (row + 1) <= 10:
                if self.fullBoard[0][row + 1][col + 1] != "_":
                    moves.append(Move((row,col),(row + 1,col + 1),self.fullBoard))
                              
        else:
            if self.fullBoard[0][row][col - 1] == "_":
                moves.append(Move((row,col),(row,col - 1),self.fullBoard))
                for i in range(1,10,1):
                    if row == i and self.fullBoard[0][row][col - 2] == "_":
                        moves.append(Move((row,col),(row,col  - 2),self.fullBoard))
            """
            #Left Capture Black
            if (row - 1) >= 0:
                    if self.fullBoard[0][row - 1][col - 1] != "_": 
                        moves.append(Move((row,col),(row - 1,col - 1),self.fullBoard))
            #Right capture Black
            if (row + 1) <= 10:
                if self.fullBoard[0][row + 1][col] != "_": 
                    moves.append(Move((row,col),(row + 1,col),self.fullBoard))
            """
            


    """
    Get all rook moves
    """
    def getRookMoves(self,row,col,moves):
        pass
                                
                                  


                        
                         


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




    def __init__(self, firstHex, secondHex, fullBoard):
        self.startRow = firstHex[0]
        self.startCol = firstHex[1]
        self.endRow = secondHex[0]
        self.endCol = secondHex[1]
        self.pieceMoved = fullBoard[0][self.startRow][self.startCol]
        self.pieceCaptured = fullBoard[0][self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self,row,col):
        return self.rowsToFiles[row] + self.colsToRanks[col]


