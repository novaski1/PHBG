import random
import pandas as pd
import subprocess
import os
from block import block_structure, block_to_chords, block_to_bass, block_to_lead, block_to_pluck
from drums import drums_movements2, eightoeight_notes, hihats_notes, kick_notes, snare_notes
from track import track_chooser, track_random_events, track_to_notes
from sf2 import return_sf2
from quality_check import quality_check
from midi_export import midi_writer


def phbg(seed, info, how_much):

    for i in range(how_much):

        print('1. Creating base track elements')
        
        # Parameters
        notes_used = info['notes_used']
        chord_select = info['chord_select']
        scale = info['scale']
        bpm = info['bpm']
        beat = info['beat']
        num_chords = info['num_chords']
        length = info['length']
        style_drums = info['style_drums']

        # Setting seed for elements generation
        random.seed(seed)

        # Creating main chord progression
        block1 = block_structure(notes_used, beat, num_chords, chord_select)
        block2 = block1

        # Creating loop of individual elements
        elements = {'chords1': [], 'chords2': [], 'pad': [], 'lead': [], 'pluck': [], 'bass': [], 'eightoeight': [], 'hihats': [], 'kick': [], 'snare': []}
        movements = drums_movements2(beat)
        elements = elements_to_notes(elements, block1, block2, notes_used, scale, beat, style_drums, movements)

        # QC on each elements
        elements = quality_check_elements(elements, 1)

        # Setting seed for track structure generation
        random.seed(seed[1])

        print('2. Creating track structure')

        # Creating track structure
        track, length_elements = track_chooser(beat, bpm, length)

        # Extending loops to match track structure (+ random events)
        elements_all = {'chords1': None, 'chords2': None, 'pad': None, 'lead': None, 'pluck': None, 'bass': None, 'eightoeight': None, 'hihats': None, 'kick': None, 'snare': None}
        elements_all = elements_to_track(elements_all, elements, track, beat)
        elements_all = track_random_events(elements_all, track)

        # QC on each elements
        elements_all = quality_check_elements(elements_all, 2)

        print('3. Generating MIDI files')

        # Creating MIDI tracks for each element
        elements_to_midi(elements_all, bpm)

        print('4. Rendering individual audio files')

        # Creating audio files for each MIDI track
        sf2list = return_sf2(['chords', 'chords', 'lead', '808', 'snare', 'hats', 'chords', 'pluck'])
        midi_to_audio(elements_all,sf2list)

        print('5. Rendering final mix')

        # Merging all audio files together
        final_mix(seed, elements_all)

        print(str('Track successfully generated at: ') + os.path.dirname(os.path.abspath(__file__)).replace("\\","/") + "/wav/mix_" + seed + ".wav")

def elements_to_notes(elements, block1, block2, notes_used, scale, beat, style_drums, movements):
    for i in elements:
        for x in range(2):
            if i == 'chords1' and x == 0: elements[i].append(block_to_chords(notes_used, block1, scale))
            if i == 'chords1' and x == 1: elements[i].append(elements['chords1'][0])
            if i == 'chords2': elements[i].append(elements['chords1'][x])
            if i == 'pad': elements[i].append(elements['chords1'][x])
            if i == 'lead' and x == 0: elements[i].append(block_to_lead(notes_used, beat, block1, scale))
            if i == 'lead' and x == 1: elements[i].append(block_to_lead(notes_used, beat, block2, scale))
            if i == 'pluck' and x == 0: elements[i].append(block_to_pluck(notes_used, beat, block1, scale))
            if i == 'pluck' and x == 1: elements[i].append(block_to_pluck(notes_used, beat, block2, scale))
            if i == 'bass' and x == 0: elements[i].append(block_to_bass(notes_used, block1, scale, beat))
            if i == 'bass' and x == 1: elements[i].append(block_to_bass(notes_used, block2, scale, beat))
            if i == 'eightoeight': elements[i].append(eightoeight_notes(beat, elements['bass'][x]))
            if i == 'hihats': elements[i].append(hihats_notes(beat, style_drums, movements))
            if i == 'kick': elements[i].append(kick_notes(beat, style_drums, movements))
            if i == 'snare': elements[i].append(snare_notes(beat, style_drums, movements))
      
    return(elements)

def elements_to_track(elements_all, elements, track, beat):
    for i in elements_all:
        if i == 'chords1': elements_all[i] = track_to_notes(elements[i], track, 'Chords1', beat)
        if i == 'chords2': elements_all[i] = track_to_notes(elements[i], track, 'Chords2', beat)
        if i == 'pad': elements_all[i] = track_to_notes(elements[i], track, 'Pad', beat)
        if i == 'lead': elements_all[i] = track_to_notes(elements[i], track, 'Lead', beat)
        if i == 'pluck': elements_all[i] = track_to_notes(elements[i], track, 'Pluck', beat)
        if i == 'bass': elements_all[i] = track_to_notes(elements[i], track, 'Bass', beat)
        if i == 'eightoeight': elements_all[i] = track_to_notes(elements[i], track, '808', beat)
        if i == 'hihats': elements_all[i] = track_to_notes(elements[i], track, 'Hats', beat)
        if i == 'kick': elements_all[i] = track_to_notes(elements[i], track, 'Kick', beat)
        if i == 'snare': elements_all[i] = track_to_notes(elements[i], track, 'Snare', beat)
    
    return(elements_all)

def quality_check_elements(elements, type):

    # List of dataframes (elements)
    if type == 1:
        list_elements_qc2 = quality_check([elements['chords1'][1], elements['chords2'][1], elements['pad'][1], elements['lead'][1], elements['pluck'][1], elements['bass'][1], elements['eightoeight'][1], elements['hihats'][1], elements['kick'][1], elements['snare'][1]])
        elements['chords1'][1], elements['chords2'][1], elements['pad'][1], elements['lead'][1], elements['pluck'][1], elements['bass'][1], elements['eightoeight'][1], elements['hihats'][1], elements['kick'][1], elements['snare'][1] = list_elements_qc2[0], list_elements_qc2[1], list_elements_qc2[2], list_elements_qc2[3], list_elements_qc2[4], list_elements_qc2[5], list_elements_qc2[6], list_elements_qc2[7], list_elements_qc2[8], list_elements_qc2[9]
        list_elements_qc1 = quality_check([elements['chords1'][0], elements['chords2'][0], elements['pad'][0], elements['lead'][0], elements['pluck'][0], elements['bass'][0], elements['eightoeight'][0], elements['hihats'][0], elements['kick'][0], elements['snare'][0]])
        elements['chords1'][0], elements['chords2'][0], elements['pad'][0], elements['lead'][0], elements['pluck'][0], elements['bass'][0], elements['eightoeight'][0], elements['hihats'][0], elements['kick'][0], elements['snare'][0] = list_elements_qc1[0], list_elements_qc1[1], list_elements_qc1[2], list_elements_qc1[3], list_elements_qc1[4], list_elements_qc1[5], list_elements_qc1[6], list_elements_qc1[7], list_elements_qc1[8], list_elements_qc1[9]
    
    # Just dataframes (elements_all)
    if type == 2:
        list_elements_qc1 = quality_check([elements['chords1'], elements['chords2'], elements['pad'], elements['lead'], elements['pluck'], elements['bass'], elements['eightoeight'], elements['hihats'], elements['kick'], elements['snare']])
        elements['chords1'], elements['chords2'], elements['pad'], elements['lead'], elements['pluck'], elements['bass'], elements['eightoeight'], elements['hihats'], elements['kick'], elements['snare'] = list_elements_qc1[0], list_elements_qc1[1], list_elements_qc1[2], list_elements_qc1[3], list_elements_qc1[4], list_elements_qc1[5], list_elements_qc1[6], list_elements_qc1[7], list_elements_qc1[8], list_elements_qc1[9]

    return(elements)

def elements_to_midi(elements_all, bpm):
    for i in elements_all:
        if i == 'chords1': midi_writer(elements_all[i], "chords1", bpm)
        if i == 'chords2': midi_writer(elements_all[i], "chords2", bpm)
        if i == 'pad': midi_writer(elements_all[i], "pad", bpm)
        if i == 'lead': midi_writer(elements_all[i], "lead", bpm)
        if i == 'pluck': midi_writer(elements_all[i], "pluck", bpm)
        if i == 'bass': midi_writer(elements_all[i], "bass", bpm)
        if i == 'eightoeight': midi_writer(elements_all[i], "808", bpm)
        if i == 'hihats': midi_writer(elements_all[i], "hihats", bpm)
        if i == 'kick': midi_writer(elements_all[i], "kick", bpm)
        if i == 'snare': midi_writer(elements_all[i], "snare", bpm)

def midi_to_audio(elements_all, sf2list):

    current_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")

    for i in elements_all:
        if i == 'chords1': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/chords/' + sf2list[0]), str(current_path + '/midi/chords1.mid'), str(current_path + '/wav/chords1.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if i == 'chords2': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/chords/' + sf2list[1]), str(current_path + '/midi/chords2.mid'), str(current_path + '/wav/chords2.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #if i == 'chords1': subprocess.run(['python', '-m', 'midi2audio', '-s', 'sf2/chords/chords22.sf2', 'midi/chords1.mid', 'wav/chords1.wav'])
        #if i == 'chords2': subprocess.run(['python', '-m', 'midi2audio', '-s', 'sf2/chords/chords24.sf2', 'midi/chords2.mid', 'wav/chords2.wav'])
        if i == 'pad': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/chords/' + sf2list[6]), str(current_path + '/midi/pad.mid'), str(current_path + '/wav/pad.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if i == 'lead': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/lead/' + sf2list[2]), str(current_path + '/midi/lead.mid'), str(current_path + '/wav/lead.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if i == 'pluck': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/pluck/' + sf2list[7]), str(current_path + '/midi/pluck.mid'), str(current_path + '/wav/pluck.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if i == 'bass': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/bass/bassv1.sf2'), str(current_path + '/midi/bass.mid'), str(current_path + '/wav/bass.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if i == 'eightoeight': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/808/808v1.sf2'), str(current_path + '/midi/808.mid'), str(current_path + '/wav/808.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if i == 'hihats': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/hats/' + sf2list[5]), str(current_path + '/midi/hihats.mid'), str(current_path + '/wav/hihats.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if i == 'kick': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/kick/kickv1.sf2'), str(current_path + '/midi/kick.mid'), str(current_path + '/wav/kick.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if i == 'snare': subprocess.run(['python', '-m', 'midi2audio', '-s', str(current_path + '/sf2/snare/' + sf2list[4]), str(current_path + '/midi/snare.mid'), str(current_path + '/wav/snare.wav')], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #if i == 'snare': subprocess.run(['python', '-m', 'midi2audio', '-s', 'sf2/snare/snare3.sf2', 'midi/snare.mid', 'wav/snare.wav'])

def final_mix(seed, elements_all):
    current_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
    a = str(str(seed) + ' ' + current_path + '/wav/hihats.wav ' + current_path + '/wav/snare.wav ' + current_path + '/wav/kick.wav ' + current_path + '/wav/bass.wav ' + current_path + '/wav/808.wav ' + current_path + '/wav/lead.wav ' + current_path + '/wav/chords1.wav ' + current_path + '/wav/chords2.wav')
    subprocess.call(str('python ' + current_path + '/audio_merger.py ' + a))

if __name__ == "__main__":

    info = {
    'notes_used':   'minor',        # Musical scale to be used. Possible values: major, minor
    'chord_select': 'preset',       # Algorithm for chord progression selection. Possible values: auto, preset
    'scale':        'C',            # Root note to be used: Possible values: A, A#, B, C, C#, D, D#, E, F, F#, G, G#
    'bpm':           140,           # Track tempo (BPM). Range recommended: between 70 and 180 (but no limitation)
    'beat':          16,            # Length of the main motif. Possible values: 4, 8, 16, 32
    'num_chords':    2,             # Number of chords in chord progression. Possible values: 2, 3, 4
    'length':       'short',        # Track length. Possible values: short, normal, long
    'style_drums':  'trap'          # Drums style. Possible values: trap, halftime
    }

    seed = str(random.choice(range(9999)))

    phbg(seed, info, 1)