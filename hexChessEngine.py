"""
This classi responsible for storing all the information about the curent state of the chess game
Also responsible for determinating valid moves on current state
Also keeps a move log
"""
import numpy as np

class gameState():
    def __init__(self):
        self.board = (
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

        self.hexagons = ()
    
