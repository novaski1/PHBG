import random
import os

def return_sf2(elements):
    
    l = []
    for i in elements:
        l.append(random.choice(os.listdir(str(os.path.dirname(os.path.abspath(__file__)) + '/sf2/' + i))))

    return(l)