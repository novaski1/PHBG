def quality_check(notes_list):

    for i in range(len(notes_list)):
        notes_list[i] = tone_fix(notes_list[i])
        notes_list[i] = overlapping(notes_list[i])
        notes_list[i] = drop_empty(notes_list[i])
    
    return(notes_list)

def tone_fix(notes):

    notes = notes.reset_index(drop=True)
    for i in range(len(notes)):
        if notes.at[i, 'notes'] < 48: notes.at[i, 'notes'] += 12
        if notes.at[i, 'notes'] > 72: notes.at[i, 'notes'] -= 12

    return(notes)

def overlapping(notes):
    
    notes.drop_duplicates(keep=False,inplace=True)
    notes = notes.sort_values(['notes', 'time'], ascending=['True', 'True'])
    notes = notes.reset_index(drop=True)

    for i in range(len(notes)):
        if i != len(notes) - 1 and len(notes) != 1:
            notes.at[i, 'next_time'] = notes.at[i+1, 'time']
            
            if notes.at[i, 'notes'] == notes.at[i+1, 'notes'] and notes.at[i, 'next_time'] < notes.at[i, 'time_end']:
                notes.at[i, 'time_end'] = notes.at[i, 'next_time']
                notes.at[i, 'duration'] = notes.at[i, 'time_end'] - notes.at[i, 'time']
            
            notes = notes.drop(columns=['next_time'])

    return(notes)

def drop_empty(notes):

    for i in range(len(notes)):
        try:
            if notes.at[i, 'time'] == notes.at[i, 'time_end'] or notes.at[i, 'duration'] <= 0: 
                notes = notes.drop(i)
        except: print('')
    
    notes = notes.reset_index(drop=True)
    return(notes)