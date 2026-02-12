"""Download NYC listing data from Inside Airbnb."""

import os
import subprocess

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

URLS = {
    "2025-12": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-12-04/data/listings.csv.gz",
    "2025-11": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-11-01/data/listings.csv.gz",
    "2025-10": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-10-01/data/listings.csv.gz",
    "2025-09": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-09-01/data/listings.csv.gz",
    "2025-08": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-08-01/data/listings.csv.gz",
    "2025-07": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-07-01/data/listings.csv.gz",
    "2025-06": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-06-17/data/listings.csv.gz",
    "2025-05": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-05-01/data/listings.csv.gz",
    "2025-04": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-04-01/data/listings.csv.gz",
    "2025-03": "https://data.insideairbnb.com/united-states/ny/new-york-city/2025-03-01/data/listings.csv.gz",
}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    for month, url in URLS.items():
        filename = f"listings_{month}.csv.gz"
        output_path = os.path.join(DATA_DIR, filename)
        print(f"Downloading {filename}...")
        subprocess.run(["wget", "-c", url, "-O", output_path], check=True)
        print(f"  Saved to {output_path}")

    print("All downloads complete.")


if __name__ == "__main__":
    main()
