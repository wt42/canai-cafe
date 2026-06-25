"""
Run complete cleaning and profiling pipeline.

Run from project root:
    python scripts/run_all.py
"""

from dataset_cleaner import main as clean_main
from dataset_profiler import main as profile_main


if __name__ == "__main__":
    clean_main()
    print("\n" + "-" * 90 + "\n")
    profile_main()
