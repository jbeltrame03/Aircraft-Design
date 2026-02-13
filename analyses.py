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


        