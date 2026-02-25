import numpy as np
import matplotlib.pyplot as plt
import atmosprops


plt.figure()

#Estimate Parameters

CDo = 0.05

e = 0.75
AR = 10
k = 1/(np.pi*e*AR)

h = 40000
M = 0.9

color = ["#de324c", "#f4895f", "#f8e16f", "#95cf92"]
W_S = np.linspace(1, 200, num=1000)


q = 0.5 * atmosprops.imperial_atmosphere(h).density() * ((atmosprops.imperial_atmosphere(h).speed_of_sound()*M)**2)
T_W1 = (((q)*CDo/(W_S)) + ((W_S*k)/q))

plt.plot(W_S, T_W1, color="#6f1926", lw=2)
#plt.plot(W_S, T_W0, color="#6f1926", lw=2)

#plt.legend(['Sustained Turn @ 9g V=1600 fps', f'Cruise @ FL400 M={M[0]}', f'Dash @ FL300 M={M[1]}', f'Dash @ SL M={M[2]}', 'Combat @ FL100 M=2.8', 'Design Wing Loading = 82 lb/ft^2', 'Non Afterburning T/W=0.82', 'Afterburning T/W=1.33', 'W/S @ Mid-Mission Fuel'])

#plt.title("MTOW = 65,500 lbs, Thrust = 54,000 lbs, w/ Afterburner = 82,000 lbs")

#plt.vlines(W_S[630], 0, 100)

plt.ylim([0,2])
plt.xlim([0,200])
plt.xlabel("W/S [lb/ft^2]")
plt.ylabel("T/W")
plt.grid(True, which="both")
plt.show(block=False)
 
 
plt.show()