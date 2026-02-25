import SALib.sample.sobol
import SALib.analyze.sobol
import numpy as np
import struct_weight, HLS_geom
import plotly.express as px
import pandas as pd

def weight(Cr, Ct, tc_root, LE_sweep, b):
        Wo = 600000
        Nz = 2.5
        c_CS = 0.3*Ct
        b_CS = 0.5*b
        geometry = HLS_geom.Geometry(Cr, Ct, b, LE_sweep)
        CS_geom = HLS_geom.Geometry(c_CS, c_CS, b_CS, 0)
        t1 = (Wo*Nz)**0.557
        t2 = geometry.getArea()**0.649
        t3 = geometry.getAspectRatio()**0.5
        t4 = tc_root**-0.4
        t5 = (1 + geometry.getLambda())**0.1
        t5 = np.cos(np.deg2rad(geometry.getSweepChord(0.25)))**-1
        t6 = CS_geom.getArea()**0.1

        W_wing = 0.0051*t1*t2*t3*t4*t5*t6
        return W_wing


N = 1024*2*2*2*2


problem = {
    "num_vars": 5, 
    "names": ["Cr", "Ct", "b", "LE", "tc"], 
    "bounds": [[40,100], [5,20], [80, 185], [30,70], [0.06, 0.16]]
}

sample = SALib.sample.sobol.sample(problem, N)
Y = np.empty([sample.shape[0]])

for i in range(len(Y)):
    x = sample[i]
    Y[i] = weight(x[0], x[1], x[4], x[3], x[2])

sensitivity = SALib.analyze.sobol.analyze(problem, Y)
print(sensitivity["ST"])

data = {'Variable': ["Root Chord", "Tip Chord", "Span", "Leading Edge Sweep", "t/c Ratio"], 'Sensitivity': sensitivity["S1"]}
df = pd.DataFrame(data)
fig = px.bar(df, x="Variable", y="Sensitivity")
fig.update_layout(
    title_text="Wing Weight Sensitivity First Order Sobol Coefficients", # Use title_text or title=dict(text="...")
    title_x=0.5, # Centers the title above the plot
    title_font=dict(size=24, family="Arial", color="black") # Optional: Customize font
)
fig.show()

data = {'Variable': ["Root Chord", "Tip Chord", "Span", "Leading Edge Sweep", "t/c Ratio"], 'Sensitivity': sensitivity["ST"]}
df = pd.DataFrame(data)
fig = px.bar(df, x="Variable", y="Sensitivity")
fig.update_layout(
    title_text="Wing Weight Sensitivity Sobol Total Sensitivity Coefficients", # Use title_text or title=dict(text="...")
    title_x=0.5, # Centers the title above the plot
    title_font=dict(size=24, family="Arial", color="black") # Optional: Customize font
)
fig.show()
