from dataclasses import dataclass
import tkinter as tk
from typing import Any, Callable


@dataclass
class Info:
    iteration: int = -1
    step: int = -1
    best_score: int = -1


@dataclass
class Controls:
    learning_rate: float
    exploration: float
    map_influence: float
    tps: float


class ControlsWindow(tk.Tk):
    def __init__(self, controls: Controls) -> None:
        super().__init__()
        self.title('Controls')
        self.geometry('450x280+1300+450')
        
        self.controls = controls

        self.iter_var = tk.StringVar(self, '')
        self.step_var = tk.StringVar(self, '')
        self.best_score_var = tk.StringVar(self, '')
        
        tk.Label(self, textvariable=self.iter_var) \
            .grid(row=0, column=0, columnspan=2)
        tk.Label(self, textvariable=self.step_var) \
            .grid(row=1, column=0, columnspan=2)
        tk.Label(self, textvariable=self.best_score_var) \
            .grid(row=2, column=0, columnspan=2)
        
        self.lr_var = tk.DoubleVar(self, self.controls.learning_rate)
        self.ex_var = tk.DoubleVar(self, self.controls.exploration)
        # self.inf_var = tk.DoubleVar(self, self.controls.map_influence)
        self.tps_var = tk.DoubleVar(self, self.controls.tps)
        
        self._grid_slider(
            3, 'Learning Rate',
            (0.001, 0.03, 0.001),
            self.lr_var,
            lambda v: setattr(self.controls, 'learning_rate', v)
        )
        
        self._grid_slider(
            4, 'Exploration',
            (0, 1, 0.01),
            self.ex_var,
            lambda v: setattr(self.controls, 'exploration', v)
        )
        
        # self._grid_slider(
        #     5, 'Full map state multiplier',
        #     (0, 1, 0.01),
        #     self.inf_var,
        #     lambda v: setattr(self.controls, 'map_influence', v)
        # )
        
        self._grid_slider(
            6, 'Ticks per Second',
            (0, 200, 5),
            self.tps_var,
            lambda v: setattr(self.controls, 'tps', v)
        )
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
    def set_info(self, info: Info) -> None:
        self.iter_var.set(f'Iteration: {info.iteration}')
        self.step_var.set(f'Step: {info.step}')
        self.best_score_var.set(f'Best Score: {info.best_score}')
        
    def _grid_slider(
        self, row: int, lbl: str, rg: tuple[float, float, float],
        var: tk.DoubleVar, cb: Callable[[float], None]
    ) -> None:
        label = tk.Label(self)
        slider = tk.Scale(
            self, from_=rg[0], to=rg[1], resolution=rg[2],
            orient=tk.HORIZONTAL, length=200, variable=var
        )
        label.grid(row=row, column=0)
        slider.grid(row=row, column=1)
        
        def update_value(*_: Any):
            cb(var.get())
            label.config(text=f'{lbl}: {var.get()}')
        
        update_value()
        var.trace_add('write', update_value)
        
    
