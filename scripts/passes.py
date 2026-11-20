"""Filter selected repeat passes in an expanded Standard MIDI File."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
from mido import MidiFile, MidiTrack

def ticks(value,ppq):
    n=Fraction(value)*ppq
    if n.denominator!=1 or n<0:
        raise ValueError("Quarter-note positions must resolve to nonnegative integral ticks")
    return int(n)

def apply(song,track,start,length,passes,play):
    if song.type not in (0,1) or song.ticks_per_beat<=0:
        raise ValueError("Only synchronous PPQ MIDI files are supported")
    if not 0<=track<len(song.tracks) or length<=0 or not 1<=passes or not play or not play<=set(range(1,passes+1)):
        raise ValueError("Invalid track, length, pass count or play selection")
    if start+length*passes>max(sum(m.time for m in tr) for tr in song.tracks):
        raise ValueError("File ends before all indicated passes; check repeat expansion")
    original=song.tracks[track]
    channels={m.channel for m in original if m.type=="note_on" and m.velocity}
    if not channels:
        raise ValueError("Selected track has no notes")
    for i,tr in enumerate(song.tracks):
        if i!=track and any(m.type=="note_on" and m.velocity and m.channel in channels for m in tr):
            raise ValueError("Another track shares the target's note channel; isolate the instrument first")
    counts=[0]*passes
    removed=[0]*passes
    active={}
    absolute=previous=0
    out=MidiTrack()
    for m in original:
        absolute+=m.time
        drop=False
        if m.type in ("note_on","note_off"):
            key=m.channel,m.note
            if m.type=="note_on" and m.velocity:
                if key in active: raise ValueError("Overlapping instances of one pitch need DAW review")
                index=(absolute-start)//length
                if 0<=index<passes:
                    counts[index]+=1
                    drop=index+1 not in play
                    removed[index]+=int(drop)
                active[key]=drop
            else:
                if key not in active: raise ValueError("Unpaired note-off in target track")
                drop=active.pop(key)
        if not drop:
            out.append(m.copy(time=absolute-previous))
            previous=absolute
    if active: raise ValueError("Unpaired note-on in target track")
    if not any(removed): raise ValueError("No notes matched a suppressed pass; verify track and range")
    song.tracks[track]=out
    return {"original_onsets_by_pass":counts,"removed_onsets_by_pass":removed}

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input",type=Path)
    ap.add_argument("output",type=Path,nargs="?")
    ap.add_argument("--track",type=int)
    ap.add_argument("--start",type=Fraction)
    ap.add_argument("--length",type=Fraction)
    ap.add_argument("--passes",type=int)
    ap.add_argument("--play-on")
    a=ap.parse_args()
    try:
        song=MidiFile(a.input)
        if a.output is None:
            print(json.dumps({"ticks_per_quarter":song.ticks_per_beat,"tracks":[[i,t.name,sum(m.time for m in t)] for i,t in enumerate(song.tracks)]}))
        else:
            if None in (a.track,a.start,a.length,a.passes,a.play_on): ap.error("Supply all five selection options")
            r=apply(song,a.track,ticks(a.start,song.ticks_per_beat),ticks(a.length,song.ticks_per_beat),
                    a.passes,{int(x) for x in a.play_on.split(",")})
            from io import BytesIO
            out=BytesIO()
            song.save(file=out)
            with a.output.open("xb") as f: f.write(out.getvalue())
            print(json.dumps(r))
    except (ValueError,OSError,EOFError,KeyError) as exc:
        ap.exit(2,f"{exc}\n")
