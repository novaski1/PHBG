from pydub import AudioSegment, effects
import sys
import datetime
import os

if __name__ == "__main__":

    a = 0
    current_path = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
    for i in sys.argv[2:]:

        if a == 0:
            mix = AudioSegment.from_file(str(i), format="wav")
            #mix = effects.normalize(mix)
            mix.export(str(current_path + '/wav/mix.wav'), format="wav")

            a += 1
    
        else:

            new_sound = AudioSegment.from_file(str(i), format="wav")
            #new_sound = effects.normalize(new_sound)

            if str(i) == str(current_path + '/wav/snare.wav'): 
                new_sound = new_sound - 4
            if str(i) == str(current_path + '/wav/hats.wav'): 
                new_sound = new_sound - 10
            #    new_sound = effects.high_pass_filter(new_sound, 6000)
            if str(i) == str(current_path + '/wav/kick.wav'): 
                new_sound = new_sound - 3
            #    new_sound = effects.low_pass_filter(new_sound, 500)
            if str(i) == str(current_path + '/wav/bass.wav'): 
                new_sound = new_sound - 2
                #new_sound = effects.low_pass_filter(new_sound, 100)
            if str(i) in [str(current_path + '/wav/chords1.wav'), str(current_path + '/wav/chords2.wav')]:
                new_sound = effects.normalize(new_sound)
                new_sound = effects.high_pass_filter(new_sound, 800)
                new_sound = new_sound - 42
            if str(i) == str(current_path + '/wav/pad.wav'): 
                #new_sound = effects.high_pass_filter(new_sound, 800)
                new_sound = new_sound - 12
            if str(i) == str(current_path + '/wav/lead.wav'): 
                new_sound = new_sound - 3
            if str(i) == str(current_path + '/wav/808.wav'): 
                new_sound = new_sound
            if str(i) == str(current_path + '/wav/pluck.wav'): 
                new_sound = new_sound - 3

            mix = new_sound.overlay(mix, position=0)
            mix.export(str(current_path + '/wav/mix.wav'), format="wav")

    mix = AudioSegment.from_file(str(current_path + '/wav/mix.wav'), format="wav")
    mix = effects.normalize(mix)
    #mix = mix.compress_dynamic_range(threshold=-20.0, ratio=4.0, attack=5.0, release=50.0)
    mix = mix + 5

    duration = mix.duration_seconds*1000 - 500
    mix = mix[0:duration]

    now = datetime.datetime.now()

    #mix.export(str("wav/mix_" + str(now.hour) + "." + str(now.minute) + "." + str(now.second) + ".wav"), format="wav")
    mix.export(str(current_path + '/wav/mix_' + str(sys.argv[1]) + '.wav'), format="wav")