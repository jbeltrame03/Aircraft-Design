import aircraft, atmosprops, thrust_model #type: ignore
import numpy as np
import matplotlib.pyplot as plt

class study:

    

    def __init__(self,ac):
        #configuration is aircraft type
        self.configuration = ac
        pass

    def reset_param(self, init, surf, param):
        self.configuration.set_Param(surf, param, init)

    def Sweep_CDo(self, Sweep_bounds):
        init = self.configuration.get_Wing_Param("WING", "LE")
        X = np.linspace(Sweep_bounds[0], Sweep_bounds[1], num=100)
        Y = []
        for i in X:
            self.configuration.set_Param("WING", "LE", i)
            print(self.configuration.get_Wing_Param("WING", "LE"))
            Y.append(self.configuration.calculate_CDo())

        self.reset_param(init, "WING", "LE")
        plt.figure()
        plt.plot(X,Y, linewidth=3)
        plt.grid(visible=True, which='both')
        plt.xlabel('Leading Edge Sweep (degree)')
        plt.ylabel('Parasite Drag (CDo)')
        plt.show()

    def thrust_required(self, M_bounds, h):
        

        [M0, h0, Mcrit0] = self.configuration.get_flight_param()


        M_range = np.linspace(M_bounds[0], M_bounds[1], num=100)

        D = []
        T2 = []
        Mcrit = 0.85

        for i in range(len(M_range)):
            self.configuration.set_flight_param(M_range[i], h, Mcrit)
            [CL, CD] = self.configuration.calculate_CL_CD()
            q = self.configuration.get_Dyn_Pressure()
            D.append(q*CD*self.configuration.get_Wing_Param("WING", "Area"))

            T2.append(thrust_model.Model(self.configuration.get_TSL()).thrust_altitude_Low_BPR_norm(M_range[i],self.configuration.get_altitude()))

        self.configuration.set_flight_param(M0,h0, Mcrit0)
        plt.figure()
        plt.rcParams['savefig.dpi'] = 1200   # super high quality when saving
        plt.plot(M_range, D, linewidth=3)
        plt.plot(M_range, T2, linewidth=3)
        plt.xlabel("Mach")
        plt.ylabel("Thrust Required & Thrust Available (lb)")
        plt.grid(visible=True, which="both")
        plt.title("Thrust Required & Thrust Available Verus Mach Number")
        plt.legend(["Thrust Required", "Thrust Available"])
        plt.show()   


    def range_integration(self, dW):
        [M0, h0, Mcrit0] = self.configuration.get_flight_param()

        R = 0
        Wi = self.configuration.get_MTOW()
        Wf = Wi - self.configuration.get_fuel_weight()
        print(f"Wi = {Wi}, Wf = {Wf}")
    
        W = Wi
        W_fuel = self.configuration.get_fuel_weight()
        [M, h, Mcrit] = self.configuration.get_flight_param()
        V = (atmosprops.imperial_atmosphere(h).speed_of_sound()*M)
        
        R_p = []
        W_plot = []
        Sw = self.configuration.get_Wing_Param("WING", "Area")
        
        while W > Wf:
            
            q = self.configuration.get_Dyn_Pressure()
            [CDo, CDw, CDi] = self.configuration.get_Drag_Buildup()
            CD = CDi + CDo + CDw
            D = q*CD*Sw
            T = D
            W_dot = (self.configuration.get_SFC()/3600)*T
            R += ((V/W_dot)*abs(dW))
            #print(f"R={R}, V={V} T={T}")
            W += dW
            R_p.append(R/5280/1.151)
            W_plot.append(W)
            W_fuel += dW
            self.configuration.set_fuel_weight(W_fuel)
            self.configuration.update_MTOW()
            #print(W_fuel)

        self.configuration.set_flight_param(M0,h0, Mcrit0)

        self.configuration.set_fuel_weight(Wi-Wf)
        self.configuration.update_MTOW()
        print(self.configuration.get_MTOW())
        
        print(f"Range by Integration = {np.ceil(R/5280/1.151)} nmi")
        plt.figure()
        plt.plot(W_plot, R_p, linewidth=3)
        plt.ylabel("Range (nmi)")
        plt.xlabel("Gross Weight")
        plt.title("Range Integration")
        plt.grid(visible=True, which="both")
        plt.show()

    def fuel_sensitivity(self, w_f_bounds):
 
        W_fuel = np.linspace(w_f_bounds[0], w_f_bounds[1], num=200)
        R_p = []
        Wempty = self.configuration.get_structure_weight()
        Wp = self.configuration.get_payload_weight()
        for i in W_fuel:
            
            WTO = Wempty + Wp + i
            
            [CL,CD] = self.configuration.calculate_CL_CD()
            [M, h, Mcrit] = self.configuration.get_flight_param()
            V = (atmosprops.imperial_atmosphere(h).speed_of_sound()*M)
 
            R = ((V/1.688)*CL)/(CD*self.configuration.get_SFC())*np.log(WTO/(Wempty+Wp))
            R_p.append(R)

        plt.rcParams['savefig.dpi'] = 1200   # super high quality when saving
        plt.figure()
        plt.plot(W_fuel, R_p, linewidth=3)
        plt.ylabel("Range (nmi)")
        plt.xlabel("Fuel Load (lb)")
        plt.title("Fuel Load Sensitivity Study")
        plt.grid(visible=True, which="both")
        plt.ticklabel_format(style='plain', axis='x')
        plt.ticklabel_format(useOffset=False, style='plain', axis='x')

 
        plt.show()


    def drag_buildup(self, M_bounds, h):


        M_range = np.linspace(M_bounds[0], M_bounds[1], num=100)

        CD_t = []
        CDo_p = []
        CDi_p = []
        CDw_p = []
        Mcrit = 0.85

        for i in range(len(M_range)):
            self.configuration.set_flight_param(M_range[i], h, Mcrit)
            [CDo, CDw, CDi] = self.configuration.get_Drag_Buildup()
            CD_t.append(CDo+CDw+CDi)
            CDo_p.append(CDo)
            CDi_p.append(CDi)
            CDw_p.append(CDw)
   

        plt.figure()
        print(f"Minimum: CDo={min(CDo_p)} CD={min(CD_t)} CDi={min(CDi_p)}")
        plt.rcParams['savefig.dpi'] = 1200   # super high quality when saving
        plt.plot(M_range, CD_t, linewidth=3)
        plt.plot(M_range, CDi_p, linewidth=3)
        plt.plot(M_range, CDw_p, linewidth=3)
        plt.plot(M_range, CDo_p, linewidth=3)
        plt.xlabel("Mach")
        plt.ylabel("Drag Coefficient")
        plt.grid(visible=True, which="both")
        plt.title("Drag Coefficient Build Up")
        plt.legend(["CD", "CDi", "CDw", "CDo"])
        plt.show()  


    def thrust_model(self, model, upper_alt):


        alt = np.linspace(0, upper_alt, num=100)
        T = []
        for i in alt:
            T.append(thrust_model.Model(self.configuration.get_TSL()).thrust_altitude_Low_BPR_norm(M_range[i],self.configuration.get_altitude()))



    