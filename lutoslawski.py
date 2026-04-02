from itertools import product


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


def main():
	text = input("Enter 3 chord codes (e.g., CHC, BKB, AAA): ").strip()
	try:
		print_solutions(text)
	except Exception as e:
		print(f"Error: {e}")


if __name__ == "__main__":
	main()
