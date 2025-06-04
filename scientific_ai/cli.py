import argparse
import numpy as np
import pandas as pd


def main():
    """Simple entry point for the Scientific AI CLI."""
    parser = argparse.ArgumentParser(description="Run a demo data analysis")
    parser.add_argument(
        "--samples", type=int, default=100, help="Number of random samples"
    )
    args = parser.parse_args()

    data = np.random.randn(args.samples)
    df = pd.DataFrame({"value": data})
    print(df.describe())


if __name__ == "__main__":
    main()
