import struct_weight, atmosprops
import plotly.graph_objects as go

'''

Study to analyze what factors most impact the weight of the aircrafts wing
CR and LE
'''

weight = struct_weight.weights(600000, 2.5)

W = []
W_temp = []
tc_root = 0.12
Cr = [40,50,60,70,80,90]
Ct = 10
LE = [30,40,50,60,70,80]
b = 180

for i in Cr:
    for j in LE:
        weight.add_wing(i, Ct, tc_root, j, b, 0.3*Ct, 0.5*b)
        W_temp.append(weight.get_Struct_Weight())
        weight.reset_weight()
    W.append(W_temp)
    W_temp = []

print(W)
fig = go.Figure(go.Carpet(a=Cr, b=LE, y=W, aaxis=dict(tickprefix = 'Cr=',gridcolor='black', linecolor='black', smoothing=1.3),
    baxis=dict(tickprefix = 'LE=',gridcolor='black', linecolor='black', smoothing=1.3)))

fig.update_layout(
    title_text="Wing Weight Sensitivity to root chord snd LE sweep", # Use title_text or title=dict(text="...")
    title_x=0.5, # Centers the title above the plot
    title_font=dict(size=24, family="Arial", color="black") # Optional: Customize font
)


fig.show()

