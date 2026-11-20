# MIDI Repeat Passes

Make a rehearsal MIDI in which the backing part plays only on the selected trips through an expanded repeat.

## English quickstart

**[Follow the step-by-step tutorial](TUTORIAL.md)**

Download the named ZIP under **Assets** on the [release page](https://github.com/Uone100/midi-repeat-passes/releases/latest). Extract it and open a terminal in the folder that contains `SKILL.md`.

Python 3.9 or later with Mido. Install it with `python -m pip install mido`. No synthesizer is required to generate the file.

```sh
python examples/make_demo.py four.mid
python scripts/passes.py four.mid
python scripts/passes.py four.mid rehearsal.mid --track 1 --start 0 --length 1 --passes 4 --play-on 2,4
```

The four passes each start with one backing note. The report shows `[1, 0, 1, 0]` removed.

## Use as an Agent Skill

Extract the ZIP contents into `.agents/skills/midi-repeat-passes/` in a Codex project or `.claude/skills/midi-repeat-passes/` in a Claude Code project. Confirm that `SKILL.md` sits directly inside that folder, then start a new session. The tutorial includes an example request and the inputs to supply. You can also use the commands directly.

## Where the request came from

Arrangers describe needing parts to enter only on particular repeat passes. This workflow produces an edited rehearsal MIDI from expanded playback. [MuseScore request](https://github.com/musescore/MuseScore/issues/19994)
