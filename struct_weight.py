import math, HLS_geom # type: ignore
import numpy as np


class weights:

    W_S = 0
    def __init__(self, Wo, Nz):
        self.Wo = Wo
        self.Nz = Nz
        pass
    

    def add_wing(self, Cr, Ct, tc_root, LE_sweep, b, c_CS, b_CS):
        geometry = HLS_geom.Geometry(Cr, Ct, b, LE_sweep)
        CS_geom = HLS_geom.Geometry(c_CS, c_CS, b_CS, 0)
        t1 = (self.Wo*self.Nz)**0.557
        t2 = geometry.getArea()**0.649
        t3 = geometry.getAspectRatio()**0.5
        t4 = tc_root**-0.4
        t5 = (1 + geometry.getLambda())**0.1
        t5 = np.cos(np.deg2rad(geometry.getSweepChord(0.25)))**-1
        t6 = CS_geom.getArea()**0.1

        W_wing = 0.0051*t1*t2*t3*t4*t5*t6
        self.W_S += W_wing


    def add_HT(self, all_moving, w_f, Cr, Ct, b, Lt, LE_sweep, c_CS, b_CS):

        geometry = HLS_geom.Geometry(Cr, Ct, b, LE_sweep)
        elevator = HLS_geom.Geometry(c_CS, c_CS, b_CS, 0)
        if all_moving:
            UHT = 1.17
        else:
            UHT = 1

        Ky = 0.3*Lt
        t1 = 0.0379*UHT
        t2 = (1+(w_f/b))**-0.25
        t3 = self.Wo**0.639
        t4 = self.Nz**0.10
        t5 = geometry.getArea()**0.75
        t5 = Lt**-1
        t6 = Ky**0.704
        t7 = math.cos(math.radians(geometry.getSweepChord(0.25)))**-1
        t8 = geometry.getAspectRatio()**0.166
        t9 = (1+((elevator.getArea())/(geometry.getArea())))**0.1

        W_HT = t1*t2*t3*t4*t5*t6*t7*t8*t9
        self.W_S += W_HT
    
    def add_VT(self, T_tail, Lt, Cr, Ct, b, LE_sweep, tc_root):

        geometry = HLS_geom.Geometry(Cr, Ct, b, LE_sweep)

        if T_tail:
            HtHv = 0
        else:
            HtHv = 1

        Kz = Lt

        t1 = 0.0026*((1+HtHv)**0.225)
        t2 = self.Wo**0.556
        t3 = self.Nz**0.536
        t4 = Lt**-0.5
        t5 = geometry.getArea()**0.5
        t6 = Kz**0.875
        t7 = math.cos(math.radians(geometry.getSweepChord(0.25)))**-1
        t8 = geometry.getAspectRatio()**0.35
        t9 = tc_root**-0.5

        W_VT = t1*t2*t3*t4*t5*t6*t7*t8*t9
        self.W_S += W_VT
    

    #Sf = 16000 ' ' approx, L = 200', D=30'
    def add_fuselage(self, K_door, K_LDG, L, Sf, Cr_w, Ct_w, b_w, LE_sweep, D_f):
        geometry = HLS_geom.Geometry(Cr_w, Ct_w, b_w, LE_sweep)

        Kws = 0.75*((1+(2*geometry.getLambda()))/(1+geometry.getLambda()))*(b_w/L)*math.tan(math.radians(geometry.getSweepChord(0.25)))

        t1 = 0.3280*K_door
        t2 = K_LDG
        t3 = (self.Wo*self.Nz)**0.5
        t4 = L**0.25
        t5 = Sf**0.302
        t6 = (1+Kws)**0.04
        t7 = (L/D_f)**0.10

        W_fuse = t1*t2*t3*t4*t5*t6*t7
        self.W_S += W_fuse

    def add_Landing_Gear(self, Kneel, num_gear, L, N_nose, N_main, N_main_strut, Vs):

        if Kneel:
            Kmp = 1.126
            Knp = 1
        else:
            Kmp = 1
            Knp = 1
        W_MLG = 0.0106*Kmp*(self.Wo**0.888)*((1.5*num_gear)**0.25)*(L**0.4)*(N_main**0.321)*(N_main_strut**-0.5)*(Vs**0.1)

        W_NLG = 0.032*Knp*(self.Wo**0.646)*((1.5*num_gear)**0.2)*(L**0.5)*(N_nose**0.45)

        W_LG = W_MLG + W_NLG
        self.W_S += W_LG
    
    def add_engines(self, N_eng, W_eng, L_eng, Sn, D_eng, X_eng):
        Kng = 1.017
        N_LT = L_eng * 1.1
        N_w = D_eng * 1.1

        W_nacelle = 0.6724*Kng*(N_LT**0.1)*(self.Nz**0.119)*(W_eng**0.611)*(N_eng**0.984)*(Sn**0.224)
        W_engs = W_eng*N_eng
        W_eng_control = (5*N_eng) + (0.80*X_eng)
        W_starter = 49.19*(N_eng*W_eng*(1/1000))**0.541


    def get_Struct_Weight(self):
        return math.ceil(float(self.W_S))
    
    def add_misc(self, W_elem):
        self.W_S += W_elem



