import random
import pandas as pd
import numpy as np

# Change tone of all notes
def fx_change_tone(notes, tone):

    notes['notes'] = notes['notes'] + tone
    return(notes)

# Calculate the average of tone, then move all notes to fit in [average - 6 ; average + 6]
def fx_average_tone(notes):

    av = notes['notes'].mean()
    for i in range(len(notes)):
        while notes.at[i, 'notes'] > av + 6 or notes.at[i, 'notes'] < av - 6:
            if notes.at[i, 'notes'] >= av + 6: notes.at[i, 'notes'] -= 12
            if notes.at[i, 'notes'] <= av - 6: notes.at[i, 'notes'] += 12
    
    return notes

# Randomly slice notes
def fx_random_slice(notes):

    skip_next = 0

    for i in range(len(notes)):
        if skip_next == 0:
            if random.choice(range(1,5)) == 1 and float(notes.at[i, 'duration']).is_integer() == True:
                notes.loc[i + 0.5] = notes.loc[i]
                notes = notes.sort_index().reset_index(drop=True)

                offset = random.choice(range(1,int(notes.at[i, 'duration']*2)))/2
                
                notes.at[i, 'time_end'] = notes.at[i, 'time_end'] - offset
                notes.at[i+1, 'time'] = notes.at[i, 'time_end']

                notes.at[i, 'duration'] = notes.at[i, 'time_end'] - notes.at[i, 'time']
                notes.at[i+1, 'duration'] = notes.at[i+1, 'time_end'] - notes.at[i+1, 'time']

                skip_next = 1 #Skip the chord that is being duplicated
                
        else: skip_next = 0
    
    return notes

# Randomly change the octave of notes
def fx_random_pitch(notes):

    next = 0

    for i in range(len(notes)):
        if next == 0:
            if random.choice(range(1,3)) == 1 and notes.at[i, 'notes'] <= 65:
                notes.at[i, 'notes'] += 12
                next = 1 #Skip the chord that is being duplicated

            if random.choice(range(1,3)) == 2 and notes.at[i, 'notes'] >= 70:
                notes.at[i, 'notes'] -= 12
                next = 1 #Skip the chord that is being duplicated

        else: next = 0
    
    return notes

# Delete random notes
def fx_random_delete(notes):
    remove_n = int(len(notes)/8)
    drop_indices = np.random.choice(notes.index, remove_n, replace=False)
    notes = notes.drop(drop_indices)

    notes = notes.sort_index().reset_index(drop=True)

    return notes

# Arpeggtiator (WARNING: to use only on raw chords, after block_to_chords())
def fx_arpeggiator(notes, beat):

    notes = notes.sort_values(['time', 'notes'], ascending=['True', 'True']).reset_index(drop=True)
    notes['next_time'] = notes['time'].shift(-1)

    for i in list(set(notes['time'])):
        
        n = 0
        for x in range(len(notes)):

            if notes.at[x, 'time'] == i and notes.at[x, 'time'] + n < notes.at[x, 'time_end'] and random.choice(range(1)) == 0:
                notes.at[x, 'time'] = notes.at[x, 'time'] + n
                notes.at[x, 'duration'] = notes.at[x, 'time_end'] - notes.at[x, 'time']
                n += beat/16
                
    return notes

# Create random melody
def fx_melody(chords):

    chop = random.choice([1/2,1,1,2,2,2,4,4])

    chords.sort_values(by='time', inplace=True)
    flag = 1
    while flag == 1:
        flag = 0
        for i in range(len(chords)):
            if chords.at[i, 'duration'] > chop:
                chords.loc[i + 0.5] = chords.loc[i]
                chords.at[i + 0.5, 'time'] = chords.at[i + 0.5, 'time'] + chop - chords.at[i, 'time']%chop
                chords.at[i, 'time_end'] = chords.at[i, 'time'] + chop - chords.at[i, 'time']%chop
                chords.at[i, 'duration'] = chords.at[i, 'time_end'] - chords.at[i, 'time']
                chords.at[i + 0.5, 'duration'] = chords.at[i + 0.5, 'time_end'] - chords.at[i + 0.5, 'time']

                chords = chords.sort_index().reset_index(drop=True)
                flag = 1
                break

    return chords

# Concatenate two arrays of notes
def fx_double(notes, beat):

    new_notes = notes.copy() 
    new_notes['time'] = new_notes['time'] + beat
    new_notes['time_end'] = new_notes['time_end'] + beat

    notes = notes.append(new_notes)

    return notes

# Multiply by 2 the length between each note
def fx_slow(notes):

    notes['time'] = notes['time']*2
    notes['time_end'] = notes['time_end']*2

    return notes

def fx_gross_beat(notes, track_effects):

    if len(track_effects) > 0:
        for x in track_effects:
            for i in range(len(notes)):
                skip = 0
                if x[0] <= notes.at[i, 'time'] < x[1] and notes.at[i, 'time']%8 >= 4:
                    notes = notes.drop(i)
                    skip = 1
                if skip == 0:
                    if x[0] <= notes.at[i, 'time'] < x[1] and notes.at[i, 'time']%8 < 4:
                        notes.at[i, 'notes'] = int(notes.at[i, 'notes'] - 12)
                        notes.at[i, 'time'] = int(notes.at[i, 'time'] + (notes.at[i, 'time']%8))
                        notes.at[i, 'time_end'] = int(notes.at[i, 'time_end']  + (notes.at[i, 'time_end']%8))
                        notes.at[i, 'duration'] = min(notes.at[i, 'time_end'] - notes.at[i, 'time'], notes.at[i, 'time'] + (8 - notes.at[i, 'time']%8))

            notes = notes.reset_index(drop=True)

    return(notes)

# Offset random chords position in a chord array (WARNING: to apply on chords array only, after block_chooser())
def blockfx_chord_mover(block, beat):

    for x in range(len(block)):

        r = random.choice(range(1,10))
        if r == 1 and x > 0:
            block.at[x, 'time'] = block.at[x, 'time'] - beat/32
            block.at[x, 'duration'] = block.at[x, 'duration'] + beat/32
            block.at[x-1, 'time_end'] = block.at[x-1, 'time_end'] - beat/32
            block.at[x-1, 'duration'] = block.at[x, 'duration'] - beat/32

        if r == 2 and x < len(block) - 1:
            block.at[x, 'time_end'] = block.at[x, 'time_end'] + beat/32
            block.at[x, 'duration'] = block.at[x, 'duration'] + beat/32
            block.at[x+1, 'time'] = block.at[x+1, 'time'] + beat/32
            block.at[x+1, 'duration'] = block.at[x+1, 'duration'] - beat/32

    return(block)

# Return an array of timeframes to apply effects to notes in track format
def trackfx_time_chooser(track):

    track_effects = []
    for i in track.columns:
        r = random.choice(range(2))
        if r == 0:
            if 'Intro' in i or 'Outro' in i or 'Chorus' in i: track_effects.append([track.at[13, i] - 8, track.at[13, i]])
        if r == 1:
            if 'Verse' in i or 'Bridge' in i or 'Outro' in i: track_effects.append([track.at[13, i] - 8, track.at[13, i]])
    return track_effects

# Cut random parts of drums at specific times
def elementsfx_drum_remover(elements_all, track):

    timeframes = []
    for i in track.columns:
        if 'Chorus' in i or 'Verse' in i:
            timeframes.append([track.at[13, i] - 8, track.at[13, i]])
    
    for i in elements_all:
        if i in ['kick', 'hihats', 'snare']:
            print('a')
            for a in range(len(elements_all[i]['time'])):
                for x in timeframes:
                    if x[0] <= elements_all[i].at[a, 'time'] <= x[1]:
                        print('dropped')
                        elements_all[i].drop(a)

        elements_all[i] = elements_all[i].sort_index().reset_index(drop=True)
    
    print(timeframes)
    return(elements_all)