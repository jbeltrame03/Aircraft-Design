import numpy as np
import atmosprops,math # type: ignore
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import aircraft, analyses #type: ignore


concept_4 = aircraft.aircraft(2.5*1.5, 670000)
concept_4.set_weights(110000, 400000)
concept_4.wing_geometry(94.403, 10, 47.5, 183.2, 9563.28, 3.509, .12, 0, 0.3, 1)
concept_4.set_engine(0.578, 4, 16640, 97000)
concept_4.update_MTOW()
 
M = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
M = np.linspace(0.5, 1, num=100)
h = [30000,35000,40000,45000,50000,55000]
L_D = []
CDo_p = []
CDi_p = []
CDw_p = []
CD_tot = []

for i in M:
    #for j in h:
        concept_4.set_flight_param(i, 45000, 0.85)
        [CL,CD] = concept_4.calculate_CL_CD()
        L_D.append(float(CL/CD))
        print(f"L/D={CL/CD}")
plt.figure()
plt.plot(M, L_D)
plt.show()
'''
for i in M:
    #for j in h:
        concept_4.set_flight_param(i, 45000, 0.85)
        [CDo, CDw, CDi] = (concept_4.get_Drag_Buildup())
        #L_D.append(float(CL/CD))
        CDo_p.append(CDo)
        CDi_p.append(CDi)
        CDw_p.append(CDw)
        CD_tot.append(CDo+CDi+CDw)

       #print(f"M={i}, h={45000}, L/D={CL/CD}")

plt.figure()
plt.plot(M, CDo_p)
plt.plot(M, CDi_p)
plt.plot(M, CDw_p)
plt.plot(M, CD_tot)
plt.legend(["CDO", "CDi", "CDw", "CD"])

plt.show()



'''
fig = go.Figure(go.Carpet(a=M, b=h, y=L_D, aaxis=dict(tickprefix = 'M=',gridcolor='black', linecolor='black', smoothing=1.3),
    baxis=dict(tickprefix = 'h=',gridcolor='black', linecolor='black', smoothing=1.3)))

fig.update_layout(
    title_text="L/D Sensitivity with M and Altitude (ft)", # Use title_text or title=dict(text="...")
    title_x=0.5, # Centers the title above the plot
    title_font=dict(size=24, family="Arial", color="black") # Optional: Customize font
)

fig.show()

