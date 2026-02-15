import math
import numpy as np

class Geometry:

    def __init__(self, Cr, Ct, b, sweepLE):
        self.Cr = Cr
        self.Ct = Ct
        self.b = b
        self.LE = sweepLE

    def getArea(self):
        return 0.5*self.b*(self.Cr+self.Ct)
    
    def getAspectRatio(self):
        return (self.b**2)/self.getArea()

    def getLambda(self):
        return self.Ct/self.Cr
    
    def getMAC(self):
        return (((2/3)*self.Cr*((1 + self.getLambda() + (self.getLambda()**2))))/(1 + self.getLambda()))
    
    def getSweepChord(self, pchord):
        return np.rad2deg(np.arctan(np.tan(np.deg2rad(self.LE))-((4*(pchord-0)*(1-self.getLambda()))*(1/(self.getAspectRatio()*(1+self.getLambda()))))))
    