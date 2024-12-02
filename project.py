import matplotlib.pyplot as plt
from matplotlib import widgets
import numpy as np


# Constants
graph_start = -5
graph_end = 5
graph_point_density = 100

parameter_starting_value = 0
parameter_slider_range = (graph_start, graph_end)

cobweb_starting_point = 0
cobweb_slider_range = (graph_start, graph_end)
cobweb_iteration_count = 25

def function(x, a):
    return a * x * (1 - x)


# Plot Function graph
fig, axes = plt.subplots(nrows=1, ncols=2)


# Graph 2
# TODO
ax2 = axes[1]
ax2.set_position([0.55, 0.1, 0.4, 0.6])
A_MIN = 1
A_MAX = 4
A_DELTA = 0.005
NUM_IT = 200
X_INIT = 0.5

x = X_INIT
for mu in np.arange(A_MIN, A_MAX, A_DELTA):
    y = []
    for _ in range(NUM_IT):
        x = mu * x * (1.0 - x)
        y.append(x)
    ax2.plot([mu] * len(y), y, '.k', markersize=0.5)  # Feigenbaum tree
ax2.set_xlabel('$a$')
ax2.set_ylabel('$x$')
ax2.set_title('Feigenbaum Tree')






# Graph 1
ax1 = axes[0]
# Data
x = np.linspace(graph_start, graph_end, graph_point_density)
a = parameter_starting_value
y = function(x, a)

# Configure Axes
line, = ax1.plot(x, y, color='blue', lw=2)
ax1.set_position([0.05, 0.1, 0.4, 0.6])
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('f(x) = ax(1-x)')


# Utility for drawing on graph
xx = []
yy = []
def drawLine(x1, y1, x2, y2):
    global xx, yy
    xx.append(x1)
    yy.append(y1)
    xx.append(x2)
    yy.append(y2)

def dumpLines(ax, color='black', width=1):
    global xx, yy
    result = ax.plot(xx, yy, color=color, lw=width)
    xx, yy = [], []
    return result
def clearLines():
    global xx, yy
    xx, yy = [], []
def drawSingleSine(ax, x1, y1, x2, y2, color='black', width=1):
    clearLines()
    drawLine(x1, y1, x2, y2)
    dumpLines(ax=ax, color=color, width=width)
    clearLines()


# Cobweb
plt.subplot(1, 2, 1)
plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
drawSingleSine(ax1, graph_start, graph_start, graph_end, graph_end, color='black', width=1)
drawSingleSine(ax1, graph_start, 0, graph_end, 0, color='black', width=1)
drawSingleSine(ax1, 0, graph_start, 0, graph_end, color='black', width=1)


def drawCobweb(iterationPoint: float):
    x = iterationPoint
    fx = function(x, a)
    drawLine(x, 0, x, fx)
    for _ in range(cobweb_iteration_count):
        drawLine(x, fx, fx, fx)
        ffx = function(fx, a)
        drawLine(fx, fx, fx, ffx)
        x = fx
        fx = ffx

drawCobweb(cobweb_starting_point)
cobweb_graph, = dumpLines(ax=ax1, color='green', width=1)


# Parameter "a" Slider
parameter_slider = widgets.Slider(
    plt.axes([0.2, 0.95, 0.6, 0.05]),
    'Parameter "a"',
    parameter_slider_range[0],
    parameter_slider_range[1],
    valinit=a
)

def update_parameter_a(val):
    global a
    a = parameter_slider.val
    line.set_ydata(function(x, a))
    clearLines()
    drawCobweb(cobweb_starting_point)
    cobweb_graph.set_xdata(xx)
    cobweb_graph.set_ydata(yy)

parameter_slider.on_changed(update_parameter_a)


# Cobweb Slider
cobweb_slider = widgets.Slider(
    plt.axes([0.3, 0.90, 0.4, 0.05]),
    'Cobweb Iteration Point',
    cobweb_slider_range[0],
    cobweb_slider_range[1],
    valinit=cobweb_starting_point
)

def update_cobweb(val):
    global cobweb_starting_point
    cobweb_starting_point = cobweb_slider.val
    clearLines()
    drawCobweb(cobweb_starting_point)
    cobweb_graph.set_xdata(xx)
    cobweb_graph.set_ydata(yy)

cobweb_slider.on_changed(update_cobweb)


# On click function value display
annot = ax1.annotate(
    "", xy=(0, 0), xytext=(10, 10),
    textcoords="offset points",
    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7),
    arrowprops=dict(arrowstyle="->", color='black')
)
annot.set_visible(False)

def handle_click(mouse_event):
    ax = axes[0]
    if mouse_event.inaxes != ax:
        annot.set_visible(False)
        fig.canvas.draw_idle()
        return

    if mouse_event.button == 2:
        # cobweb_slider.val = mouse_event.xdata
        cobweb_slider.set_val(mouse_event.xdata)
        update_cobweb(cobweb_slider.val)
        fig.canvas.draw_idle()

    if mouse_event.button == 3:
        x, y = mouse_event.xdata, mouse_event.ydata
        point_val = function(mouse_event.xdata, parameter_slider.val)
        print(f'Clicked point: ({x}, {point_val})')

        annot.xy = (x, point_val)
        annot.set_text(f'({x:.2f}, {point_val:.2f})')
        annot.set_visible(True)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', handle_click)

def handle_motion(mouse_event):
    ax = axes[0]
    line.set_xdata(np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], graph_point_density))
    line.set_ydata(function(line.get_xdata(), a))

fig.canvas.mpl_connect('motion_notify_event', lambda e: handle_motion(e))


plt.show()
