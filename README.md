## atonal_music

Small Python utilities for pitch-class set analysis in 12-tone / atonal contexts.

### Files

#### [basics.py](basics.py)
Pitch-class set and interval-vector utilities. Menu options:
1. Compute the interval vector of one pc set (e.g. `[0,2,3,5]` → `[1,2,2,0,1,0]`)
2. Print all transposition-normalized pc sets of size `m` and their interval vectors
3. Print only interval vectors shared by 2 or more pc sets of size `m`

#### [lutoslawski.py](lutoslawski.py)
Lutosławski harmonic tools. Menu options:
1. **3-strand chord-code solver** — given three chord codes (e.g. `CHC`, `BKB`), enumerate all ordered (high / middle / low) 4-note chord realizations that together cover all 12 pitch classes. Chord codes A–K (no I) are supported:

   | Code | pc set | Stack |
   |------|--------|-------|
   | A | `[0,3,6,9]` | dim7 (+3+3+3) |
   | B | `[0,3,6,10]` | half-dim7 (+3+3+4) |
   | C | `[0,3,7,10]` | min7 (+3+4+3) |
   | D | `[0,4,7,10]` | dom7 (+4+3+3) |
   | E | `[0,3,7,11]` | minM7 (+3+4+4) |
   | F | `[0,4,7,11]` | maj7 (+4+3+4) |
   | G | `[0,4,8,11]` | augM7 (+4+4+3) |
   | H | `[0,3,8,11]` | Lutosławski (+3+5+3) |
   | J | `[0,3,6,11]` | Lutosławski (+3+3+5) |
   | K | `[0,5,8,11]` | Lutosławski (+5+3+3) |

2. **Feasible code-triple enumeration** — enumerate all ordered chord-type triples from `AAA` to `KKK` (A–K, no I) and keep only triples that admit at least one valid full-aggregate solution under feature 1.

3. **Interval-pairing 12-tone chord generator** — given a set of interval classes (e.g. `2,5` or `1,5,6`), enumerate all 12-tone ordered pitch-class sequences that can be built by freely stacking those interval classes (each applied as either `+ic` or `+(12−ic)` semitones). All 12 transpositions are included.

### Requirements

- Python 3.8+
- Standard library only (no external packages)

### Quick start

```
python basics.py
python lutoslawski.py
```

### Notes

- Pitch classes are integers `0..11`; interval classes are integers `1..6`.
- Interval vector format: `[ic1, ic2, ic3, ic4, ic5, ic6]`.
- In [basics.py](basics.py), enumerated pc sets are transposition-normalized (first pc fixed at `0`).
- In [lutoslawski.py](lutoslawski.py), 3-strand solutions are ordered: high, middle, low.
