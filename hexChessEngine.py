"""
This classi responsible for storing all the information about the curent state of the chess game
Also responsible for determinating valid moves on current state
Also keeps a move log
"""
import copy
import numpy as np

class gameState():
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
