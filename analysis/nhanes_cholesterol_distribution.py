import io
import sys
import os
import math
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import re
from typing import Optional, List

# Output locations
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)
CSV_PATH = os.path.join(OUTPUT_DIR, "cholesterol_distribution_males_40_60_2021_2023.csv")
PNG_PATH = os.path.join(OUTPUT_DIR, "cholesterol_distribution_males_40_60_2021_2023.png")

# Known candidate URLs for NHANES 2021-2023 XPT files
TCHOL_URLS = [
    # Direct file patterns (may change)
    "https://wwwn.cdc.gov/Nchs/Nhanes/2021-2023/TCHOL_L.XPT",
    "https://wwwn.cdc.gov/nchs/nhanes/2021-2023/TCHOL_L.XPT",
    "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/xptfiles/TCHOL_L.XPT",
    # Official handler
    "https://wwwn.cdc.gov/Nchs/Nhanes/Download/DataFile.aspx?FileName=TCHOL_L&CycleBeginYear=2021",
    # Documentation page (we will parse to find the XPT link)
    "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/TCHOL_L.htm",
]
DEMO_URLS = [
    # Direct file patterns (may change)
    "https://wwwn.cdc.gov/Nchs/Nhanes/2021-2023/DEMO_L.XPT",
    "https://wwwn.cdc.gov/nchs/nhanes/2021-2023/DEMO_L.XPT",
    "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/xptfiles/DEMO_L.XPT",
    # Official handler
    "https://wwwn.cdc.gov/Nchs/Nhanes/Download/DataFile.aspx?FileName=DEMO_L&CycleBeginYear=2021",
    # Documentation page (we will parse to find the XPT link)
    "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.htm",
]


def discover_xpt_from_doc(doc_url: str) -> Optional[str]:
    """Attempt to discover the XPT file URL by parsing the CDC documentation page.
    Returns the discovered URL or None if not found.
    """
    try:
        print(f"Parsing documentation page for XPT link: {doc_url}")
        resp = requests.get(doc_url, timeout=60, headers={"User-Agent": "nhanes-downloader/1.0"})
        resp.raise_for_status()
        html = resp.text
        # Find hrefs ending with .XPT (case-insensitive)
        candidates = re.findall(r'href\s*=\s*\"([^\"]+\.XPT)\"', html, flags=re.IGNORECASE)
        if not candidates:
            candidates = re.findall(r'href\s*=\s*\'([^\']+\.XPT)\'', html, flags=re.IGNORECASE)
        for href in candidates:
            # Resolve relative URLs
            if href.startswith("http"):
                url = href
            else:
                url = requests.compat.urljoin(doc_url, href)
            print(f"Discovered XPT link: {url}")
            # quick HEAD/GET to validate
            try:
                r2 = requests.get(url, timeout=60, headers={"User-Agent": "nhanes-downloader/1.0"})
                if r2.ok and r2.content[:4] != b"<htm":
                    return url
            except Exception:
                pass
        return None
    except Exception as e:
        print(f"Failed to parse doc page: {e}")
        return None


def fetch_xpt_as_dataframe(urls: list, label: str) -> pd.DataFrame:
    last_err = None
    # Local fallback: look under project/data
    here = os.path.dirname(os.path.dirname(__file__))
    local_dir = os.path.join(here, "data")
    local_name = f"{label}.XPT" if label.endswith("_L") else f"{label}.XPT"
    local_path = os.path.join(local_dir, local_name)
    if os.path.exists(local_path):
        try:
            print(f"Loading {label} from local file: {local_path}")
            with open(local_path, "rb") as f:
                df = pd.read_sas(io.BytesIO(f.read()), format="xport")
            print(f"Loaded {label} locally: {df.shape[0]} rows, {df.shape[1]} cols")
            return df
        except Exception as e:
            last_err = e
            print(f"Failed to load local {label}: {e}")
    for url in urls:
        try:
            print(f"Downloading {label} from: {url}")
            if url.lower().endswith(".htm") or "DataFile.aspx" in url:
                discovered = discover_xpt_from_doc(url)
                if not discovered:
                    raise RuntimeError("Could not discover XPT link from documentation page")
                url = discovered
                print(f"Resolved {label} XPT to: {url}")
            resp = requests.get(url, timeout=120, headers=UA, allow_redirects=True)
            resp.raise_for_status()
            # Skip if HTML
            ctype = resp.headers.get("Content-Type", "").lower()
            if resp.content[:4].lower() == b"<htm" or "text/html" in ctype:
                # try to discover from this page directly
                alt = discover_xpt_from_doc(url)
                if alt:
                    resp = requests.get(alt, timeout=120, headers=UA, allow_redirects=True)
                    resp.raise_for_status()
                else:
                    # last resort: try without SSL verification
                    resp = requests.get(url, timeout=120, headers=UA, verify=False, allow_redirects=True)
                    if resp.content[:4].lower() == b"<htm" or "text/html" in resp.headers.get("Content-Type", "").lower():
                        raise RuntimeError("Got HTML instead of XPT")
            df = pd.read_sas(io.BytesIO(resp.content), format="xport")
            print(f"Loaded {label}: {df.shape[0]} rows, {df.shape[1]} cols")
            return df
        except Exception as e:
            last_err = e
            print(f"Failed {label} URL {url}: {e}")
    raise RuntimeError(f"All download attempts failed for {label}. Last error: {last_err}")


def main():
    # Load total cholesterol and demographics
    tch_df = fetch_xpt_as_dataframe(TCHOL_URLS, "TCHOL_L")
    demo_df = fetch_xpt_as_dataframe(DEMO_URLS, "DEMO_L")

    # Ensure required columns exist
    required_tch = {"SEQN", "LBXTC", "WTPH2YR"}
    required_demo = {"SEQN", "RIDAGEYR", "RIAGENDR"}
    if not required_tch.issubset(tch_df.columns):
        missing = required_tch - set(tch_df.columns)
        raise KeyError(f"TCHOL_L missing columns: {missing}")
    if not required_demo.issubset(demo_df.columns):
        missing = required_demo - set(demo_df.columns)
        raise KeyError(f"DEMO_L missing columns: {missing}")

    # Merge
    df = pd.merge(tch_df[["SEQN", "LBXTC", "WTPH2YR"]],
                  demo_df[["SEQN", "RIDAGEYR", "RIAGENDR"]],
                  on="SEQN", how="inner")

    # Filter: males (RIAGENDR == 1), age 40-60 inclusive, valid cholesterol and positive weights
    df = df[(df["RIAGENDR"] == 1) &
            (df["RIDAGEYR"].between(40, 60, inclusive="both")) &
            (df["LBXTC"].notna()) & (df["LBXTC"] > 0) &
            (df["WTPH2YR"].notna()) & (df["WTPH2YR"] > 0)]

    if df.empty:
        raise ValueError("No records after filtering. Check data files and filters.")

    # Binning: x-axis from 50 to 400 with step 5. Use 5 mg/dL bins centered at these values.
    midpoints = np.arange(50, 401, 5, dtype=float)
    edges = np.arange(47.5, 402.6, 5.0, dtype=float)  # ensures midpoints between edges

    weights = df["WTPH2YR"].to_numpy()
    tc = df["LBXTC"].to_numpy()

    # Weighted histogram and convert to percentage of population
    hist_counts, _ = np.histogram(tc, bins=edges, weights=weights)
    total_weight = weights.sum()
    if total_weight <= 0:
        raise ValueError("Sum of weights is non-positive.")
    perc = (hist_counts / total_weight) * 100.0

    out_df = pd.DataFrame({
        "cholesterol_level": midpoints,
        "population_perc": perc,
    })

    # Save CSV
    out_df.to_csv(CSV_PATH, index=False)
    print(f"Saved CSV -> {CSV_PATH}")

    # Plot
    plt.figure(figsize=(10, 6), dpi=150)
    plt.plot(midpoints, perc, color="#2F4F4F", linewidth=2)
    plt.fill_between(midpoints, 0, perc, color="#2F4F4F", alpha=0.15)
    plt.xlabel("Total cholesterol (mg/dL)")
    plt.ylabel("Population (%)")
    plt.title("NHANES 2021–2023: Distribution of Total Cholesterol\nMales age 40–60 (weighted with WTPH2YR)")
    plt.xlim(50, 400)
    plt.xticks(np.arange(50, 401, 25))
    plt.grid(axis="y", linestyle=":", alpha=0.5)

    # Arrow pointing to 184 mg/dL
    x_arrow = 184.0
    # Find bin index containing x_arrow
    idx = int(np.clip(np.digitize([x_arrow], edges)[0] - 1, 0, len(midpoints) - 1))
    y_arrow = perc[idx]
    plt.scatter([x_arrow], [y_arrow], color="#C0392B", zorder=5)
    plt.annotate(
        "184 mg/dL",
        xy=(x_arrow, y_arrow),
        xytext=(x_arrow + 25, y_arrow + max(perc) * 0.08),
        arrowprops=dict(arrowstyle="->", color="#C0392B", lw=2),
        color="#C0392B",
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#C0392B", alpha=0.7),
    )

    plt.tight_layout()
    plt.savefig(PNG_PATH)
    print(f"Saved plot -> {PNG_PATH}")


if __name__ == "__main__":
    main()
