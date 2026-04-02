from itertools import combinations
from collections import defaultdict

from basics import interval_vector


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
    Print all pc sets of size m and their interval vectors.
    """
    for pc_set in generate_pc_sets_of_size(m):
        vec = interval_vector(pc_set)
        vec_str = "".join(map(str, vec))
        print(f"{pc_set} -> {vec_str}")


def print_shared_interval_vectors_for_size(m):
    """
    Print interval vectors that correspond to two or more pc sets of size m.

    Output is sorted by lexicographic order of the interval vector
    (comparing ic1, then ic2, ..., then ic6).
    """
    groups = defaultdict(list)

    for pc_set in generate_pc_sets_of_size(m):
        vec_key = tuple(interval_vector(pc_set))
        groups[vec_key].append(pc_set)

    shared_items = [(vec, sets) for vec, sets in groups.items() if len(sets) >= 2]
    shared_items.sort(key=lambda item: item[0])

    for vec, sets in shared_items:
        print(f"interval vector {list(vec)}:")
        for pc_set in sets:
            print(f"  {pc_set}")
        print()


def main():
    try:
        print("Choose an option:")
        print("1) Print all pc sets and their interval vectors")
        print("2) Print only interval vectors shared by 2+ pc sets")

        choice = input("Enter choice (1 or 2): ").strip()
        if choice not in {"1", "2"}:
            raise ValueError("choice must be 1 or 2.")

        m_text = input("Enter m (pc set size, 1-12): ").strip()
        m = int(m_text)
        if choice == "1":
            print_interval_vectors_for_size(m)
        else:
            print_shared_interval_vectors_for_size(m)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
