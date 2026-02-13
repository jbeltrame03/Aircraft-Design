from ambiance import Atmosphere
import sys

#Input the altitude in feet and get different atmospheric properties in USC units.

class imperial_atmosphere:

    rho_conv = 515.37882
    sos_conv = 3.281
    T_conv = 1.8
    P_conv = 0.020885434273039
    nu_conv = 10.764

    def __init__(self, altitude):
        self.h = altitude / 3.281 #Convert to meters multiply by 3.281
        self.alt = Atmosphere(self.h)
    
    def density(self):
        return self.alt.density / self.rho_conv
    
    def speed_of_sound(self):
        return self.alt.speed_of_sound * self.sos_conv

    def temperature(self):
        return self.alt.temperature * self.T_conv
    
    def pressure(self):
        return self.alt.pressure * self.P_conv
    
    def kinematic_viscosity(self):
        return self.alt.kinematic_viscosity * self.nu_conv
    






    