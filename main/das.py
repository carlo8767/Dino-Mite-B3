from mido import Message, MidiFile, MidiTrack, bpm2tempo
from midi2audio import FluidSynth
import pygame

# -------------------------
# 1. CREATE MIDI FILE
# -------------------------
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

tempo = bpm2tempo(120)

track.append(Message('program_change', program=12, time=0))

melody = [
    60, 62, 64, 65, 67, 65, 64, 62,
    60, 60, 67, 67, 69, 69, 67
]

note_duration = 480

for note in melody:
    track.append(Message('note_on', note=note, velocity=80, time=0))
    track.append(Message('note_off', note=note, velocity=80, time=note_duration))

mid.save('simple_melody.mid')


# -------------------------
# 2. CONVERT MIDI → WAV
# -------------------------
fs = FluidSynth("FluidR3_GM.sf2")  # path to soundfont
fs.midi_to_audio("simple_melody.mid", "output.wav")


# -------------------------
# 3. PLAY AUDIO WITH PYGAME
# -------------------------
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("output.wav")
pygame.mixer.music.play()

while pygame.mixer.music.get_busy():
    pygame.time.wait(100)

print("Done!")