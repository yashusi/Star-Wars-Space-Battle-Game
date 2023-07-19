import matplotlib as mpl

"""from svgpathtools import svg2paths
from svgpath2mpl import parse_path

vdroid_path, attributes = svg2paths('Untitled-1.svg')

vdroid_marker = parse_path(attributes[0]['d'])


vdroid_marker.vertices -= vdroid_marker.vertices.mean(axis=0)"""

import matplotlib.pyplot as plt

from matplotlib.offsetbox import OffsetImage, AnnotationBbox

plt.rcParams["figure.figsize"] = [7.5, 3.5]
plt.rcParams["figure.autolayout"] = True

def getImage(path):
   return OffsetImage(plt.imread(path, format="png"), zoom=.1)

paths = ['vdroid.png', 'vdroid.png']

x = [4, 14]
y = [3, 12]

#x = 23
#y = 6

fig, ax = plt.subplots()
for x0, y0, path in zip(x, y, paths):
   ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
   ax.add_artist(ab)
plt.xticks(range(-20, 20))
plt.yticks(range(-20, 20))
plt.show()



"""plt.plot(x,y, color = 'black')

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
  
# giving a title to my graph
plt.title('My first graph!')
  
# function to show the plot
plt.show()"""