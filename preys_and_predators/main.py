from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

from board import Board, BoardConfig
from board_window import BoardWindow, Event
from entity import EntityConfig

BOARD_SIZE = 100

board = Board(BOARD_SIZE, BoardConfig(
    initial_preys=200,
    initial_predators=200,
    initial_prey_energy=50,
    initial_predator_energy=200,
    predator_kill_energy=300,
    prey_config=EntityConfig(
        energy_per_move=lambda possibilites: 2,
        reproduction_cost=30,
        reproduction_energy=50,
        reproduction_threshold=60,
        reproduction_chance=0.4,
    ),
    predator_config=EntityConfig(
        energy_per_move=lambda possibilites: -possibilites // 3 - 1,
        reproduction_cost=80,
        reproduction_energy=200,
        reproduction_threshold=300,
        reproduction_chance=0.8,
    ),
))

is_playing = False
play_speed = 8  # steps/s
preys = [board.preys]
predators = [board.predators]
populations = [board.population]


def callback(event: Event):
    global is_playing, play_speed

    if event == Event.Step:
        step()
    elif event == Event.Play:
        is_playing = True
    elif event == Event.Pause:
        is_playing = False
    elif event == Event.SpeedUp:
        play_speed *= 2
        print(f'Play speed: {play_speed}')
    elif event == Event.SlowDown:
        play_speed //= 2
        print(f'Play speed: {play_speed}')


def step():
    board.step()
    window.update_board(board)

    window.update_infos({
        'Step': board.step_count,
        'Population': board.population,
        'Preys': board.preys,
        'Predators': board.predators,
    })

    preys.append(board.preys)
    predators.append(board.predators)
    populations.append(board.population)

    ax.set_xlim(0, board.step_count)
    ax.set_ylim(0, max(populations) + 100)
    preys_line.set_data(range(len(preys)), preys)
    predators_line.set_data(range(len(predators)), predators)
    population_line.set_data(range(len(populations)), populations)
    fig.canvas.draw()
    fig.canvas.flush_events()


def play_steps():
    if is_playing:
        step()

    global after_id
    after_id = window.after(1000 // play_speed, play_steps)


plt.ion()
fig = plt.figure()
fig.canvas.manager.window.wm_geometry('850x500+1030+240') # type: ignore
ax = fig.add_subplot(1, 1, 1)
ax.set_title('Population Plot')
ax.set_xlabel('Steps')

preys_line: Line2D = ax.plot(preys, color='blue', label='Preys')[0]
predators_line: Line2D = ax.plot(predators, color='red', label='Predators')[0]
population_line: Line2D = ax.plot(populations, color='green', label='All Population')[0]
ax.legend(loc='lower left')

window = BoardWindow(BOARD_SIZE, callback, [
    ('Step', board.step_count),
    ('Population', board.population),
    ('Preys', board.preys),
    ('Predators', board.predators),
])
window.update_board(board)
after_id = window.after(100, play_steps)
window.wm_protocol('WM_DELETE_WINDOW', lambda: (
    window.after_cancel(after_id),
    window.destroy(),
    plt.close()
))
window.mainloop()
