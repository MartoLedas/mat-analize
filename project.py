import matplotlib.pyplot as plt
from matplotlib import widgets
import numpy as np


# Constants
graph_start = -5
graph_end = 5
graph_point_density = 50

parameter_starting_value = 0
parameter_slider_range = (-2, 4)

cobweb_starting_point = 0
cobweb_iteration_count = 100
precision = 0.01

definition_ranges = (-10, 10)

def function(x, a):
    return a * x * (1 - x)

# Plot Function graph
fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
plt.subplots_adjust(top=0.75)


# Graph 2 - Feigenbaum Tree with Bifurcation Points
ax2 = axes[1]

A_MIN = 2.5
A_MAX = 4
A_DELTA = 0.005
NUM_IT = 200
NUM_IT_TRANSIENT = 1000
X_INIT = 0.5

bifurcation_points = []

x = X_INIT
prev_unique_count = 1
for mu in np.arange(A_MIN, A_MAX, A_DELTA):
    y = []
    for it in range(NUM_IT + NUM_IT_TRANSIENT):
        x = mu * x * (1.0 - x)
        if it >= NUM_IT_TRANSIENT:
            y.append(x)

    unique_points = np.unique(np.round(y, decimals=5))
    unique_count = len(unique_points)

    # Detect bifurcation when unique count doubles
    if unique_count == 2 * prev_unique_count and mu not in bifurcation_points:
        bifurcation_points.append(mu)
        prev_unique_count = unique_count

    ax2.plot([mu] * len(y), y, '.k', markersize=0.5)

for i, mu_bif in enumerate(bifurcation_points[:3]):
    ax2.axvline(mu_bif, color='red', linestyle='--', label=f"Bifurcation {i+1}: a ≈ {mu_bif:.4f}")

ax2.axvline(A_MAX, color='blue', linestyle='--', label=f"Limit: a = {A_MAX}")


ax2.set_xlabel('$a$')
ax2.set_ylabel('$x$')
ax2.set_title('Feigenbaum Tree')
ax2.legend()


# Graph 1
ax1 = axes[0]
# Data
x = np.linspace(graph_start, graph_end, graph_point_density)
a = parameter_starting_value
y = function(x, a)

# Configure Axes
line, = ax1.plot(x, y, color='blue', lw=2)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('f(x) = ax(1-x)')


# Definition ranges
def getIterationDefRanges(start, end, step, a):
    if np.abs(a) < step:
        return "Always defined."
    iteration_count = 50
    definition_status_changes = []
    def calcIteration(x, a, count):
        if count <= 0:
            return x
        return calcIteration(function(x, a), a, count - 1)

    prev_is_inf = True
    for i in np.arange(start, end, step):
        val = calcIteration(cobweb_starting_point, i, iteration_count)
        curr_is_inf = np.isinf(val)
        if not prev_is_inf and curr_is_inf:
            definition_status_changes.append((i, 'infinite'))
        elif prev_is_inf and not curr_is_inf:
            definition_status_changes.append((i, 'finite'))
        prev_is_inf = curr_is_inf

    # print(definition_status_changes)
    defined_intervals = [val for (val, _) in definition_status_changes]

    undefined_intervals = [-np.inf]
    undefined_intervals.extend(defined_intervals)
    undefined_intervals.append(np.inf)

    try:
        undefined_intervals = [f"({undefined_intervals[i]:.2f}; {undefined_intervals[i+1]:.2f})" for i in range(0, len(undefined_intervals), 2)]
        defined_intervals = [f"({defined_intervals[i]:.2f}; {defined_intervals[i+1]:.2f})" for i in range(0, len(defined_intervals), 2)]
    except:
        undefined_intervals = []
        defined_intervals = []

    result_string = f"""Defined intervals: {' '.join(str(defined_intervals))}
Undefined intervals: {' '.join(str((undefined_intervals)))}
    """

    return result_string

definition_text = ax1.text(0, 1.1, getIterationDefRanges(*definition_ranges, precision, a),
        verticalalignment='bottom', horizontalalignment='left',
        transform=ax1.transAxes,
        color='green', fontsize=9)

def update_function_definition_ranges():
    definition_text.set_text(getIterationDefRanges(*definition_ranges, precision, a))


# Graph 3 - Orbit

ax3 = axes[2]

def update_orbit(x):
    orbit = generate_orbit(x, a, cobweb_iteration_count)
    orbit_line.set_ydata(orbit)

# Generate time series for the orbit
def generate_orbit(initial_point, a, iterations):
    orbit = [initial_point]
    x = initial_point
    for _ in range(iterations):
        x = function(x, a)
        orbit.append(x)
    return orbit

# Parameters
initial_point = cobweb_starting_point
iterations = cobweb_iteration_count

# Generate and plot the orbit time series
orbit = generate_orbit(initial_point, a, iterations)
orbit_line,  = ax3.plot(orbit, marker='o', linestyle='-')
ax3.set_xlabel("Iteration)")
ax3.set_ylabel("x")
ax3.set_title("Time Series of the Orbit")
ax3.grid()





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

ax1.grid(color = 'black', linestyle = '--', linewidth = 0.5)
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
    if np.abs(a) < precision:
        a = 0
        parameter_slider.set_val(a)
        pass
    line.set_ydata(function(x, a))
    update_cobweb(cobweb_starting_point)

    update_orbit(cobweb_starting_point)
    update_function_definition_ranges()
    fig.canvas.draw_idle()

parameter_slider.on_changed(update_parameter_a)


def update_cobweb(val):
    global cobweb_starting_point
    cobweb_starting_point = val
    clearLines()
    drawCobweb(cobweb_starting_point)
    cobweb_graph.set_xdata(xx)
    cobweb_graph.set_ydata(yy)
    fig.canvas.draw_idle()


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

    if mouse_event.button == 3:
        update_orbit(mouse_event.xdata)
        update_cobweb(mouse_event.xdata)
        update_function_definition_ranges()
        fig.canvas.draw_idle()

    if mouse_event.button == 2:
        x, y = mouse_event.xdata, mouse_event.ydata
        point_val = function(mouse_event.xdata, parameter_slider.val)
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