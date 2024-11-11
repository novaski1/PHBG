import random
import pandas as pd
from chords import chord_chooser, return_chords, return_bass, scale_pick

def block_structure(scale, beat, number, mode):

    # Creating a chord progression 
    first_chord = 0
    last_chord = 0
    chordlist = []

    if number != 1:
        if mode == 'auto':
            
            if scale in ['major', 'minor']: r = range(5)
            if scale in ['custom1', 'custom2', 'custom3']: r = range(4)

            while(first_chord != chord_chooser(last_chord, scale)):
                
                chordlist = []

                for i in range(0,number-1):
                    if i == 0:
                        first_chord = random.choice(r)
                        chordlist.append(first_chord)
                        next_chord = first_chord
                    else:
                        next_chord = chord_chooser(next_chord, scale)
                        chordlist.append(next_chord)

                
                last_chord = chord_chooser(next_chord, scale)
                chordlist.append(last_chord)

        if mode == 'preset':

            if scale == 'minor' or scale == 'major':

                presets4 = [[0,1,2,5],
                            [0,1,5,3],
                            [0,2,1,4],
                            [0,2,3,2],
                            [0,2,3,3],
                            [0,2,4,3],
                            [0,2,5,0],
                            [0,3,2,5],
                            [0,4,1,5],
                            [0,4,2,1],
                            [0,4,2,3],
                            [0,4,5,3],
                            [0,4,5,5],
                            [0,5,0,3],
                            [0,5,4,1],
                            [0,5,4,5],
                            [2,0,3,4],
                            [2,1,5,0],
                            [2,3,4,5],
                            [2,4,5,0],
                            [3,0,2,5],
                            [3,2,0,0],
                            [3,4,1,0],
                            [3,4,3,0],
                            [4,0,3,1],
                            [4,0,3,3],
                            [4,2,0,3],
                            [4,5,1,0]
                ]

                presets3 = [[0,1,2],
                            [0,1,2],
                            [0,1,5],
                            [0,2,0],
                            [0,2,5],
                            [0,3,3],
                            [0,4,1],
                            [0,4,3],
                            [0,4,5],
                            [0,5,0]
                ]

                presets2 = [[0,2],
                            [0,4],
                            [0,5],
                            [2,0],
                            [3,0],
                            [3,4],
                            [4,0],
                            [5,0]
                ]
            
            if scale == 'custom1':

                presets4 = [[0,1,2,3]
                ]

                presets3 = [[0,1,2]
                ]

                presets2 = [[0,1]
                ]

            if number == 4:
                chordlist = random.choice(presets4)
            if number == 3:
                chordlist = random.choice(presets3)
            if number == 2:
                chordlist = random.choice(presets2)
    
    else:
        if scale in ['major', 'minor']: chordlist = [0]
        if scale in ['custom1', 'custom2', 'custom3']: chordlist = [random.choice(range(4))]


    # Selecting timeframe for each chord (depending on the number of bars)
    block = pd.DataFrame(columns=['chords', 'time'])

    if number == 4:

        i = 0

        for chord in chordlist:
            block.at[i, 'time'] = int(i*(beat/number))
            block.at[i, 'chords'] = chord
            i += 1
    
    if number == 3:

        presets = [[0, beat/4, (3*beat)/4],[0, beat/2, (3*beat)/4], [0, beat/4, beat/2], [0, beat/8, beat/2]]
        a = random.choice(presets)
        i = 0

        for chord in chordlist:
            block.at[i, 'time'] = int(a[i])
            block.at[i, 'chords'] = chord
            i += 1

    if number == 2:

        presets = [[0, beat/4], [0, beat/2], [0, (beat/4)*3], [0, beat/8], [0, (beat/8)*7]]
        a = random.choice(presets)
        i = 0

        for chord in chordlist:
            block.at[i, 'time'] = int(a[i])
            block.at[i, 'chords'] = chord
            i += 1
    
    if number == 1:
        block.at[0, 'time'] = 0
        block.at[0, 'time_end'] = int(beat)
        block.at[0, 'chords'] = chordlist[0]

    if number != 1:
        block['time_end'] = block['time'].shift(-1)
        block.time_end.iat[-1] = beat

    block['duration'] = block['time_end'] - block['time']

    return block

def block_to_chords(scale, block, root):

    ch = return_chords(scale)
    root = scale_pick(root)
    
    notes = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration'])

    for i in range(len(block)):
        for x in ch[block.at[i, 'chords']]:
            
            notes.loc[len(notes)] = [x+root-12, block.at[i, 'time'], block.at[i, 'time_end'], block.at[i, 'duration']]
    
    return notes

def block_to_bass(scale, block, root, beat):

    ch = return_chords(scale)
    root = scale_pick(root)

    notes = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration'])
    chords = block['chords'].tolist()
    bass = return_bass(scale)

    for i in range(len(block)):
        
        x = random.choice(range(int(block.at[i, 'time']), int(block.at[i, 'time_end']))) + 1

        if random.choice(range(4)) == 0 and block.at[i, 'chords'] in [0]:
            notes.loc[len(notes)] = [bass[chords[i]][0]+root-24, block.at[i, 'time'], x, x - block.at[i, 'time']]
            notes.loc[len(notes)] = [bass[chords[i]][1]+root-24, x, block.at[i, 'time_end'], block.at[i, 'time_end'] - x]
        else: notes.loc[len(notes)] = [bass[chords[i]][0]+root-24, block.at[i, 'time'], block.at[i, 'time_end'], block.at[i, 'time_end'] - block.at[i, 'time']]

    # Random cut
    #if random.choice(range(1)) == 0:
    #    
    #    rand_loop = random.choice([1/2, 1, 2, 2, 4, 4, 8])
    #    x = random.choice(range(1, rand_loop+1))
    #    y = random.choice(range(1, rand_loop+1))
    #    mnmx = [min([x,y]),max([x,y])]
    #    for i in range(len(notes)):
    #        if mnmx[0] <= notes.at[i, 'time_end']%rand_loop < mnmx[1]:
    #            notes.at[i, 'time_end'] = mnmx[0]
    #        elif mnmx[0] <= notes.at[i, 'time']%rand_loop < mnmx[1]:
    #            notes.at[i, 'time'] = mnmx[1]
    #            #notes.loc[len(notes)] = [notes.at[i, 'notes'], mnmx[1], notes.at[i, 'time_end'], mnmx[1] - block.at[i, 'time_end']]
    #    
    #    notes = notes.sort_index().reset_index(drop=True)

    # Normalizing bass note
    for i in range(len(notes)):
        notes.at[i, 'notes'] = 36 + notes.at[i, 'notes']%12
    return notes

def block_to_lead(scale, beat, block, root):

    root = scale_pick(root)

    notes = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration'])
    chords_list = block['chords'].tolist()
    chords = return_chords(scale)

    min_duration = block['duration'].min()
    #num_notes_lead = int(random.choice(range(1, int(min_duration))))
    num_notes_lead = 0

    time_notes = [0]
    for i in range(num_notes_lead):
        x = random.choice([0.5, 1, 1, 1, 2, 2])
        time_notes.append(time_notes[len(time_notes)] + x)
    
    time_notes.append(min_duration)

    for i in range(len(block)):

        for j in range(len(time_notes)-1):
            #notes.loc[len(notes)] = [random.choice(chords[chords_list[i]])+root, block.at[i, 'time'] + time_notes[j], block.at[i, 'time'] + time_notes[j+1], time_notes[j+1] - time_notes[j]]
            #notes.loc[len(notes)] = [random.choice(chords[chords_list[i]])+root, block.at[i, 'time'], block.at[i, 'time_end'], block.at[i, 'duration']]
            pass
        pass
        
    notes.loc[len(notes)] = [60+root, 0, beat, beat]
    
    return notes

def block_to_pluck(scale, beat, block, root):

    root = scale_pick(root)

    notes = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration'])
    chords_list = block['chords'].tolist()
    chords = return_chords(scale)

    min_duration = block['duration'].min()
    #num_notes_lead = int(random.choice(range(1, int(min_duration))))
    num_notes_lead = 0

    if min_duration >= 2:
        for i in range(len(block)):
            notes.loc[len(notes)] = [chords[chords_list[i]][0]+root+12, block.at[i, 'time'], block.at[i, 'time'] + 0.5, 0.5]
            notes.loc[len(notes)] = [chords[chords_list[i]][1]+root+12, block.at[i, 'time'] + 0.5, block.at[i, 'time'] + 1, 0.5]
            notes.loc[len(notes)] = [chords[chords_list[i]][2]+root+12, block.at[i, 'time'] + 1, block.at[i, 'time_end'], block.at[i, 'time_end'] - block.at[i, 'time'] - 1]
    
    return notes