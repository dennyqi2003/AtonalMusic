## atonal_music

Small Python utilities for pitch-class set analysis in 12-tone / atonal contexts.

### Files

- [basics.py](basics.py): compute the interval vector of one pc set, enumerate pc sets of size `m`, print all interval vectors, or print only vectors shared by 2+ pc sets.
- [lutoslawski.py](lutoslawski.py): solve 3-strand Lutosławski chord-code problems (e.g., `CHC`, `BKB`) and list all ordered full-aggregate solutions.

### Requirements

- Python 3.8+
- Standard library only (no external packages)

### Quick start

Run each script directly:

- `python basics.py`
- `python lutoslawski.py`

### Notes

- Pitch classes are represented as integers `0..11`.
- Interval vector format is `[ic1, ic2, ic3, ic4, ic5, ic6]`.
- In [basics.py](basics.py), pc sets are normalized by fixing the first pitch class as `0` when enumerating sets of size `m`.
- In [lutoslawski.py](lutoslawski.py), strands are ordered: high, middle, low.
