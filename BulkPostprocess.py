from pydub.utils import make_chunks
from pydub import AudioSegment
from os import listdir
import numpy as np
import math
import os
import datetime

def reduce_volume(atrack, trvol):

    stsound = -22

    if trvol < stsound:
        chvol = (stsound - trvol)
        atrack = atrack + chvol

    if trvol > stsound:
        chvol = (trvol - stsound)
        atrack = atrack - chvol

    return atrack

def bass_line_freq(track):
    #sample_track = list(track)

    # c-value
    est_mean = np.mean(track)

    # a-value
    est_std = 3 * np.std(track) / (math.sqrt(2))

    bass_factor = int(round((est_std - est_mean) * 0.005))

    return bass_factor

def get_loudness(sound, slice_size):
    return max(chunk.dBFS for chunk in make_chunks(sound, slice_size))

contenttrax = []

for subdir, dirs, files in os.walk('C:\\Users\\mysti\\Desktop\\AutoProd'):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".wav") and ("_Post" not in str(filepath)):
            cline = str(filepath)
            contenttrax.append(cline)

for elem in contenttrax:

    right_now = datetime.datetime.now().isoformat()

    list = []

    for i in right_now:
        if i.isnumeric():
            list.append(i)

    time = ("".join(list))

    attenuate_db = 0
    accentuate_db = .24
    goldsound = -18
    stsound = -23

    newAudio = AudioSegment.from_wav(elem)
    leng = len(newAudio)

    startvol = get_loudness(newAudio, leng)

    if startvol < -16 and startvol > -18.5:

        newAudio2 = reduce_volume(newAudio, startvol)

        filtered = newAudio2.low_pass_filter(bass_line_freq(newAudio2.get_array_of_samples()))

        newAudio3 = (newAudio2 - attenuate_db).overlay(filtered + accentuate_db)

        loudn = get_loudness(newAudio3, leng)

        print(loudn)


        if loudn <= goldsound:
            chvol = (goldsound - loudn)
            newAudio3 = newAudio3 + chvol

        if loudn > goldsound:
            chvol = (loudn - goldsound)
            newAudio3 = newAudio3 - chvol

        oustr = "C:\\Users\\mysti\\Desktop\\AutoProd\\Processed\\_" + str(time) + "_Post.wav"
    

        newAudio3.export(oustr, format="wav")
