import random
import pandas as pd
import math


def drums_movements(beat):
    movements = []
    rand_offset = random.uniform(-100,100)
    for i in range(0, beat):
        rand_value = (math.sin(2 * (i+rand_offset)) + math.sin(math.pi * (i+rand_offset))+1)/2
        movements.append(rand_value)
    
    mn = min(movements)
    mx = max(movements) - mn
    
    for i in range(len(movements)):
        movements[i] = (movements[i] - mn)/mx

    return(movements)

def drums_movements2(beat):
    rand_start = random.choice(range(-1000,1000))
    movements = [rand_start]
    for i in range(0, beat-1):
        prev_value = movements[i]
        next_value = prev_value + random.choice(range(-100,100))
        movements.append(next_value)
    
    mn = min(movements)
    mx = max(movements) - mn
    
    for i in range(len(movements)):
        movements[i] = (movements[i] - mn)/mx

    return(movements)

def snare_notes(beat, style, movements):

    snare = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration'])

    if style == 'trap':
    
        for i in range(0, beat):
            if i%4 == 2:
                snare.loc[len(snare)] = [int(60), i, i+0.25, 0.25]
        
            elif i%4 == 3:
                if 0.1 <= movements[i] < 0.2:
                    snare.loc[len(snare)] = [int(60), i+0.5, i+0.75, 0.25]

                if 0.2 <= movements[i] < 0.27:
                    snare.loc[len(snare)] = [int(60), i, i+0.25, 0.25]
                    snare.loc[len(snare)] = [int(60), i+0.5, i+0.75, 0.25]

                if 0.27 <= movements[i] < 0.3:
                    snare.loc[len(snare)] = [int(60), i, i+1/3, 1/3]
                    snare.loc[len(snare)] = [int(60), i+1/3, i+2/3, 1/3]
                    snare.loc[len(snare)] = [int(60), i+2/3, i+1, 1/3]
    
    if style == 'halftime':

        for i in range(0, beat):
            if i%4 == 1 or i%4 == 3:
                snare.loc[len(snare)] = [int(60), int(i), int(i+1), int(1)]          
    
    if style == 'drill':
    
        for i in range(0, beat):
            if i%4 == 2 and i%8 < 4:
                snare.loc[len(snare)] = [int(60), i, i+0.25, 0.25]
            elif i%4 == 3 and i%8 >= 4:
                snare.loc[len(snare)] = [int(60), i, i+0.25, 0.25]

    return snare

def kick_notes(beat, style, movements):

    kick = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration'])

    if style == 'trap':
        
        for i in range(0, beat):
            if (i/2)%4 == 0:
                kick.loc[len(kick)] = [int(60), int(i), int(i+1), int(1)]
            
            else:
                if 0.3 <= movements[i] < 0.4:
                    kick.loc[len(kick)] = [int(60), i+0.5, i+0.75, 0.25]

                if 0.4 <= movements[i] < 0.45:
                    kick.loc[len(kick)] = [int(60), i, i+0.25, 0.25]
                    kick.loc[len(kick)] = [int(60), i+0.5, i+0.75, 0.25]

                if 0.45 <= movements[i] < 0.50:
                    kick.loc[len(kick)] = [60, i, i+0.25, 0.25]
            
            #if 0.15 < movements[i] < 0.3:
            #    kick.loc[len(kick)] = [int(60), int(i), int(i+1), int(1)]

    if style == 'halftime':
        
        for i in range(0, beat):
            if (i/2)%4 == 0:
                kick.loc[len(kick)] = [int(60), int(i), int(i+1), int(1)] 
    
    if style == 'drill':
        
        for i in range(0, beat):
            if (i/2)%4 == 0:
                kick.loc[len(kick)] = [int(60), int(i), int(i+1), int(1)]

    return kick

def hihats_notes(beat, style, movements):

    hihats = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration', 'velocity'])

    if style == 'trap':
        
        rand_offset = random.uniform(-100,100)

        # Main hats
        if random.choice(range(10)) in range(9):
            for i in range(0, beat):
                hihats.loc[len(hihats)] = [60, i, i+0.25, 0.25, int(100)]
                hihats.loc[len(hihats)+1] = [60, i+0.5, i+0.75, 0.25, int(100)]

                if random.choice(range(5)) == 0: hihats.loc[len(hihats)+2] = [60, i+0.25, i+0.5, 0.25, int(100)]
                elif random.choice(range(5)) == 0: hihats.loc[len(hihats)+2] = [60, i+0.75, i+1, 0.25, int(100)]

                hihats = hihats.sort_index().reset_index(drop=True)
        else:
            for i in range(0, beat):
                hihats.loc[len(hihats)] = [60, i, i+0.25, 0.25, int(100)]

                if random.choice(range(5)) == 0: hihats.loc[len(hihats)+2] = [60, i+0.5, i+0.75, 0.25, int(100)]

                hihats = hihats.sort_index().reset_index(drop=True)
        

        # Hats rolls
        for i in range(0, beat):
            if random.choice(range(4)) == 0: 

                up_down = random.choice(['up','down'])
                base_note = random.choice(range(10,20))

                if up_down == 'up':
                    hihats.loc[len(hihats)+1] = [base_note, i, i+0.03125, 0.03125, int(100)]
                    hihats.loc[len(hihats)+2] = [base_note+1, i+(0.03125*2), i+(0.03125*3), 0.03125, int(100)]
                    hihats.loc[len(hihats)+3] = [base_note+2, i+(0.03125*3), i+(0.03125*4), 0.03125, int(100)]
                    hihats.loc[len(hihats)+4] = [base_note+3, i+(0.03125*4), i+(0.03125*5), 0.03125, int(100)]
                    hihats.loc[len(hihats)+5] = [base_note+4, i+(0.03125*5), i+(0.03125*6), 0.03125, int(100)]
                    hihats.loc[len(hihats)+6] = [base_note+5, i+(0.03125*5), i+(0.03125*6), 0.03125, int(100)]
                    hihats.loc[len(hihats)+7] = [base_note+6, i+(0.03125*5), i+(0.03125*5)+0.5, 0.5, int(100)]
                
                if up_down == 'down':
                    hihats.loc[len(hihats)+1] = [base_note, i, i+0.03125, 0.03125, int(100)]
                    hihats.loc[len(hihats)+2] = [base_note-1, i+(0.03125*2), i+(0.03125*3), 0.03125, int(100)]
                    hihats.loc[len(hihats)+3] = [base_note-2, i+(0.03125*3), i+(0.03125*4), 0.03125, int(100)]
                    hihats.loc[len(hihats)+4] = [base_note-3, i+(0.03125*4), i+(0.03125*5), 0.03125, int(100)]
                    hihats.loc[len(hihats)+5] = [base_note-4, i+(0.03125*5), i+(0.03125*6), 0.03125, int(100)]
                    hihats.loc[len(hihats)+6] = [base_note-5, i+(0.03125*5), i+(0.03125*6), 0.03125, int(100)]
                    hihats.loc[len(hihats)+7] = [base_note-6, i+(0.03125*5), i+(0.03125*5)+0.5, 0.5, int(100)]

            hihats = hihats.sort_index().reset_index(drop=True)
        
        # Patterns randomizer
        size = random.choice([4,4,8])
        time = random.choice([[0,size/4],[size/4,size/2],[size/2,3*size/4,],[3*size/4,size],[size/2,size]])
        if random.choice(range(5)) in range(3):
            for i in range(len(hihats)):
                if time[0] < math.floor(hihats.at[i, 'time'])%size <= time[1]:
                    hihats = hihats.drop([i])
            hihats = hihats.sort_index().reset_index(drop=True)

        # Velocity randomizer
        r = random.choice(range(10))
        for i in range(len(hihats)):
            if r == 0: hihats.at[i, 'velocity'] = 100 - (hihats.at[i, 'time']%2)*20
            if r == 1: hihats.at[i, 'velocity'] = 100 - (hihats.at[i, 'time']%4)*20
            #if r == 1: hihats.at[i, 'velocity'] = 100 - 5*hihats.at[i, 'time']%4
            if hihats.at[i, 'velocity'] <= 50: hihats.at[i, 'velocity'] = 0

    if style == 'halftime':
            
        #Main hats
        for i in range(0, beat):
            a = 0
            hihats.loc[len(hihats)] = [60, i, i+0.25, 0.25, int(100)]
            if random.choice(range(6)) == 0: 
                hihats.loc[len(hihats)+1] = [60, i+0.25, i+0.5, 0.25, int(100)]
                a += 1
            hihats.loc[len(hihats)+1+a] = [60, i+0.5, i+0.75, 0.25, int(100)]
            if random.choice(range(10)) == 0: 
                hihats.loc[len(hihats)+2+a] = [60, i+0.75, i+1, 0.25, int(100)]
                a += 1
            
            hihats = hihats.sort_index().reset_index(drop=True)

        #Hats rolls
        for i in range(0, beat):

            if random.choice(range(6)) == 0: 

                up_down = random.choice(['up','down'])
                base_note = random.choice(range(45,70))

                if up_down == 'up':
                    hihats.loc[len(hihats)+1] = [base_note, i, i+0.03125, 0.03125, int(100)]
                    hihats.loc[len(hihats)+2] = [base_note+1, i+(0.03125*2), i+(0.03125*3), 0.03125, int(100)]
                    hihats.loc[len(hihats)+3] = [base_note+2, i+(0.03125*3), i+(0.03125*4), 0.03125, int(100)]
                    hihats.loc[len(hihats)+4] = [base_note+3, i+(0.03125*4), i+(0.03125*5), 0.03125, int(100)]
                    hihats.loc[len(hihats)+5] = [base_note+4, i+(0.03125*5), i+(0.03125*6), 0.03125, int(100)]
                    hihats.loc[len(hihats)+6] = [base_note+5, i+(0.03125*5), i+(0.03125*6), 0.03125, int(100)]
                    hihats.loc[len(hihats)+7] = [base_note+6, i+(0.03125*5), i+(0.03125*5)+0.5, 0.5, int(100)]
                
                if up_down == 'down':
                    hihats.loc[len(hihats)+1] = [base_note, i, i+0.03125, 0.03125, int(100)]
                    hihats.loc[len(hihats)+2] = [base_note-1, i+(0.03125*2), i+(0.03125*3), 0.03125, int(100)]
                    hihats.loc[len(hihats)+3] = [base_note-2, i+(0.03125*3), i+(0.03125*4), 0.03125, int(100)]
                    hihats.loc[len(hihats)+4] = [base_note-3, i+(0.03125*4), i+(0.03125*5), 0.03125, int(100)]
                    hihats.loc[len(hihats)+5] = [base_note-4, i+(0.03125*5), i+(0.03125*6), 0.03125, int(100)]
                    hihats.loc[len(hihats)+6] = [base_note-5, i+(0.03125*5), i+(0.03125*6), 0.03125, int(100)]
                    hihats.loc[len(hihats)+7] = [base_note-6, i+(0.03125*5), i+(0.03125*5)+0.5, 0.5, int(100)]

            hihats = hihats.sort_index().reset_index(drop=True)

    # Velocity randomizer
        r = random.choice(range(10))
        for i in range(len(hihats)):
            if r == 0: hihats.at[i, 'velocity'] = 100 - (hihats.at[i, 'time']%2)*20
            if r == 1: hihats.at[i, 'velocity'] = 100 - (hihats.at[i, 'time']%4)*20
            #if r == 1: hihats.at[i, 'velocity'] = 100 - 5*hihats.at[i, 'time']%4
            if hihats.at[i, 'velocity'] <= 50: hihats.at[i, 'velocity'] = 0

    if style == 'drill':

        for i in range(0, int(beat/2)):
            hihats.loc[len(hihats)] = [60, i*2+0.75, i*2+1, 0.25]
            hihats.loc[len(hihats)] = [60, i*2+1.5, i*2+1.75, 0.25]

            
            hihats = hihats.sort_index().reset_index(drop=True)


    return hihats

def eightoeight_notes(beat, bass):

    eightoeight = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration'])
    eightoeight.loc[len(eightoeight)] = [0, 0, 0, 0]

    for i in range(random.choice(range(4,20))):
        eightoeight.loc[len(eightoeight)] = [0, random.choice(range(0, beat - 1)) + random.choice([0, 0, 0.5]), 0, 0]

        eightoeight = eightoeight.sort_index().reset_index(drop=True)
    
    eightoeight = eightoeight.sort_values(by='time')
    eightoeight['time_end'] = eightoeight['time'].shift(-1)
    eightoeight.time_end.iat[-1] = beat
    eightoeight['duration'] = eightoeight['time_end'] - eightoeight['time']

    for i in range(len(eightoeight)):
        for x in range(len(bass)):
            if bass.at[x, 'time'] <= eightoeight.at[i, 'time'] < bass.at[x, 'time_end']: eightoeight.at[i, 'notes'] = bass.at[x, 'notes']
        
        if eightoeight.at[i, 'notes'] > 75: eightoeight.at[i, 'notes'] = eightoeight.at[i, 'notes'] - 12
        if eightoeight.at[i, 'notes'] < 63: eightoeight.at[i, 'notes'] = eightoeight.at[i, 'notes'] + 12

        if eightoeight.at[i, 'notes']%12 >= 6:
            eightoeight.at[i, 'notes'] = 48 + eightoeight.at[i, 'notes']%12
        else:
            eightoeight.at[i, 'notes'] = 60 + eightoeight.at[i, 'notes']%12

        #eightoeight.at[i, 'notes'] = eightoeight.at[i, 'notes'] - 12
        if random.choice(range(4)) == 0: eightoeight.at[i, 'notes'] = eightoeight.at[i, 'notes'] + 24
        elif random.choice(range(8)) == 0: eightoeight.at[i, 'notes'] = eightoeight.at[i, 'notes'] + 36
    
    eightoeight = eightoeight.sort_index().reset_index(drop=True)

    return eightoeight