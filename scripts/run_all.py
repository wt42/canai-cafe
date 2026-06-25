"""
Run complete cleaning and profiling pipeline.

Run from project root:
    python scripts/run_all.py
"""

from dataset_cleaner import main as clean_main
from dataset_profiler import main as profile_main
from generate_dashboard_data import main as dashboard_main


if __name__ == "__main__":
    clean_main()
    print("\n" + "-" * 90 + "\n")
    profile_main()
    print("\n" + "-" * 90 + "\n")
    dashboard_main()
