import numpy as np

point1x = float(input('1st point x coordinate:'))
point1y = float(input('1st point y coordinate:'))
point2x = float(input('2nd point x coordinate:'))
point2y = float(input('2nd point y coordinate:'))

m = ((np.log10(point2y/point1y))/(np.log10(point2x/point1x)))
b = (np.log10(point1y)-(m*np.log10(point1x)))

print("\n" + "slope (m): {}".format("%.4f" % m) + "\n" + "F(x=1) (b): {}".format("%.4f" % b))
