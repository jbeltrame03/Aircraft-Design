import struct_weight, atmosprops # type: ignore
import numpy as np
import matplotlib.pyplot as plt

class Model:

    def __init__(self, Tsl):
        self.Tsl = Tsl
    
    def thrust_altitude_NICOALI(self, h):
        P0 = atmosprops.imperial_atmosphere(0).pressure()
        T0 = atmosprops.imperial_atmosphere(0).temperature()
        P1 = atmosprops.imperial_atmosphere(h).pressure()
        T1 = atmosprops.imperial_atmosphere(h).temperature()
        return (self.Tsl*(P1/P0)*(T1/T0))
    
    def Thrust_altitude_SNORRI(self, M, h):
        throttle = 0.95

        gamma = 1.4 

        theta = atmosprops.imperial_atmosphere(h).temperature()/atmosprops.imperial_atmosphere(0).temperature()
        delta = atmosprops.imperial_atmosphere(h).pressure()/atmosprops.imperial_atmosphere(0).pressure()
        theta_0 = theta*(1+(((gamma-1)/2)*(M**2)))
        delta_0 = delta*((1+(((gamma-1)/2)*(M**2)))**(gamma/(gamma-1)))


        if theta_0 < throttle:
            return (self.Tsl*delta_0*(1-(0.49*np.sqrt(M))))
        else:
            return (self.Tsl*delta_0*(1-(0.49*np.sqrt(M))-(((3*(theta_0-throttle)))/(1.5+M))))
        
    def thrust_avg(self, M, h):
        return (self.Thrust_altitude_SNORRI(M, h)+self.thrust_altitude_NICOALI(h))*0.5
    
    def TR(self, h, M):
        theta = atmosprops.imperial_atmosphere(h).temperature()/atmosprops.imperial_atmosphere(0).temperature()
        return theta*(1+(((1.4-1)/2)*(M**2)))
    
    def thrust_altitude_Low_BPR_norm(self, M, h):

        throttle = 1

        gamma = 1.4 

        theta = atmosprops.imperial_atmosphere(h).temperature()/atmosprops.imperial_atmosphere(0).temperature()
        delta = atmosprops.imperial_atmosphere(h).pressure()/atmosprops.imperial_atmosphere(0).pressure()
        theta_0 = theta*(1+(((gamma-1)/2)*(M**2)))
        delta_0 = delta*((1+(((gamma-1)/2)*(M**2)))**(gamma/(gamma-1)))
        
        if theta_0 < throttle:
            return (self.Tsl*delta_0*0.6)
        else:
            return ((self.Tsl*delta_0*0.6)*((1-((3.8*(theta_0-throttle))/theta_0))))
   