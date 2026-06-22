import random
import numpy as np
import math
from collections import namedtuple

# namedtuple for the new varieties
VarietyData = namedtuple('VarietyData', ['hs_constant', 'quality'])

class Variety:
    def __init__(self):
        self.hs_constant, self.quality = self.set_hsc_qual()
        self.variety_id = self.set_id()
        
    def set_hsc_qual(self): #For the hs_constant and quality. Not really used by now
        hsc = np.zeros(3)
        for i in range(len(hsc)):
            while True:
                number = random.gauss(0.5, 0.15)
                if 0 <= number <= 1:
                    hsc[i] = number
                    break
        while True:
                number = random.gauss(0.5, 0.15)
                if 0 <= number <= 1:
                    quality = number
                    break
        return hsc, quality
        
    def set_id(self):
        id_variety = 0
        step = 0.1
        scale = int(math.pow(1 / step, 2)) #This is the original scale. I am not so sure of that
        current_scale = scale 

        # quality
        id_variety += math.floor(self.quality / (step / 2))

        # for hs_constant
        for i in self.hs_constant:
            temp = math.floor(i / step)  
            id_variety += current_scale * temp 
            current_scale *= scale  

        return id_variety

        
    def mutation(self):
        pass
    
    def newVariety(self, new_variety): # To copy the data of the new_variety. Not used by now
        self.hs_constant = new_variety.hs_constant
        self.quality = new_variety.quality
    
    def sexual_reproduction(variedad1, variedad2, change): #To reproduce 2 random varieties of a UD. This method can be used also. Not used by now.
        # to reproduce with one of the UD and one in the "forest" I have to think more on that.
        new_hsconstant = []
        new_quality = []
        for j in range(3):  # 3 values for each variety
            new_value = (variedad1.hs_constant[j] + variedad2.hs_constant[j]) / 2 + change * (2 * random.uniform(0, 1) - 1)
            while new_value < 0 or new_value > 1:
                new_value = (variedad1.hs_constant[j] + variedad2.hs_constant[j]) / 2 + change * (2 * random.uniform(0, 1) - 1)
            new_hsconstant.append(new_value)
        new_quality = (variedad1.quality + variedad2.quality) / 2 + change * random.uniform(0, 1)
        while new_quality < 0 or new_quality > 1:
            new_quality = (variedad1.quality + variedad2.quality) / 2 + change * random.uniform(0, 1)

        return VarietyData(hs_constant=np.array(new_hsconstant), quality=new_quality)  