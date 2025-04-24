from setuptools import setup, find_packages

setup(
    name='aoa_code_mypack',
    version='0.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "show-aoa-codes=aoa_code_mypack.main:cli",
        ],
    },
    package_data={
        "aoa_code_mypack": [
            "codes.txt",
            "binarysearch.txt",
            "dijkstra.txt",
            "floydwarshall.txt",
            "greedy.txt",
            "insertionsort.txt",
            "knapsack.txt",
            "mergesort.txt",
            "nqueens.txt",
            "prims.txt",
            "quicksort.txt",
            "rabincarp.txt",
            "selectionsort.txt",
            "sumofsubsets.txt"
        ],
    },
)
