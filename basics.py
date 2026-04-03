from itertools import combinations
from collections import defaultdict
import ast


def normalize_pc_set(pc_set):
    """
    Normalize a pc set to sorted unique pitch classes in 0..11.
    """
    return sorted({int(p) % 12 for p in pc_set})


def transpose_to_zero(sorted_pcs):
    """
    Transpose a sorted pitch-class list so its first element becomes 0.
    """
    if not sorted_pcs:
        return tuple()
    first = sorted_pcs[0]
    return tuple(p - first for p in sorted_pcs)


def best_rotation_form(pcs):
    """
    Return the best normal order (transposed to 0) among all rotations.

    Comparison rule:
    1) smallest outer span,
    2) if tied, lexicographically smallest adjacent-interval sequence,
    3) if still tied, lexicographically smallest zeroed tuple.
    """
    m = len(pcs)
    if m <= 1:
        return tuple(pcs)

    best_key = None
    best_form = None

    for i in range(m):
        rotated = pcs[i:] + [p + 12 for p in pcs[:i]]
        zeroed = tuple(x - rotated[0] for x in rotated)
        span = zeroed[-1]
        adjacent = tuple(zeroed[j + 1] - zeroed[j] for j in range(m - 1))
        key = (span, adjacent, zeroed)

        if best_key is None or key < best_key:
            best_key = key
            best_form = zeroed

    return best_form


def invert_pc_set(pcs):
    """
    Invert a normalized pc set around 0 and return sorted unique pitch classes.
    """
    return sorted((-p) % 12 for p in pcs)


def prime_form(pc_set):
    """
    Return the prime form under rotation + transposition + inversion.

    Rule used:
    1) find best normal order for original pc set,
    2) find best normal order for inverted pc set,
    3) choose the smaller one by the same ordering rule.
    """
    pcs = normalize_pc_set(pc_set)
    original_form = best_rotation_form(pcs)
    inverted_form = best_rotation_form(invert_pc_set(pcs))

    def form_key(form):
        span = form[-1] if form else 0
        adjacent = tuple(form[j + 1] - form[j] for j in range(len(form) - 1))
        return (span, adjacent, form)

    return min(original_form, inverted_form, key=form_key)


def is_prime_form(pc_set):
    """
    Check whether a pc set is already in prime form (with inversion equivalence).
    """
    pcs = normalize_pc_set(pc_set)
    return transpose_to_zero(pcs) == prime_form(pcs)


def interval_vector(pc_set):
    """
    Compute the interval vector of a pitch-class set.

    Duplicate pitch classes are removed, and all values are normalized mod 12.
    The result is returned as a list [ic1, ic2, ic3, ic4, ic5, ic6].
    """
    pcs = sorted({p % 12 for p in pc_set})

    vec = [0] * 6
    for a, b in combinations(pcs, 2):
        d = (b - a) % 12
        ic = min(d, 12 - d)
        if 1 <= ic <= 6:
            vec[ic - 1] += 1
    return vec


def parse_pc_set(text):
    """
    Parse a user-entered pc set such as [0,2,3,5].
    """
    value = ast.literal_eval(text)
    if not isinstance(value, (list, tuple, set)):
        raise ValueError("pc set must be a list, tuple, or set of integers.")
    return list(value)


def print_single_interval_vector():
    """
    Read one pc set from input and print its interval vector.
    """
    text = input("Enter a pc set (e.g., [0,2,3,5]): ").strip()
    pc_set = parse_pc_set(text)
    vec = interval_vector(pc_set)
    print(f"interval vector = {vec}")


def generate_pc_sets_of_size(m):
    """
    Generate all transposition-normalized pc sets of size m.

    We fix 0 as the first pitch class, then choose the remaining m-1
    pitch classes from 1..11 in ascending order.
    """
    if not (1 <= m <= 12):
        raise ValueError("m must be between 1 and 12.")

    if m == 1:
        yield [0]
        return

    for tail in combinations(range(1, 12), m - 1):
        yield [0, *tail]


def print_interval_vectors_for_size(m):
    """
    Print prime-form pc sets of size m and their interval vectors.
    """
    for pc_set in generate_pc_sets_of_size(m):
        if not is_prime_form(pc_set):
            continue
        vec = interval_vector(pc_set)
        vec_str = "".join(map(str, vec))
        print(f"{pc_set} -> {vec_str}")


def print_shared_interval_vectors_for_size(m):
    """
    Print interval vectors that correspond to two or more prime-form pc sets of size m.

    Output is sorted by lexicographic order of the interval vector
    (comparing ic1, then ic2, ..., then ic6).
    """
    groups = defaultdict(list)

    for pc_set in generate_pc_sets_of_size(m):
        if not is_prime_form(pc_set):
            continue
        vec_key = tuple(interval_vector(pc_set))
        groups[vec_key].append(pc_set)

    shared_items = [(vec, sets) for vec, sets in groups.items() if len(sets) >= 2]
    shared_items.sort(key=lambda item: item[0])

    for vec, sets in shared_items:
        print(f"interval vector {list(vec)}:")
        for pc_set in sets:
            pc_set_text = ",".join(map(str, pc_set))
            print(f"  {pc_set_text}")
        print()


def main():
    try:
        print("Choose an option:")
        print("1) Compute the interval vector of one pc set")
        print("2) Print all pc sets of size m and their interval vectors")
        print("3) Print only interval vectors shared by 2+ pc sets of size m")

        choice = input("Enter choice (1, 2, or 3): ").strip()
        if choice not in {"1", "2", "3"}:
            raise ValueError("choice must be 1, 2, or 3.")

        if choice == "1":
            print_single_interval_vector()
        else:
            m_text = input("Enter m (pc set size, 1-12): ").strip()
            m = int(m_text)
            if choice == "2":
                print_interval_vectors_for_size(m)
            else:
                print_shared_interval_vectors_for_size(m)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()