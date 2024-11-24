import matplotlib.pyplot as plt
from matplotlib import widgets
import numpy as np

def function(x, a):
    return -a * x * (1 - x)

# Data
x = np.linspace(-10, 10, 100)
a = 1
y = function(x, a)

# Plot
fig, axes = plt.subplots(nrows=1,ncols=2)
ax = axes[0]
line, = ax.plot(x, y, color='blue', lw=2)
ax.set_xlabel('x')
ax.set_ylabel('y')

ax.set_title('f(x) = ax(1-x)')

def drawLine(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], color='black', lw=1)

plt.subplot(1, 2, 1)
drawLine(-100, -100, 100, 100, width=1)
iterationPoint = 1.1
iterationCount = 1
for i in range(1):
    iterationValue = function(iterationPoint, a)
    drawLine(iterationPoint, 0, iterationPoint, iterationValue)
    drawLine(iterationPoint, iterationValue, iterationValue, iterationValue)
    iterationPoint = iterationValue



# Update data based on slider value
def update(val):
    a = slider.val
    line.set_ydata(function(x, a))

# Slider
slider = widgets.Slider(
    plt.axes([0.2, 0.95, 0.6, 0.05]),
    'Amplitude',
    -5.0,
    5.0,
    valinit=a
)

# Annotation
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


slider.on_changed(update)
fig.canvas.mpl_connect('button_press_event', print_clicked_point)


plt.show()
