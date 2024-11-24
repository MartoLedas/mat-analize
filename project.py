import matplotlib.pyplot as plt
from matplotlib import widgets
import numpy as np

# Graph 1
# TODO: make cobweb graph update with the slider
# TODO: make cobweb graph point enterable

# Constants
graphStart = -10
graphEnd = 10
graphPointCount = 1000

iterationPoint = 0.9
iterationCount = 10

def function(x, a):
    return a * x * (1 - x)


# Data
x = np.linspace(graphStart, graphEnd, graphPointCount)
a = 1
y = function(x, a)

# Plot Function graph
fig, axes = plt.subplots(nrows=1, ncols=2)
ax = axes[0]
line, = ax.plot(x, y, color='blue', lw=2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('f(x) = ax(1-x)')


# Utility wrapper for drawing on graph
def drawLine(x1, y1, x2, y2, width=1, color='green'):
    plt.plot([x1, x2], [y1, y2], color=color, lw=width)


# Cobweb
plt.subplot(1, 2, 1)
plt.grid(color = 'black', linestyle = '--', linewidth = 0.5)
drawLine(graphStart, graphStart, graphEnd, graphEnd, width=1, color='black')

def drawCobweb(iterationPoint: float):
    x = iterationPoint
    fx = function(x, a)
    drawLine(x, 0, x, fx)

    for _ in range(iterationCount):
        drawLine(x, fx, fx, fx)
        ffx = function(fx, a)
        drawLine(fx, fx, fx, ffx)
        x = fx
        fx = ffx
drawCobweb(iterationPoint)



# Slider
slider = widgets.Slider(
    plt.axes([0.2, 0.95, 0.6, 0.05]),
    'Amplitude',
    -5.0,
    5.0,
    valinit=a
)

def update(val):
    a = slider.val
    line.set_ydata(function(x, a))
    
slider.on_changed(update)


# On click value display
annot = ax.annotate(
    "", xy=(0, 0), xytext=(10, 10),
    textcoords="offset points",
    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.7),
    arrowprops=dict(arrowstyle="->", color='black')
)
annot.set_visible(False)

def print_clicked_point(event):
    if event.inaxes != ax:
        annot.set_visible(False)
        fig.canvas.draw_idle()
        return
    x, y = event.xdata, event.ydata
    point_val = function(event.xdata, slider.val)
    print(f'Clicked point: ({x}, {point_val})')

    annot.xy = (x, point_val)
    annot.set_text(f'({x:.2f}, {point_val:.2f})')
    annot.set_visible(True)
    fig.canvas.draw_idle()

fig.canvas.mpl_connect('button_press_event', print_clicked_point)


plt.show()
