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
M = 0.9
h = 45000
q = atmosprops.imperial_atmosphere(h).density() * ((atmosprops.imperial_atmosphere(h).speed_of_sound()*M)**2)
q = float(q)
AR = 8
W_S = 100
T_W = []
e = [0.7,0.8,0.9,1.0]
CDo = [0.01, 0.02, 0.03,0.04]
T_W1 = []
for i in e:
    for j in CDo:
        k = 1/(math.pi*i*AR)
        T_W1.append(((q*j)/(W_S)) + ((W_S*k)/q))
        print(f"e={i}, CDo={j}, T/W={(((q*j)/(W_S)) + ((W_S*k)/q))}")
    T_W.append(T_W1)
    T_W1 = []

for i in T_W:
    print(i)

print(type(CDo))
fig = go.Figure(go.Carpet(a=CDo, b=e, y=T_W, aaxis=dict(tickprefix = 'CDo=',gridcolor='black', linecolor='black', smoothing=1.3),
    baxis=dict(tickprefix = 'e=',gridcolor='black', linecolor='black', smoothing=1.3)))

fig.update_layout(
    title_text="T/W Sensitivity with CDo and e (oswalds efficiency)", # Use title_text or title=dict(text="...")
    title_x=0.5, # Centers the title above the plot
    title_font=dict(size=24, family="Arial", color="black") # Optional: Customize font
)
fig.show()

