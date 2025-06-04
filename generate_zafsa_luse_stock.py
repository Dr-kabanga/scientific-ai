import os
import pandas as pd
import numpy as np


def generate_luse_data(start_date: str, end_date: str, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic LUSE stock market data."""
    np.random.seed(seed)
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    price = 100.0
    records = []

    for dt in dates:
        open_p = price * (1 + np.random.normal(0, 0.01))
        close_p = open_p * (1 + np.random.normal(0, 0.01))
        high_p = max(open_p, close_p) * (1 + np.random.uniform(0, 0.02))
        low_p = min(open_p, close_p) * (1 - np.random.uniform(0, 0.02))
        volume = np.random.randint(1000, 10000)
        price = close_p
        records.append({
            "date": dt.date(),
            "open": round(open_p, 2),
            "high": round(high_p, 2),
            "low": round(low_p, 2),
            "close": round(close_p, 2),
            "volume": volume,
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = generate_luse_data("2024-01-01", "2024-12-31")
    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "zafsa_luse_stock_data.csv")
    df.to_csv(output_path, index=False)
    print(f"Synthetic LUSE stock data saved to {output_path}")
