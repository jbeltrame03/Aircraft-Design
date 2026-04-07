import aircraft, analyses, HLS_geom

'''

Calculates and returns the X ordinate of the center of gravity of the aircraft

'''

class CG:

    def __init__(self):

        self.XCG = 0
        self.MTOW = 0
        self.moment = 0


    def add_elem(self, W, X):
        
        self.MTOW += W
        self.moment = W*X
        self.XCG = (self.moment/(self.MTOW))
    

    def calc_XCG(self):
        self.XCG = (self.moment/(self.MTOW))

    def get_XCG(self):

        return self.XCG
    

concept_CG = CG()
