from pydub import AudioSegment, effects
import os

typ = input(str())

# Note: wav files should be exported in 24 bits in Cubase
for i in os.listdir(str('cpr/wav files/' + typ + '/to convert')):
    
    sound = AudioSegment.from_file(str('cpr/wav files/' + typ + '/to convert/' + str(i)), format="wav")
    print(str('cpr/wav files/' + typ + '/to convert/' + str(i)))
    print(i)
    sound = effects.compress_dynamic_range(sound, threshold=-20.0, ratio=20.0, attack=5.0, release=50.0)
    sound = effects.normalize(sound)
    # -14 for chords
    # -22 for lead
    sound = sound - 14

    sound.export(str('cpr/wav files/' + typ + '/to convert/output_' + i), format="wav")