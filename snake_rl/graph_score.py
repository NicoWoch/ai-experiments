import random
from typing import Any

from matplotlib import pyplot as plt
from matplotlib.widgets import Button

from mean_stream import MeanStream


plt.ion()

fig, ax = plt.subplots()
ax.set_title('Game Results')
ax.set_xlabel('Iteration')
ax.set_ylabel('Score')

line_score, = ax.plot([], [])
line_score.set_color('blue')
line_score.set_label('AI')

line_mean, = ax.plot([], [])
line_mean.set_color('green')
line_mean.set_label('Average')

ax.legend()

manager = plt.get_current_fig_manager()
manager.window.wm_geometry("+10+300") # type: ignore

button_ax = fig.add_axes((0.4, 0.01, 0.2, 0.075))
reset_button = Button(button_ax, "Reset")

plt.subplots_adjust(bottom=0.2)

follow = True
default_ax_lims: list[float] = [0, 5, 0, 5]


def plot(stream: MeanStream):
    scores = stream.stream
    means = stream.mean
    
    line_score.set_xdata([i + 1 for i in range(len(scores))])
    line_score.set_ydata(scores)
    
    line_mean.set_xdata([i + 1 for i in range(len(means))])
    line_mean.set_ydata(means)
    
    max_x = max(len(scores), len(means), 5) + 1
    
    default_ax_lims[0] = max(0, max_x - 140)
    default_ax_lims[1] = max_x
    default_ax_lims[2] = 0
    default_ax_lims[3] = max(max(scores, default=5), max(means, default=5)) + 5
    
    if follow:
        reset_view()
    
    plt.draw()
    plt.show(block=False)


def reset_view(*_: Any) -> None:
    global follow
    follow = True
    
    ax.set_xlim(*default_ax_lims[:2])
    ax.set_ylim(*default_ax_lims[2:])
    fig.canvas.draw_idle()


reset_button.on_clicked(reset_view)


def user_interaction(*_: Any) -> None:
    global follow
    follow = False


fig.canvas.mpl_connect("button_press_event", user_interaction)
fig.canvas.mpl_connect("scroll_event", user_interaction)


if __name__ == "__main__":
    # Test code
    from time import perf_counter

    next: float = 0
    
    while True:
        if perf_counter() > next + 0.5:
            next = perf_counter()
            plot(
                MeanStream.from_array([random.randint(0, 20) for _ in range(5)], 3),
            )
        
        fig.canvas.draw_idle()
        fig.canvas.flush_events()
