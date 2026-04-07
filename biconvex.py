#Program to iterate and test different Airfoil configs
import matplotlib.pyplot as plt
import numpy as np
 
def export(coordinates, name):
 
    save_loc = "/Users/joshbeltrame/OneDrive/AIAA Navy NGAD Design/" + name + ".csv"
    np.savetxt(save_loc, np.transpose(coordinates), delimiter=",")
 
 
 
xl = 0.5
tl = 0.05
xu = 0.5
tu = 0.05
 
 
x = np.linspace(0,1, num=50)
 
yu = tu * x * ((1 - 2*xu)*x**2 + (3*xu**2 - 1)*x + xu*(2 - 3*xu)) / (xu**2 * (1 - xu)**2)
yl = -tl * x * ((1 - 2*xl)*x**2 + (3*xl**2 - 1)*x + xl*(2 - 3*xl)) / (xl**2 * (1 - xl)**2)
t_c = max(yu) + -1 * min(yl)
print(t_c)
 
plt.figure()
[x, x[::-1]]
output_x = []
output_y = []
 
for i in range(len(x)):
    output_x.append(x[::-1][i])
    output_y.append(yu[::-1][i])
 
for i in range(len(x)):
    output_x.append(x[i])
    output_y.append(yl[i])
 
 
 
 
export([output_x, output_y], "BICONVEX_010")
plt.plot(output_x, output_y)
plt.ylim([-0.5, 0.5])
plt.grid(visible=True)
plt.show()