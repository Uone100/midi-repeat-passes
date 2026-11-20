---
name: midi-repeat-passes
description: Prepare a rehearsal MIDI where a selected instrument enters only on chosen passes of an already expanded repeated passage, preserving the original printed score and the event timing of other parts.
---
Inspect the user's MIDI export first with `python scripts/passes.py input.mid`. Obtain the target track, the actual start of the first pass, the length of one pass, the pass count, and which passes should play. Positions use quarter notes, measured from the start of the MIDI file. Check pickups and alternate endings explicitly; use this tool only for equal-length passes already present in the file.

Generate a new MIDI using the command in TUTORIAL.md. The tool removes matched note-on/off pairs for suppressed onsets; events on other tracks and controller messages keep their positions. A note begun before a suppressed interval may ring across its boundary. For a full acoustic cutoff or variable-length passes, use a DAW and confirm the desired phrasing. Compare the reported counts and audition each join before delivering an audio render.
