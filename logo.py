import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge, Circle

fig = plt.figure(figsize=[10,10])
ax = fig.add_subplot(111)
c = plt.Circle((0,0), radius=3.0,fc='#227885',lw=0.0, zorder=0)##29737e
ax.add_patch(c)

circle_size = 0.3

x1 = 2.0
x2 = 2.0*np.cos(np.pi/3.0)
x3 = 2.0*np.cos(2*np.pi/3.0)
x4 = -2.0
x5 = x3
x6 = x2

y1 = 0.0
y2 = 2.0*np.sin(np.pi/3.0)
y3 = y2
y4 = 0.0
y5 = 2.0*np.sin(4*np.pi/3.0)
y6 = y5

my_color = '#FFFFFF'

c1 = plt.Circle((x1, y1), radius=circle_size, fc=my_color,lw=0.0, zorder=1)
ax.add_patch(c1)
c2 = plt.Circle((x2, y2), radius=circle_size, fc=my_color,lw=0.0, zorder=2)
ax.add_patch(c2)
c3 = plt.Circle((x3, y3), radius=circle_size, fc=my_color,lw=0.0, zorder=3)
ax.add_patch(c3)
c4 = plt.Circle((x4, y4), radius=circle_size, fc=my_color,lw=0.0, zorder=4)
ax.add_patch(c4)
c5 = plt.Circle((x5, y5), radius=circle_size, fc=my_color,lw=0.0, zorder=5)
ax.add_patch(c5)
c6 = plt.Circle((x6, y6), radius=circle_size, fc=my_color,lw=0.0, zorder=6)
ax.add_patch(c6)


c7 = plt.Circle((0.0, 0.5), radius=circle_size, fc='white', lw=0.0, zorder=7)
ax.add_patch(c7)
c8 = plt.Circle((0.0, -0.5), radius=circle_size, fc='white', lw=0.0, zorder=8)
ax.add_patch(c8)

x_1 = np.linspace(x1, x2, 20)
x_2 = np.linspace(x2, x3, 20)
x_3 = np.linspace(x3, x4, 20)
x_4 = np.linspace(x4, x5, 20)
x_5 = np.linspace(x5, x6, 20)
x_6 = np.linspace(x6, x1, 20)

line_width = 20
m = (y2-y1)/(x2-x1)
y_1 = m*(x_1-x1)+y1
plt.plot(x_1, y_1, linewidth=line_width,color=my_color)

m = (y3-y2)/(x3-x2)
y_2 = m*(x_2-x2)+y2
plt.plot(x_2, y_2, linewidth=line_width,color=my_color)

m = (y4-y3)/(x4-x3)
y_3 = m*(x_3-x3)+y3
plt.plot(x_3, y_3, linewidth=line_width,color=my_color)

m = (y5-y4)/(x5-x4)
y_4 = m*(x_4-x4)+y4
plt.plot(x_4, y_4, linewidth=line_width,color=my_color)

m = (y6-y5)/(x6-x5)
y_5 = m*(x_5-x5)+y5
plt.plot(x_5, y_5, linewidth=line_width,color=my_color)

m = (y1-y6)/(x1-x6)
y_6 = m*(x_6-x6)+y6
plt.plot(x_6, y_6, linewidth=line_width,color=my_color)

plt.fill_between(x_1, y_1, y_6[::-1], color = '#34b1c3')
plt.fill_between(x_5, y_2[::-1], y_5, color = '#34b1c3')
plt.fill_between(x_4, y_4, y_3[::-1], color = '#34b1c3')

ax.set_ylim([-3.1, 3.1])
ax.set_xlim([-3.1, 3.1])
plt.axis('off')
plt.savefig('/Users/christian/logo.pdf',bbox_inches='tight')
plt.show()