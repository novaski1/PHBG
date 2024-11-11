import os
from midiutil.MidiFile import MIDIFile

def midi_writer(notes, file, bpm):

    ch = [[],[],[],[],[],[],[]]

    track    = 0
    channel  = 0
    time     = 0
    volume   = 100

    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track, time, bpm)
        
    for i in range(len(notes)):
        if 'velocity' in notes.columns: volume = int(notes.at[i, 'velocity'])
        MyMIDI.addNote(track, channel, int(notes.at[i, 'notes']), notes.at[i, 'time'], notes.at[i, 'duration'], volume)
        
    with open(str(os.path.dirname(os.path.abspath(__file__)) + '/midi/' + file + ".mid"), "wb") as output_file:
        MyMIDI.writeFile(output_file)