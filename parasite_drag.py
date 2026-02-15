import struct_weight, atmosprops, thrust_model, HLS_geom # type: ignore
import numpy as np
import matplotlib.pyplot as plt

class lift_drag:

    

    def __init__(self):
        self.CDo = 0
        self.surfaces = {}
        self.e = 0
        self.k = 0
        self.Sref = 0
        pass
    
    def set_Sref(self, Sref):
        self.Sref = Sref

    def set_Wing_Geometry(self, Cr, Ct, Swet, t_c, xc_max, LE, b, num_surf):
        wing = HLS_geom.Geometry(Cr, Ct, b, LE)
        surface = {
             "type" :"WING", 
             "geometry" : wing, 
             "Root": Cr, 
             "Tip": Ct, 
             "Wet Area": Swet, 
             "t/c": t_c, 
             "x/c": xc_max, 
             "b": b, 
             "LE": LE
             }
        self.surfaces.setdefault(num_surf, []).append(surface)

    def set_VT_geometry(self, Cr, Ct, Swet, t_c, xc_max, LE, b, num_surf):
        VT = HLS_geom.Geometry(Cr, Ct, b, LE)
        surface = {
             "type" :"VT", 
             "geometry" : VT, 
             "Root": Cr, 
             "Tip": Ct, 
             "Wet Area": Swet, 
             "t/c": t_c, 
             "x/c": xc_max, 
             "b": b, 
             "LE": LE
             }
        self.surfaces.setdefault(num_surf, []).append(surface)

    def set_fuselage_Geometry(self, l, d, Swet, num_surf):
        surface = {
             "type" :"FUSELAGE", 
             "Length": l, 
             "Diameter": d, 
             "Wet Area": Swet, 
            }
        self.surfaces.setdefault(num_surf, []).append(surface)

    def add_Wing_surface(self, M, h, itr):
        a_sos = atmosprops.imperial_atmosphere(h).speed_of_sound()
        nu = atmosprops.imperial_atmosphere(h).kinematic_viscosity()
        V = M*a_sos

        Cr = self.surfaces.get(itr)[0]["Root"]
        Ct = self.surfaces.get(itr)[0]["Tip"]
        Swet = self.surfaces.get(itr)[0]["Wet Area"]
        t_c = self.surfaces.get(itr)[0]["t/c"]
        xc_max = self.surfaces.get(itr)[0]["x/c"]
        b = self.surfaces.get(itr)[0]["b"]
        LE = self.surfaces.get(itr)[0]["LE"]
        wing = HLS_geom.Geometry(Cr, Ct, b, LE)

        Re_r = (Cr*V)/nu
        Re_t = (Ct*V)/nu

        Cf_r = 0.455/((np.log10(Re_r))**2.58)
        Cf_t = 0.455/((np.log10(Re_t))**2.58)
        Cf = (Cf_r + Cf_t)*0.5

        FF = (1 + ((0.6/xc_max)*t_c) + (100*(t_c**4))) * ((1.34*(M**0.18))*((np.cos(np.deg2rad(wing.getSweepChord(xc_max))))**0.28))
        IF = 1 

        CDo = (FF*IF*Cf*Swet)/self.Sref

        return CDo

    def add_fuselage(self, M, h, itr):
        a_sos = atmosprops.imperial_atmosphere(h).speed_of_sound()
        nu = atmosprops.imperial_atmosphere(h).kinematic_viscosity()
        V = M*a_sos

        l = self.surfaces.get(itr)[0]["Length"]
        d = self.surfaces.get(itr)[0]["Diameter"]
        Swet = self.surfaces.get(itr)[0]["Wet Area"]        

        Re = (l*V)/nu
        f = l/d
        Cf = 0.455/((np.log10(Re))**2.58)
        FF = 1 + (60*(f**-3)) + (f/400)
        IF = 1
        CDo = (FF*IF*Cf*Swet)/self.Sref
        return CDo
         
    def calculate_CDo(self, M, h):
        tmp_CDo = 0
        for i in range(len(self.surfaces)):
            if (self.surfaces.get(i+1)[0]["type"] == "WING"):
                tmp_CDo += self.add_Wing_surface(M, h, i+1)
            elif (self.surfaces.get(i+1)[0]["type"] == "VT"):
                tmp_CDo += self.add_Wing_surface(M, h, i+1)
            elif(self.surfaces.get(i+1)[0]["type"] == "FUSELAGE"):
                tmp_CDo += self.add_fuselage(M, h, i+1)  
        return tmp_CDo[0] 
        
    def get_CDo(self):
        return self.CDo
    
    def get_Surfaces(self):
        return self.surfaces
    
    def calculate_CDw(self, M, Mcrit):
        if M >= Mcrit:
            return 100 * ((M - Mcrit)**4)
        else:
            return 0
    
    def set_Oswalds(self, LE, AR):
        self.e = (4.61*(1-(0.045*(AR**0.68)))*((np.cos(np.deg2rad(LE)))**0.15))-3.1
        self.k = 1/(np.pi*self.e*AR)

    
    def calculate_CL_CD(self, M, h, W, Mcrit):
        a_sos = atmosprops.imperial_atmosphere(h).speed_of_sound()
        rho = atmosprops.imperial_atmosphere(h).density()
        V = M*a_sos
        q = 0.5*rho*V*V
        print(f"W={W}, V={V}, S={self.Sref}")
        CL = W/(q*self.Sref)
        CDi = CL*CL*self.k
        print(f"V={V} q={q} CL={CL} CDi={CDi}")
        CDo = self.calculate_CDo(M, h)
        CDw = self.calculate_CDw(M, Mcrit)
        CD = CDo + CDi + CDw

        return [CL, CD]

    def update_Param(self, surf, param, value):
        for i in range(len(self.surfaces)):
            if (self.surfaces.get(i+1)[0]["type"] == surf):
                self.surfaces.get(i+1)[0][param] = value

    def drag_buildup(self, M, h, W, Mcrit):
        a_sos = atmosprops.imperial_atmosphere(h).speed_of_sound()
        rho = atmosprops.imperial_atmosphere(h).density()
        print(f"a={a_sos}, rho={rho}")
        V = M*a_sos
        q = 0.5*rho*V*V
        CL = W/(q*self.Sref)
        CDi = CL*CL*self.k
        CDo = self.calculate_CDo(M, h)
        CDw = self.calculate_CDw(M, Mcrit)
        print(f"W={W}, V={V}, S={self.Sref}")
        return [CDo, CDw, CDi]
    


