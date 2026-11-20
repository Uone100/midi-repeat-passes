"""Write an original four-pass MIDI demo to a new file."""
import sys
from pathlib import Path
from mido import Message, MetaMessage, MidiFile, MidiTrack

def make():
    f=MidiFile(type=1,ticks_per_beat=480)
    for ch,name,base in [(0,"Leader",60),(1,"Backing",48)]:
        t=MidiTrack();f.tracks.append(t)
        t.append(MetaMessage("track_name",name=name))
        for i in range(4):
            t.append(Message("note_on",note=base+i,velocity=80,channel=ch))
            t.append(Message("note_off",note=base+i,time=480,channel=ch))
        t.append(MetaMessage("end_of_track"))
    return f
if __name__=="__main__":
    with Path(sys.argv[1]).open("xb") as out: make().save(file=out)
