# Rehearse with the backing part on passes two and four

The demo contains two instruments named Leader and Backing. Each plays one note on each of four equal-length passes. You will create a new MIDI that keeps the leader throughout and rests the backing on the first and third passes.

## Set up

Download the named ZIP under **Assets** on the [release page](https://github.com/Uone100/midi-repeat-passes/releases/latest). Extract it and open a terminal in the folder that contains `SKILL.md`.

Python 3.9 or later with Mido. Install it with `python -m pip install mido`. No synthesizer is required to generate the file.

## Follow the example

Run the quickstart commands below.

```sh
python examples/make_demo.py four.mid
python scripts/passes.py four.mid
python scripts/passes.py four.mid rehearsal.mid --track 1 --start 0 --length 1 --passes 4 --play-on 2,4
```

 The inventory prints track indices, names and lengths in ticks. Check that track 1 is Backing. The last command writes `rehearsal.mid`. Its JSON output should include:

```json
{"original_onsets_by_pass":[1,1,1,1],"removed_onsets_by_pass":[1,0,1,0]}
```

Import both files into your sequencer. In the new file the leader still plays four notes, and the backing has two notes at the original times of passes 2 and 4.

## Adapt the timing to your music

1. Export a MIDI whose timeline already contains every repeat pass. Run the inventory and find the target instrument's zero-based track index.
2. Measure from the beginning in **quarter notes**. For example, if four bars of 4/4 precede the repeat, use `--start 16`. If each repeated section lasts two bars of 4/4, use `--length 8`. Pickup bars change the start position.
3. Set `--passes` to the number of expanded passes. Enter the **one-based** passes that should sound in `--play-on`. Choose an unused output name.
4. Listen to transitions in your sequencer. Selection follows each note's onset, including notes held across a boundary. Sustain pedals, controllers and program changes remain in place.

If another track shares the instrument's note channel, isolate that instrument before retrying. Unequal endings and unexpanded score repeats need manual arrangement. If the demo already exists, use new filenames for both MIDI files.

## Ask an agent

“Inspect my expanded rehearsal MIDI. Mute the brass on passes one and three and export a new file.” Give the agent the track name, repeat start, length and pass count.
