import tkinter as tk
from enum import Enum
from typing import Callable, Any

from item import Item
from board import Board

MIN_SIZE = 700
WINDOW_POSITION = (160, 160)


class Event(Enum):
    Play = 'play', 'lightgreen', '#6eb56e'
    Pause = 'pause', 'lightblue', '#7CB9E8'
    Step = 'step', 'lightgray', '#A9A9A9'
    SpeedUp = 'speed up', '#FFFF8F', '#E4D00A'
    SlowDown = 'slow down', '#FFFF8F', '#E4D00A'


class BoardWindow(tk.Tk):
    def __init__(self, board_size: int, callback: Callable[[Event], Any], infos: list[tuple[str, Any]]):
        super().__init__()

        self.board_size = board_size
        self.callback = callback
        self._infos = infos
        self._info_labels: list[tk.Label] = []

        self.__setup()

    def __setup(self):
        self.title('Preys and Predators')

        true_size = self.__calculate_board_true_size()
        controls_size = 150
        self.geometry(f'{true_size + controls_size}x{true_size}')
        self.resizable(False, False)

        self.geometry('+{}+{}'.format(*WINDOW_POSITION))

        grid_frame = self.__setup_grid_frame(self)
        grid_frame.place(x=0, y=0, width=true_size, height=true_size)
        info_frame = self.__setup_info_frame(self)
        info_frame.place(x=true_size, y=100, width=controls_size)
        control_frame = self.__setup_control_frame(self)
        control_frame.place(x=true_size, y=0, rely=.5, width=controls_size)

    def __calculate_board_true_size(self) -> int:
        window_size = 0

        while window_size < MIN_SIZE:
            window_size += self.board_size

        return window_size

    def __setup_grid_frame(self, parent: tk.Misc) -> tk.Canvas:
        self.grid = tk.Canvas(parent, background=Item.Empty.value)
        self.cell_size = self.__calculate_board_true_size() // self.board_size
        return self.grid

    def __setup_info_frame(self, parent: tk.Misc) -> tk.Frame:
        info_frame = tk.Frame(parent)
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)

        for i, (name, value) in enumerate(self._infos):
            tk.Label(info_frame, text=str(name), font=('Comic Sans MS', 12)) \
                .grid(row=i, column=0, sticky='E', padx=10)
            value_lbl = tk.Label(info_frame, text=str(value), font=('Comic Sans MS', 13))
            value_lbl.grid(row=i, column=1)
            self._info_labels.append(value_lbl)

        return info_frame

    def __setup_control_frame(self, parent: tk.Misc) -> tk.Frame:
        control_frame = tk.Frame(parent)

        buttons = {
            event: tk.Button(control_frame,
                             text=event.value[0],
                             font=('Arial', 14),
                             background=event.value[1],
                             activebackground=event.value[2],
                             command=lambda e=event: self.callback(e),
                             pady=10,
                             width=12)
            for event in Event
        }

        for btn in buttons.values():
            btn.pack()

        return control_frame

    def update_board(self, board: Board):
        assert board.board_size == self.board_size, 'board size does not match specified at construction'

        self.grid.delete('all')
        for x, row in enumerate(board.board):
            for y, item in enumerate(row):
                self.update_cell(x, y, item)

    def update_cell(self, x: int, y: int, item: Item):
        start_coords = x * self.cell_size, y * self.cell_size
        end_coords = map(lambda c: c + self.cell_size, start_coords)

        self.grid.create_oval(*start_coords, *end_coords,
                              fill=item.value, width=0)

    def update_infos(self, info_changes: dict[Any, Any]):
        for name, value in info_changes.items():
            name = str(name)
            value = str(value)

            rows = [i for i, info in enumerate(self._infos) if info[0] == name]
            assert len(rows) > 0, f'Info {name} not found!'
            row = rows[0]

            self._infos[row] = name, value
            self._info_labels[row].config(text=value)
