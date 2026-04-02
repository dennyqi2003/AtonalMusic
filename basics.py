from itertools import combinations
import ast

def interval_vector(pc_set):
    pcs = sorted({p % 12 for p in pc_set})

    vec = [0] * 6  # Count occurrences of ic1, ic2, ic3, ic4, ic5, and ic6
    for a, b in combinations(pcs, 2):
        d = (b - a) % 12
        ic = min(d, 12 - d)  # interval class: 0~6
        if 1 <= ic <= 6:
            vec[ic - 1] += 1
    return vec

if __name__ == "__main__":
    s = input("input pc set (e.g., [0,2,3,5]): ").strip()
    try:
        pc_set = ast.literal_eval(s)
        vec = interval_vector(pc_set)
        print("interval vector = (ic1~ic6)", vec)  
    except Exception:
        print("Invalid input. Please enter a list of integers, e.g., [0,2,3,5].")