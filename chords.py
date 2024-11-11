import random
import pandas as pd

def chord_chooser(chord, scale):
    
    if scale in ['minor', 'major']:

        if chord == 0: #I
            return random.choice(range(1,6)) #Any chord except I
        
        if chord == 1: #ii
            return random.choice([4, 6]) #V or vii°
        
        if chord == 2: #iii
            return 5 #VI
        
        if chord == 3: #IV
            return random.choice([1, 4, 6]) #ii, IV or vii°
        
        if chord == 4: #V
            return random.choice([0, 5, 6]) #I, vi or vii°
        
        if chord == 5: #vi
            return random.choice([1, 3]) #ii or IV
        
        if chord == 6: #vii°
            if scale == "major":
                return random.choice([0, 4]) #I or V
            if scale == "minor":
                return random.choice([0, 3, 4, 5]) #I, IV, V or vi

    if scale == 'custom1':

        if chord == 0:
            return random.choice(range(1, 3))
        
        if chord == 1:
            return random.choice([2, 2, 3])

        if chord == 2:
            return random.choice([1, 3])
        
        if chord == 3:
            return random.choice([0, 0, 0, 1, 2])
    
def scale_pick(sca):
    
    if sca == 'G': return -5
    if sca == 'G#': return -4
    if sca == 'A': return -3
    if sca == 'A#': return -2
    if sca == 'B': return -1
    if sca == 'C': return 0
    if sca == 'C#': return 1
    if sca == 'D': return 2
    if sca == 'D#': return 3
    if sca == 'E': return 4
    if sca == 'F': return 5
    if sca == 'F#': return 6

def return_chords(scale):

    ch = [[],[],[],[],[],[],[]]
    chs = [[],[],[],[],[],[],[]]
    
    if scale == 'minor':
        ch[0] = [60, 63, 67] #C Minor
        ch[1] = [62, 65, 68] #D Diminished
        ch[2] = [63, 67, 70] #Eb Major
        ch[3] = [65, 68, 72] #F Minor
        ch[4] = [67, 70, 74] #G Minor
        ch[5] = [68, 72, 75] #Ab Major
        ch[6] = [70, 74, 77] #Bb Major

        ch[0] = [55, 60, 63, 67, 70] #C Minor
        ch[1] = [56, 62, 65, 68, 72] #D Diminished
        ch[2] = [55, 63, 67, 70, 75] #Eb Major
        ch[3] = [56, 65, 68, 72, 75] #F Minor
        ch[4] = [62, 67, 70, 74, 77] #G Minor
        ch[5] = [63, 68, 72, 75, 79] #Ab Major
        ch[6] = [62, 70, 74, 77, 80] #Bb Major

        r = random.choice(range(2))

        if r == 0:
            ch[0] = [48, 55, 60, 63] 
            ch[1] = [51, 55, 58, 63]
            ch[2] = [48, 53, 56, 60] 
            ch[3] = [55, 58, 62, 67] 
            ch[4] = [56, 60, 63, 68]
            ch[5] = [46, 58, 62, 65]
        
        if r == 1:
            ch[0] = [48, 60, 63, 67] 
            ch[1] = [51, 55, 58, 63]
            ch[2] = [48, 56, 60, 65] 
            ch[3] = [58, 62, 67, 70] 
            ch[4] = [56, 63, 68, 72]
            ch[5] = [46, 62, 65, 70]

    if scale == 'major':
        ch[0] = [55, 60, 64, 67] #C Major
        ch[1] = [57, 62, 65, 69] #D Minor
        ch[2] = [59, 64, 67, 71] #E Minor
        ch[3] = [60, 65, 69, 72] #F Major
        ch[4] = [59, 62, 67, 71] #G Major
        ch[5] = [60, 64, 69, 72] #A Minor
        ch[6] = [62, 65, 71, 74] #B Diminished

    if scale == 'custom1':
        ch[0] = [60, 63, 67, 72]
        ch[1] = [58, 62, 67, 70]
        ch[2] = [60, 63, 67, 72]
        ch[3] = [62, 67, 72, 74]
    
    return(ch)

def return_bass(scale):

    ch = [[],[],[],[],[],[],[]]    

    if scale == 'minor':
        ch[0] = [60, 65, 68]
        ch[1] = [63, 51, 58]
        ch[2] = [65, 68]
        ch[3] = [58, 67]
        ch[4] = [68, 63]
        ch[5] = [58, 65]

    if scale == 'major':
        ch[0] = [60, 64]
        ch[1] = [62, 65]
        ch[2] = [64, 67]
        ch[3] = [65, 69]
        ch[4] = [59, 62]
        ch[5] = [60, 64]
    
    if scale == 'custom1':
        ch[0] = [60]
        ch[1] = [62]
        ch[2] = [63]
        ch[3] = [67]
    
    return ch