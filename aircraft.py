import struct_weight, parasite_drag, atmosprops #type: ignore


class aircraft:

    

    def __init__(self, Nz, Wo):
        self.MTOW = 0
        self.W_fuel = 0
        self.W_structure = 0
        self.W_payload = 0
        self.CDo = 0
        self.geom = {}
        self.W_structure = struct_weight.weights(Wo, Nz)
        self.lift_drag = parasite_drag.lift_drag()
        pass


    def set_fuel_weight(self, W_f):
        self.W_fuel = W_f

    def set_structure_weight(self, W_s):
        self.W_structure = W_s

    def add_structure(self, W_elem):
        self.W_structure.add_misc(W_elem)

    def set_payload(self, W_p):
        self.W_payload = W_p

    def set_weights(self, W_p, W_f):
        self.W_fuel = W_f
        self.W_payload = W_p
        self.MTOW = self.W_structure.get_Struct_Weight() + W_f + W_p
        print(self.MTOW)

    def update_MTOW(self):
        self.MTOW = self.W_fuel + self.W_structure.get_Struct_Weight() + self.W_payload

    def get_MTOW(self):
        return self.MTOW
    
    def wing_geometry(self, Cr, Ct, LE, b, Sw, AR, t_c, Swet, xc_max, num_elem):
        Swet = 2*Sw*(1+(0.25*t_c))

        surface = {
             "type" :"WING", 
             "Root": Cr, 
             "Tip": Ct, 
             "Wet Area": Swet, 
             "t/c": t_c, 
             "x/c": xc_max, 
             "b": b, 
             "LE": LE,
             "Area": Sw,
             "AR": AR
             }
        
        self.geom.setdefault(num_elem, []).append(surface)
        self.lift_drag.set_Oswalds(LE, AR)
        self.W_structure.add_wing(Cr, Ct, t_c, LE, b, 0.3*(Cr+Ct)*0.5, 0.4*b)
        self.lift_drag.set_Sref(Sw)
        self.lift_drag.set_Wing_Geometry(Cr, Ct, Swet, t_c, xc_max, LE, b, num_elem)
    
    def vertical_stab_geometry(self, Cr, Ct, LE, b, t_c, Swet, xc_max, num_elem, Lv, T_tail):
        Sw = 0.5*(Cr+Ct)*b
        Swet = 2*Sw*(1+(0.25*t_c))
        surface = {
             "type" :"VERTICAL", 
             "Root": Cr, 
             "Tip": Ct, 
             "Wet Area": Swet, 
             "t/c": t_c, 
             "x/c": xc_max, 
             "b": b, 
             "LE": LE,
             }
        self.geom.setdefault(num_elem, []).append(surface)
        self.W_structure.add_VT(T_tail, Lv, Cr, Ct, b, LE, t_c)
        self.lift_drag.set_Wing_Geometry(Cr, Ct, Swet, t_c, xc_max, LE, b, num_elem)

    def fuselage_geometry(self, Lf, Df, Swet, num_elem, Crw, Ctw, bw, LEw):

        surface = {
             "type" :"FUSELAGE", 
             "Length": Lf, 
             "Diameter": Df, 
             "Wet Area": Swet, 
             }
        self.geom.setdefault(num_elem, []).append(surface)

        self.W_structure.add_fuselage(1, 1, Lf, Swet, Crw, Ctw, bw, LEw, Df)
        self.lift_drag.set_fuselage_Geometry(Lf, Df, Swet, num_elem)

    def set_engine(self, SFC, Number_Engines, Weight_engine, Thrust_engine):
        self.SFC = SFC
        self.W_structure.add_misc(Number_Engines*Weight_engine)
        self.T_SeaLevel = Number_Engines*Thrust_engine

    def get_TSL(self):

        return self.T_SeaLevel
    
    def get_altitude(self):
        return self.h_cruise
    

    def set_flight_param(self, M, h, Mcrit):
        self.M_cruise = M
        self.h_cruise = h
        self.M_critical = Mcrit

    def get_Wing_Param(self, surf, param):

        for i in range(len(self.geom)):
            if (self.geom.get(i+1)[0]["type"] == surf):
                return (self.geom.get(i+1)[0][param])
        return 0


    def set_Param(self, surf, param, new_val):
        for i in range(len(self.geom)):
            if (self.geom.get(i+1)[0]["type"] == surf):
                self.geom.get(i+1)[0][param] = new_val
                self.lift_drag.update_Param(surf, param, new_val)
        return 0

    def calculate_CDo(self):
        self.CDo = self.lift_drag.calculate_CDo(self.M_cruise, self.h_cruise)    
        return self.CDo

    def update_geometry(self):
        self.lift_drag

    def get_Dyn_Pressure(self):
        return 0.5*((atmosprops.imperial_atmosphere(self.h_cruise).speed_of_sound()*self.M_cruise)**2)*atmosprops.imperial_atmosphere(self.h_cruise).density()
    

    def calculate_CL_CD(self):

        return self.lift_drag.calculate_CL_CD(self.M_cruise, self.h_cruise, self.MTOW, self.M_critical)
    

    def get_Drag_Buildup(self):

        return self.lift_drag.drag_buildup(self.M_cruise, self.h_cruise, self.MTOW, self.M_critical)
    




