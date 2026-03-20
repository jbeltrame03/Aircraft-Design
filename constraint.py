import numpy as np
import matplotlib.pyplot as plt
import atmosprops, thrust_model


def Takeoff_roll(CLMax, W_S, SG, alt):
    alpha =  1 #T = TSL
    beta = 1 #At MTOW weight
    rho = atmosprops.imperial_atmosphere(alt).density()
    V_stall = np.sqrt((2/(CLMax*rho))*W_S)
    VTO = 1.2*V_stall
    g = 32.2
    k_TO = VTO/V_stall
    T_W = ((k_TO**2)/(SG*rho*CLMax*g))*(W_S)*((beta**2)/alpha)
    return T_W

def cruise_speed(h, Tsl, Mcr, W_S, CDo, AR, e):
    
    T = thrust_model.Model(Tsl).Thrust_altitude_SNORRI(Mcr, h)
    rho = atmosprops.imperial_atmosphere(h).density()
    a_sos = atmosprops.imperial_atmosphere(h).speed_of_sound()
    Vcr = Mcr*a_sos
    q = 0.5*rho*Vcr*Vcr
    CDR = K2 = 0 #constant speed + alt cruise
    alpha = T/Tsl
    print(alpha)
    alpha = 0.3
    beta = 0.95
    k_prime = 1/(np.pi*AR*e)
    k_prime_prime = 0.03
    K1 = k_prime + k_prime_prime


    T_W = (beta/alpha)*((K1*(beta/q)*W_S)+K2+((CDo+CDR)/((beta/q)*W_S)))
    return T_W

def rate_of_climb(h, Tsl, Mcr, W_S, CDo, AR, e, ROC):
    
    T = thrust_model.Model(Tsl).Thrust_altitude_SNORRI(Mcr, h)
    rho = atmosprops.imperial_atmosphere(h).density()
    a_sos = atmosprops.imperial_atmosphere(h).speed_of_sound()
    Vcr = Mcr*a_sos
    q = 0.5*rho*Vcr*Vcr
    CDR = K2 = 0 #constant speed + alt cruise
    alpha = 0.3
    
    beta = 0.99
    k_prime = 1/(np.pi*AR*e)
    k_prime_prime = 0.03
    K1 = k_prime + k_prime_prime


    T_W = (beta/alpha)*((K1*(beta/q)*W_S)+K2+((CDo+CDR)/((beta/q)*W_S))+((ROC/60)/Vcr))
    return T_W







plt.figure()
plt.rcParams['savefig.dpi'] = 1200   # super high quality when saving
###############################################################################################
#Historic A/C

B_52_W = 488000
B_52_S = 4000
B_52_T = 17000*8
B_52_WS = B_52_W/B_52_S
B_52_TW = B_52_T/B_52_W
 
B_1_W = 477000
B_1_S = 1950
B_1_T = 4*17390
B_1_WS = B_1_W/B_1_S
B_1_TW = B_1_T/B_1_W
B_1_T_AB = 30780*4
B_1_TW_AB = B_1_T_AB/B_1_W


B_58_W = 176890
B_58_S = 1542
B_58_T = 10400*4
B_58_T_AB = 15000*4
B_58_WS = B_58_W/B_58_S
B_58_TW = B_58_T/B_58_W
B_58_TW_AB = B_58_T_AB/B_58_W

###############################################################################################


###############################################################################################
#Performance Parameter Estimations


CLmax = 2.5
W_S = np.linspace(0,300, num=1000)
Sg = 5000
h = 6000
cruise_alt = 40000
N_engine = 4
T_engine = 97000
Tsl = N_engine*T_engine
Mcr = 0.85
CDo = 0.015
AR = 8
e = 0.7
ROC = 4000 #FPM

###############################################################################################

T_W_takeoff = Takeoff_roll(CLmax, W_S, Sg, h)
T_W_cruise1 = cruise_speed(cruise_alt, Tsl, 0.7, W_S, CDo, AR, e)

T_W_cruise2 = cruise_speed(cruise_alt, Tsl, 0.8, W_S, CDo, AR, e)

T_W_cruise3 = cruise_speed(cruise_alt, Tsl, 0.9, W_S, CDo, AR, e)

plt.plot(W_S, T_W_takeoff, lw=2)
plt.plot(W_S, T_W_cruise1, lw=2)
plt.plot(W_S, T_W_cruise2, lw=2)
plt.plot(W_S, T_W_cruise3, lw=2)

plt.ylim([0,1])
plt.xlabel("W_TO/S [lb/ft^2]")
plt.ylabel("T_SL/W_TO")
plt.grid(True, which="both")
plt.show(block=False)
plt.xlim([0,300])

plt.scatter(B_52_WS, B_52_TW)
plt.scatter(B_1_WS, B_1_TW)
plt.scatter(B_1_WS, B_1_TW_AB)
plt.scatter(B_58_WS, B_58_TW)
plt.scatter(B_58_WS, B_58_TW_AB)
plt.legend(["Takeoff Requirements","Cruise Requirements M = 0.7","Cruise Requirements M = 0.8","Cruise Requirements M = 0.9","B-52", "B-1 (no Afterburner)", "B-1 (Afterburner)", "B-58 (no Afterburner)", "B-58 (Afterburner)"], loc="upper left")
plt.title("B-72 Constraint Diagram")
 
plt.show()