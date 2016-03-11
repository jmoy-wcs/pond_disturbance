import numpy as np
from matplotlib import pyplot

A = np.matrix([[0.62, 0.38, 0.00],
               [0.07, 0.68, 0.25],
               [0.05, 0.00, 0.95]])

s = np.matrix([[1000, 0, 0]])

# Get the data
plot_data = []
#plot_data.append(s)
for step in range(20):
    result = s * A**step
    print step, result
    plot_data.append(np.array(result).flatten())

# Convert the data format
plot_data = np.array(plot_data)

# Create the plot
pyplot.figure(1)
pyplot.xlabel('Steps')
pyplot.ylabel('Frequency')
lines = []
for i, shape, label in zip(range(3), ['x', 'h', 'H'], ['Pond', 'Herbaceous Swamp', 'Forest']):
    line, = pyplot.plot(plot_data[:, i], shape, label="%s" % label)
    lines.append(line)
pyplot.legend(handles=lines, loc=1)
pyplot.show()
