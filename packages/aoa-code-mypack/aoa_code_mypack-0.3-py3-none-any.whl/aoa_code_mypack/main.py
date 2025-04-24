# aoa_code_mypack/main.py

import os
import sys

def show_file_content(filename):
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, f"{filename}.txt")

    if not os.path.exists(file_path):
        print(f"❌ File '{filename}.txt' not found in the package.")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        print(file.read())

def cli():
    if len(sys.argv) < 2:
        print("📘 Usage: show-aoa-codes <filename>\n")
        print("📁 Available files:")
        files = [
            "codes", "binarysearch", "dijkstra", "floydwarshall", "greedy",
            "insertionsort", "knapsack", "mergesort", "nqueens", "prims",
            "quicksort", "rabincarp", "selectionsort", "sumofsubsets"
        ]
        for f in files:
            print(f"  🔹 {f}")
        return

    filename = sys.argv[1].strip().lower()
    show_file_content(filename)
