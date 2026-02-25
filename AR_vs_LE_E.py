import numpy as np
import atmosprops,math # type: ignore
import matplotlib.pyplot as plt
import plotly.graph_objects as go

 
'''
 
Analyze how AR and W/S effect the T/W loading
Analyze how
 
'''


#e = np.linspace(0.3, 1.0, num=15)
#print(e)
LE = [30,40,50,60,70,80]
AR = [1,3,5,7,9,11]
e = []
e_temp = []
k = []
k_tmp = []
for i in LE:
    for j in AR:
        print((i))
        print((j))
        e_temp.append((4.61*(1.0-(0.045*(float(j)**0.68)))*((np.cos(np.deg2rad(float(i))))**0.15))-3.1)
        k_tmp.append(1/(np.pi*j*((4.61*(1.0-(0.045*(float(j)**0.68)))*((np.cos(np.deg2rad(float(i))))**0.15))-3.1)))
    e.append(e_temp)
    e_temp = []
    k.append(k_tmp)
    k_tmp = []
print(e)
print(k)
fig = go.Figure(go.Carpet(a=AR, b=LE, y=e, aaxis=dict(tickprefix = 'AR=',gridcolor='black', linecolor='black', smoothing=1.3),
    baxis=dict(tickprefix = 'LE Sweep=',gridcolor='black', linecolor='black', smoothing=1.3)))

fig.update_layout(
    title_text="Oswalds Efficiency Sensitivity to AR and Leading Edge Sweep", # Use title_text or title=dict(text="...")
    title_x=0.5, # Centers the title above the plot
    title_font=dict(size=24, family="Arial", color="black") # Optional: Customize font
)
fig.show()

fig = go.Figure(go.Carpet(a=AR, b=LE, y=k, aaxis=dict(tickprefix = 'AR=',gridcolor='black', linecolor='black', smoothing=1.3),
    baxis=dict(tickprefix = 'LE Sweep=',gridcolor='black', linecolor='black', smoothing=1.3)))

fig.update_layout(
    title_text="CDi Efficiency (k) Sensitivity to AR and Leading Edge Sweep", # Use title_text or title=dict(text="...")
    title_x=0.5, # Centers the title above the plot
    title_font=dict(size=24, family="Arial", color="black") # Optional: Customize font
)
fig.show()

