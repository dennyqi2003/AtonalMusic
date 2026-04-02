from itertools import product
import ast


# Lutoslawski's chord-class templates (skip I).
# Each template is represented as cumulative semitone offsets from 0.
CHORD_TEMPLATES = {
	"A": [0, 3, 6, 9],
	"B": [0, 3, 6, 10],
	"C": [0, 3, 7, 10],
	"D": [0, 4, 7, 10],
	"E": [0, 3, 7, 11],
	"F": [0, 4, 7, 11],
	"G": [0, 4, 8, 11],
	"H": [0, 3, 8, 11],
	"J": [0, 3, 6, 11],
	"K": [0, 5, 8, 11],
}


def cyclic_rotations(seq):
	"""
	Generate all cyclic rotations of a sequence.
	"""
	n = len(seq)
	for i in range(n):
		yield seq[i:] + seq[:i]


def chord_variants(code):
	"""
	Generate all distinct 4-note pitch-class sets (sorted tuples) for a chord code.

	Construction rule:
	1) take the template as a linear stacked chord,
	2) allow cyclic choice of the starting note,
	3) transpose by t in [0..11],
	4) map to pitch classes mod 12 and sort.
	"""
	if code not in CHORD_TEMPLATES:
		raise ValueError(f"Unknown chord code: {code}")

	template = CHORD_TEMPLATES[code]
	results = set()

	for rot in cyclic_rotations(template):
		# Keep linear stacking by lifting wrapped values by +12.
		linear = []
		prev = None
		for x in rot:
			if prev is None:
				v = x
			else:
				v = x
				while v <= prev:
					v += 12
			linear.append(v)
			prev = v

		for t in range(12):
			pcs = tuple(sorted(((x + t) % 12) for x in linear))
			results.add(pcs)

	return sorted(results)


def solve_triple(code3):
	"""
	Enumerate all ordered (high, middle, low) solutions for a 3-code string.

	A solution is valid iff:
	- high matches code3[0], middle matches code3[1], low matches code3[2], and
	- the three 4-note sets are pairwise disjoint (thus covering all 12 pitch classes).
	"""
	code3 = code3.strip().upper()
	if len(code3) != 3:
		raise ValueError("Input must be exactly 3 chord codes, e.g., CHC or BKB.")

	for c in code3:
		if c not in CHORD_TEMPLATES:
			raise ValueError(f"Invalid chord code: {c}. Allowed: {''.join(CHORD_TEMPLATES)}")

	high_code, mid_code, low_code = code3
	high_candidates = chord_variants(high_code)
	mid_candidates = chord_variants(mid_code)
	low_candidates = chord_variants(low_code)

	solutions = []

	for high, mid, low in product(high_candidates, mid_candidates, low_candidates):
		hs, ms, ls = set(high), set(mid), set(low)

		# Pairwise disjointness implies union size = 12 because each set has size 4.
		if hs & ms:
			continue
		if hs & ls:
			continue
		if ms & ls:
			continue

		solutions.append((high, mid, low))

	return solutions


def print_solutions(code3):
	"""
	Print all ordered solutions for the 3-code query.
	"""
	solutions = solve_triple(code3)

	if not solutions:
		print(f"No solution for {code3.upper()}.")
		return

	print(f"Input: {code3.upper()}")
	print(f"Total solutions: {len(solutions)}")
	print()

	for i, (high, mid, low) in enumerate(solutions, start=1):
		print(f"Solution {i}:")
		print(f"  High strand:   {list(high)}")
		print(f"  Middle strand: {list(mid)}")
		print(f"  Low strand:    {list(low)}")
		print()


def parse_interval_pattern(text):
	"""
	Parse an interval-pairing pattern such as "2,5" or "[1,5,6]".
	"""
	text = text.strip()
	if not text:
		raise ValueError("Interval pattern cannot be empty.")

	if text[0] in "[(":
		value = ast.literal_eval(text)
		if not isinstance(value, (list, tuple)):
			raise ValueError("Interval pattern must be a list or tuple of integers.")
		intervals = [int(x) for x in value]
	else:
		parts = [part.strip() for part in text.split(",") if part.strip()]
		intervals = [int(part) for part in parts]

	if not intervals:
		raise ValueError("Interval pattern cannot be empty.")

	for ic in intervals:
		if not (1 <= ic <= 6):
			raise ValueError("Interval classes must be integers between 1 and 6.")

	return intervals


def interval_class_to_semitone_options(interval_class):
	"""
	Convert one interval class to all ascending semitone options.
	"""
	if interval_class == 6:
		return (6,)
	return (interval_class, 12 - interval_class)


def generate_interval_pairing_chords(interval_pattern):
	"""
	Generate all 12-tone chords formed by stacking an interval pattern.

	At each of the 11 steps, any interval class from the input set may be used
	(not necessarily in a fixed cyclic order). For each interval class, we may
	ascend by either `ic` semitones or `12 - ic` semitones. Only sequences that
	reach all 12 pitch classes exactly once are kept.

	All 12 transpositions are generated for each base solution starting on 0.
	"""
	if isinstance(interval_pattern, str):
		interval_pattern = parse_interval_pattern(interval_pattern)

	# Deduplicate while preserving order.
	unique_ics = list(dict.fromkeys(interval_pattern))

	base_solutions = set()

	def backtrack(step, chord, used_pcs):
		if step == 11:
			base_solutions.add(tuple(chord))
			return

		current_pitch = chord[-1]

		for ic in unique_ics:
			for semitones in interval_class_to_semitone_options(ic):
				next_pitch = (current_pitch + semitones) % 12
				if next_pitch in used_pcs:
					continue

				used_pcs.add(next_pitch)
				chord.append(next_pitch)
				backtrack(step + 1, chord, used_pcs)
				chord.pop()
				used_pcs.remove(next_pitch)

	backtrack(0, [0], {0})

	all_solutions = set()
	for chord in base_solutions:
		for t in range(12):
			all_solutions.add(tuple((pitch + t) % 12 for pitch in chord))

	return sorted(all_solutions)


def print_interval_pairing_chords(interval_pattern_text):
	"""
	Print all 12-tone chords for an interval-pairing pattern.
	"""
	interval_pattern = parse_interval_pattern(interval_pattern_text)
	chords = generate_interval_pairing_chords(interval_pattern)

	if not chords:
		print(f"No 12-tone chord found for interval pattern {interval_pattern}.")
		return

	print(f"Interval pattern: {interval_pattern}")
	print(f"Total chords: {len(chords)}")
	print()

	for i, chord in enumerate(chords, start=1):
		print(f"Chord {i}: {list(chord)}")


def main():
	try:
		print("Choose an option:")
		print("1) Solve a 3-strand Lutoslawski chord-code problem")
		print("2) Generate interval-pairing 12-tone chords")

		choice = input("Enter choice (1 or 2): ").strip()
		if choice == "1":
			text = input("Enter 3 chord codes (e.g., CHC, BKB, AAA): ").strip()
			print_solutions(text)
		elif choice == "2":
			text = input("Enter an interval pattern (e.g., 2,5 or 1,5,6): ").strip()
			print_interval_pairing_chords(text)
		else:
			raise ValueError("choice must be 1 or 2.")
	except Exception as e:
		print(f"Error: {e}")


if __name__ == "__main__":
	main()
