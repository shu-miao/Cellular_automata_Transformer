import numpy as np
import pandas as pd

class CellularAutomaton:
    def __init__(self,grid_size,lat,lon):
        self.grid_size = grid_size
        self.grid = np.zeros((grid_size, grid_size))