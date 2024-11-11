import random
import pandas as pd

def return_track_elements(element):

    if element == 1: #Intro
        return random.choice([2,2,2,2,3])
        
    if element == 2: #Verse
        return random.choice([3,3,3,3,3,4,5])
    
    if element == 3: #Chorus
        return random.choice([2,2,4])
        
    if element == 4: #Bridge
        return random.choice([2,3,5])
    
    if element == 5: #Outro
        return(6)

def track_chooser(beat, bpm, length):

    if length == 'short': l = range(50,100)
    if length == 'medium': l = range(100,200)
    if length == 'long': l = range(200,300)

    track, length_elements = track_structure(beat)
    track_length = int((60/bpm)*length_elements[-1])

    while track_length not in l:

        track, length_elements = track_structure(beat)
        track_length = int((60/bpm)*length_elements[-1])
        #track_length = random.choice(range(50,100))
    
    return track, length_elements

def track_structure(beat):
    
    #Track Elements:
    #Intro 1
    #Verse 2
    #Chorus 3
    #Bridge 4
    #Outro 5
    #End 6

    track_elements = [1]
    element = return_track_elements(1)

    while element != 6:

        track_elements.append(element)
        element = return_track_elements(element)
        if len(track_elements) > 12: 
            track_elements = [1]
            element = return_track_elements(1)
    
    col = []
    n_verse = 1
    n_chorus = 1
    n_bridge = 1

    for i in range(len(track_elements)):
        if track_elements[i] == 1: col.append('Intro')
        if track_elements[i] == 2: 
            col.append(str('Verse' + str(n_verse)))
            n_verse += 1
        if track_elements[i] == 3:
            col.append(str('Chorus' + str(n_chorus)))
            n_chorus += 1
        if track_elements[i] == 4:
            col.append(str('Bridge' + str(n_bridge)))
            n_bridge += 1
        if track_elements[i] == 5: col.append('Outro')
    
    #Index:
    #1 Lead
    #2 Chords1
    #3 Chords2
    #4 Pad
    #5 Pluck
    #6 Other
    #7 808
    #8 Bass
    #9 Kick
    #10 Snare
    #11 Hats
    #12 Percs
    #13 Sfx
    #14 TIMEFRAME TRACK ELEMENTS
    track = pd.DataFrame(columns=col, index=range(1,16))
    track = track.fillna(0)
    track['Index'] = ['Lead', 'Chords1', 'Chords2', 'Pad', 'Pluck', 'Other', '808', 'Bass', 'Kick', 'Snare', 'Hats', 'Percs', 'Sfx', 'time_start', 'time_end']

    length_elements = []
    l = 0
    next_l = 0

    # 1: Intro, Outro
    # 2: Verse
    # 3: Chorus
    # 4: Bridge
    choice_instruments = {
        'lead':     [random.choice([0,1]) for i in range(4)],
        'chords1':  [random.choice([0,1]) for i in range(4)],
        'chords2':  [],
        'pad':      [random.choice([0,1]) for i in range(4)],
        'pluck':    [random.choice([0,1]) for i in range(4)],
        '808':      [random.choice([0,1]) for i in range(4)],
        'bass':     [],
        'kick':     [random.choice([0,1,1,1,1]) for i in range(4)],
        'snare':    [random.choice([0,1,1,1,1]) for i in range(4)],
        'hats':     [random.choice([0,1,1,1,1]) for i in range(4)],
        'percs':    [random.choice([0,1,1,1,1]) for i in range(4)],
    }
    for i in range(len(choice_instruments['chords1'])):
        choice_instruments['chords2'].append(1 - choice_instruments['chords1'][i])
        choice_instruments['bass'].append(1 - choice_instruments['808'][i])
    
    # Removing 808 & bass from intro and outro
    if random.choice(range(5)) in range(4):
        choice_instruments['808'][0] = 0
        choice_instruments['bass'][0] = 0
        choice_instruments['kick'][0] = 0
        choice_instruments['snare'][0] = 0
        choice_instruments['hats'][0] = 0
        choice_instruments['percs'][0] = 0

    for i in track.columns:
        if i in ['Intro', 'Outro'] or 'Verse' in i or 'Chorus' in i or 'Bridge' in i:
            pass

        if i == 'Intro':
            track.at[1, i] = choice_instruments['lead'][0]
            track.at[2, i] = choice_instruments['chords1'][0]
            track.at[3, i] = choice_instruments['chords2'][0]
            track.at[4, i] = choice_instruments['pad'][0]
            track.at[5, i] = choice_instruments['pluck'][0]
            track.at[7, i] = choice_instruments['808'][0]
            track.at[8, i] = choice_instruments['bass'][0]
            track.at[9, i] = choice_instruments['kick'][0]
            track.at[10, i] = choice_instruments['snare'][0]
            track.at[11, i] = choice_instruments['hats'][0]
            track.at[12, i] = choice_instruments['percs'][0]
            track.at[13, i] = 1
            if beat == 8: next_l = random.choice([2,2,4])*beat + next_l
            if beat == 16: next_l = random.choice([1,1,2])*beat + next_l
            if beat == 32: next_l = random.choice([1,1,2])*beat + next_l

        if 'Verse' in i:
            track.at[1, i] = choice_instruments['lead'][1]
            track.at[2, i] = choice_instruments['chords1'][1]
            track.at[3, i] = choice_instruments['chords2'][1]
            track.at[4, i] = choice_instruments['pad'][1]
            track.at[5, i] = choice_instruments['pluck'][1]
            track.at[7, i] = choice_instruments['808'][1]
            track.at[8, i] = choice_instruments['bass'][1]
            track.at[10, i] = choice_instruments['snare'][1]
            track.at[11, i] = choice_instruments['hats'][1]
            track.at[12, i] = choice_instruments['percs'][1]
            track.at[13, i] = 1
            if beat == 8: next_l = random.choice([2,4,4,4,4,4])*beat + next_l
            if beat == 16: next_l = random.choice([1,2,2,2,2,2])*beat + next_l
            if beat == 32: next_l = random.choice([1,1,1,2,2])*beat + next_l

        if 'Chorus' in i:
            track.at[1, i] = choice_instruments['lead'][2]
            track.at[2, i] = choice_instruments['chords1'][2]
            track.at[3, i] = choice_instruments['chords2'][2]
            track.at[4, i] = choice_instruments['pad'][2]
            track.at[5, i] = choice_instruments['pluck'][2]
            track.at[7, i] = choice_instruments['808'][2]
            track.at[8, i] = choice_instruments['bass'][2]
            track.at[10, i] = choice_instruments['snare'][2]
            track.at[11, i] = choice_instruments['hats'][2]
            track.at[12, i] = choice_instruments['percs'][2]
            track.at[13, i] = 1
            if beat == 8: next_l = random.choice([4,4,8,8])*beat + next_l
            if beat == 16: next_l = random.choice([2,2,4,4])*beat + next_l
            if beat == 32: next_l = random.choice([2,2,4])*beat + next_l
                
        if 'Bridge' in i:
            track.at[1, i] = choice_instruments['lead'][3]
            track.at[2, i] = choice_instruments['chords1'][3]
            track.at[3, i] = choice_instruments['chords2'][3]
            track.at[4, i] = choice_instruments['pad'][3]
            track.at[5, i] = choice_instruments['pluck'][3]
            track.at[7, i] = choice_instruments['808'][3]
            track.at[8, i] = choice_instruments['bass'][3]
            track.at[10, i] = choice_instruments['snare'][3]
            track.at[11, i] = choice_instruments['hats'][3]
            track.at[12, i] = choice_instruments['percs'][3]
            track.at[13, i] = 1
            if beat == 8: next_l = random.choice([4,4,8,8])*beat + next_l
            if beat == 16: next_l = random.choice([2,2,4,4])*beat + next_l
            if beat == 32: next_l = random.choice([2,2,2,4])*beat + next_l
        
        if i == 'Outro':
            track.at[1, i] = choice_instruments['lead'][0]
            track.at[2, i] = choice_instruments['chords1'][0]
            track.at[3, i] = choice_instruments['chords2'][0]
            track.at[4, i] = choice_instruments['pad'][0]
            track.at[5, i] = choice_instruments['pluck'][0]
            track.at[7, i] = choice_instruments['808'][0]
            track.at[8, i] = choice_instruments['bass'][0]
            track.at[10, i] = choice_instruments['snare'][0]
            track.at[11, i] = choice_instruments['hats'][0]
            track.at[12, i] = choice_instruments['percs'][0]
            track.at[13, i] = 1
            if beat == 8: next_l = random.choice([2,4,4,4,4,8])*beat + next_l
            if beat == 16: next_l = random.choice([1,2,2,2,2,4])*beat + next_l
            if beat == 32: next_l = random.choice([1,1,1,2])*beat + next_l

        if i != "Index":
            track.at[14, i] = l
            track.at[15, i] = next_l
            l = next_l
            length_elements.append(l)

    return track, length_elements

def track_to_notes(notes, track, instrument, beat):

    if instrument == 'Lead': instrument = 1
    if instrument == 'Chords1': instrument = 2
    if instrument == 'Chords2': instrument = 3
    if instrument == 'Pad': instrument = 4
    if instrument == 'Pluck': instrument = 5
    if instrument == 'Other': instrument = 6
    if instrument == '808': instrument = 7
    if instrument == 'Bass': instrument = 8
    if instrument == 'Kick': instrument = 9
    if instrument == 'Snare': instrument = 10
    if instrument == 'Hats': instrument = 11
    if instrument == 'Percs': instrument = 12
    if instrument == 'Sfx': instrument = 13

    notes_all = pd.DataFrame(columns = ['notes', 'time', 'time_end', 'duration'])

    a = 0
    x = 0
    for i in track.columns:

        if track.at[instrument, i] == 1 and i != 'Index':
            for x in range(int((track.at[15, i]-track.at[14, i])/beat)):
                if 'Bridge' in i or i in ['Intro', 'Outro']: r = 0
                elif random.choice(range(2)) == 1 and 'Chorus' in i: r = 0
                else: r = 1
                new_notes = notes[r].copy()
                new_notes['time'] = new_notes['time'] + beat*x + track.at[14, i]
                new_notes['time_end'] = new_notes['time_end'] + beat*x + track.at[14, i]

                notes_all = notes_all.append(new_notes)
                notes_all = notes_all.reset_index(drop=True)

    if instrument == 11: notes_all.loc[len(notes_all)] = [200, track.at[15, 'Outro'], track.at[15, 'Outro']+1, 1, int(100)]
    else: notes_all.loc[len(notes_all)] = [200, track.at[15, 'Outro'], track.at[15, 'Outro']+1, 1]

    return notes_all

def track_random_events(elements_all, track):
    
    # Random events:
    # DRUMS
    # d1: Drums cutting at the last measure of Verse OR Chorus (Normal)
    # d2: Hihats cutting during first 4 measures of Verse2+ OR Chorus2+ (Normal)
    # d3: Drums (only 2) cutting during first half of Verse2+ OR Chorus2+ (Rare)
    # d4: Drums cutting during last half of Verse2+ OR Chorus2+ (Rare)
    # d5: Drums cutting during Bridge (Rare)
    # d6: Drums cutting during Intro AND Outro (Rare)
    # d7: Drums tone -12 during Outro (Very rare)
    # d8: Only hihats during Chorus (Very rare)

    # MELODY
    # m1: Pad tone - 12 during Chorus or Verse (Rare)
    # m2: Lead tone - 12 during Chorus or Verse (Rare)

    # Rarity of events:
    normal = range(4)
    rare = range(8)
    very_rare = range(12)

    list_events_rarity = [['d1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8', 'm1', 'm2'],
                            ['n', 'n', 'r', 'r', 'r', 'r', 'vr', 'vr', 'r', 'r']]
    random_events = []

    for i in range(len(list_events_rarity[0])):
        if list_events_rarity[1][i] == 'n' and random.choice(normal) == 0: random_events.append(list_events_rarity[0][i])
        if list_events_rarity[1][i] == 'r' and random.choice(rare) == 0: random_events.append(list_events_rarity[0][i])
        if list_events_rarity[1][i] == 'vr' and random.choice(very_rare) == 0: random_events.append(list_events_rarity[0][i])

    for x in elements_all:
        for i in track.columns:

            start = track.at[14, i]
            end = track.at[15, i]
        
            # d1
            if 'd1' in random_events:
                if 'Verse' in i or 'Chorus' in i:
                    if x in ['kick', 'snare', 'hihats']:
                        for y in range(len(elements_all[x])):
                            if end - 4 <= elements_all[x].at[y, 'time'] < end:
                                elements_all[x] = elements_all[x].drop(y)

                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)
            
            # d2
            if 'd2' in random_events:
                if ('Verse' in i or 'Chorus' in i) and i != 'Verse1' and i != 'Chorus1':
                    if x == 'hihats':
                        for y in range(len(elements_all[x])):
                            if start <= elements_all[x].at[y, 'time'] < start + 16:
                                elements_all[x] = elements_all[x].drop(y)

                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)

            # d3
            if 'd3' in random_events:
                if ('Verse' in i or 'Chorus' in i) and i != 'Verse1' and i != 'Chorus1':
                    drum_choice = [random.choice(range(2)) for u in range(3)]
                    if (x == 'kick' and drum_choice[0] == 1) or (x == 'snare' and drum_choice[1] == 1) or (x == 'hihats' and drum_choice[2] == 1):
                        for y in range(len(elements_all[x])):
                            if start <= elements_all[x].at[y, 'time'] < start + (end-start)/2:
                                elements_all[x] = elements_all[x].drop(y)

                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)
            
            # d4
            if 'd4' in random_events:
                if ('Verse' in i or 'Chorus' in i) and i != 'Verse1' and i != 'Chorus1':
                    if x in ['kick', 'snare', 'hihats']:
                        for y in range(len(elements_all[x])):
                            if start + (end-start)/2 <= elements_all[x].at[y, 'time'] < end:
                                elements_all[x] = elements_all[x].drop(y)

                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)
            
            # d5
            if 'd5' in random_events:
                if 'Bridge' in i:
                    if x in ['kick', 'snare', 'hihats']:
                        for y in range(len(elements_all[x])):
                            if start <= elements_all[x].at[y, 'time'] < end:
                                elements_all[x] = elements_all[x].drop(y)

                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)
            
            # d6
            if 'd6' in random_events:
                if i in ['Intro', 'Outro']:
                    if x in ['kick', 'snare', 'hihats']:
                        for y in range(len(elements_all[x])):
                            if start <= elements_all[x].at[y, 'time'] < end:
                                elements_all[x] = elements_all[x].drop(y)

                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)
            
            # d7
            if 'd7' in random_events:
                if i == 'Outro':
                    if x in ['kick', 'snare', 'hihats']:
                        for y in range(len(elements_all[x])):
                            if start <= elements_all[x].at[y, 'time'] < end:
                                elements_all[x].at[y, 'notes'] = elements_all[x].at[y, 'notes'] - 12 

                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)
            
            # d8
            if 'd8' in random_events:
                if 'Chorus' in i:
                    if x == 'hihats':
                        for y in range(len(elements_all[x])):
                            if start <= elements_all[x].at[y, 'time'] < end:
                                elements_all[x] = elements_all[x].drop(y)

                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)

            # m1
            if 'd3' in random_events:
                if 'Verse' in i or 'Chorus' in i:
                    if x in ['chords1', 'chords2']:
                        for y in range(len(elements_all[x])):
                            if start <= elements_all[x].at[y, 'time'] < end:
                                elements_all[x].at[y, 'notes'] = elements_all[x].at[y, 'notes'] - 12 
                
                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)
            
            # m2
            if 'd4' in random_events:
                if 'Verse' in i or 'Chorus' in i:
                    if x == 'lead':
                        for y in range(len(elements_all[x])):
                            if start <= elements_all[x].at[y, 'time'] < end:
                                elements_all[x].at[y, 'notes'] = elements_all[x].at[y, 'notes'] - 12 
                
                        elements_all[x] = elements_all[x].sort_index().reset_index(drop=True)
        
            
    return(elements_all)
