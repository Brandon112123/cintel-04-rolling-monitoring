"""
rolling_monitor_custom.py - Project script (custom).

Author: Brandon Smith
Date: 2026-04

Time-Series Weather Data

- Data is taken from a weather dataset that records temperature over time.
- Each row represents one observation at a specific date.
- The CSV file includes these columns:
  - Date: when the observation occurred
  - Temperature: daily temperature value

Purpose

- Read time-series weather data from a CSV file.
- Demonstrate rolling monitoring using a moving window.
- Compute rolling averages to smooth short-term variation.
- Save the resulting monitoring signals as a CSV artifact.
- Create and save a chart as a visual artifact.
- Log the pipeline process to assist with debugging and transparency.

Questions to Consider

- How does temperature change over time?
- Why might a rolling average reveal patterns that individual observations hide?
- How can smoothing short-term variation help us understand longer-term trends?

Paths (relative to repo root)

    INPUT FILE: data/daily_max_temperatures.csv
    OUTPUT FILE: artifacts/rolling_weather_metrics.csv
    CHART FILE: artifacts/rolling_weather_metrics.png

Terminal command to run this file from the root project folder

    uv run python -m cintel.rolling_monitor_custom
"""

# === DECLARE IMPORTS ===

import logging
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import polars as pl
from datafun_toolkit.logger import get_logger, log_header, log_path

# === CONFIGURE LOGGER ===

LOG: logging.Logger = get_logger("P5", level="DEBUG")

# === DEFINE GLOBAL PATHS ===

ROOT_DIR: Final[Path] = Path.cwd()
DATA_DIR: Final[Path] = ROOT_DIR / "data"
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"

DATA_FILE: Final[Path] = DATA_DIR / "daily_max_temperatures.csv"
OUTPUT_FILE: Final[Path] = ARTIFACTS_DIR / "rolling_weather_metrics.csv"
CHART_FILE: Final[Path] = ARTIFACTS_DIR / "rolling_weather_metrics.png"

# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Run the pipeline.

    log_header() logs a standard run header.
    log_path() logs repo-relative paths (privacy-safe).
    """
    log_header(LOG, "CINTEL")

    LOG.info("========================")
    LOG.info("START main()")
    LOG.info("========================")

    log_path(LOG, "ROOT_DIR", ROOT_DIR)
    log_path(LOG, "DATA_FILE", DATA_FILE)
    log_path(LOG, "OUTPUT_FILE", OUTPUT_FILE)
    log_path(LOG, "CHART_FILE", CHART_FILE)

    # Ensure artifacts directory exists
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    log_path(LOG, "ARTIFACTS_DIR", ARTIFACTS_DIR)

    # ----------------------------------------------------
    # STEP 1: READ CSV DATA FILE INTO A POLARS DATAFRAME
    # ----------------------------------------------------
    df = pl.read_csv(DATA_FILE)

    LOG.info(f"Loaded {df.height} time-series records")

    # ----------------------------------------------------
    # STEP 2: SORT DATA BY DATE
    # ----------------------------------------------------
    df = df.sort("Date")

    LOG.info("Sorted records by Date")

    # ----------------------------------------------------
    # STEP 3: DEFINE ROLLING WINDOW RECIPE
    # ----------------------------------------------------
    WINDOW_SIZE: int = 9

    # ----------------------------------------------------
    # STEP 3.1: DEFINE ROLLING MEAN FOR TEMPERATURE
    # ----------------------------------------------------
    temperature_rolling_mean_recipe: pl.Expr = (
        pl.col("Temperature")
        .rolling_mean(WINDOW_SIZE)
        .alias("temperature_rolling_mean")
    )

    # ----------------------------------------------------
    # STEP 3.2: APPLY THE ROLLING RECIPE
    # ----------------------------------------------------
    df_with_rolling = df.with_columns(
        [
            temperature_rolling_mean_recipe,
        ]
    )

    LOG.info("Computed rolling mean signals")

    # ----------------------------------------------------
    # STEP 4: SAVE RESULTS AS A CSV ARTIFACT
    # ----------------------------------------------------
    df_with_rolling.write_csv(OUTPUT_FILE)
    LOG.info(f"Wrote rolling monitoring file: {OUTPUT_FILE}")

    # ----------------------------------------------------
    # STEP 5: CREATE AND SAVE CHART
    # ----------------------------------------------------
    temperatures = df_with_rolling["Temperature"].to_list()
    rolling_means = df_with_rolling["temperature_rolling_mean"].to_list()

    plt.figure(figsize=(12, 6))
    plt.plot(temperatures, label="Daily Temperature")
    plt.plot(rolling_means, label="Temperature Rolling Mean")
    plt.title("Daily Temperature vs Rolling Mean")
    plt.xlabel("Observation")
    plt.ylabel("Temperature")
    plt.legend()
    plt.savefig(CHART_FILE, bbox_inches="tight")
    plt.close()

    LOG.info(f"Wrote chart file: {CHART_FILE}")

    LOG.info("========================")
    LOG.info("Pipeline executed successfully!")
    LOG.info("========================")
    LOG.info("END main()")


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    main()
