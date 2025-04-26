from abc import ABC, abstractmethod
from enum import IntEnum
from pathlib import Path
from .grid import *

DEFAULT_SAVETO = "./fpowerkit_logs/"

class GridSolveResult(IntEnum):
    '''Result of grid solving'''
    Failed = 0
    OK = 1
    OKwithoutVICons = 2 # Deprecated
    SubOKwithoutVICons = 3 # Deprecated
    PartialOK = 4


class SolverBase(ABC):
    def __init__(self, grid:Grid, eps:float = 1e-6, max_iter:int = 1000, *, default_saveto:str = DEFAULT_SAVETO, **kwargs):
        self.grid = grid
        self.eps = eps
        self.max_iter = max_iter
        self.saveto = default_saveto
    
    def SetErrorSaveTo(self, path:str = DEFAULT_SAVETO):
        self.saveto = path
        Path(path).mkdir(parents=True, exist_ok = True)

    def _calc_line_params(self):
        for l in self.grid.Lines:
            vi = self.grid.Bus(l.fBus).V_cpx
            vj = self.grid.Bus(l.tBus).V_cpx
            assert vi is not None and vj is not None
            i = (vi-vj)/l.Z
            l.I = abs(i)
            s = vi*i.conjugate()
            l.P = s.real
            l.Q = s.imag
    
    @abstractmethod
    def solve(self, grid:Grid, _t:int, /, **kwargs):
        raise NotImplementedError
