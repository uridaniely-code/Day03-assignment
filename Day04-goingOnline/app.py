from __future__ import annotations

import base64
from io import BytesIO
from math import isfinite, log10
from pathlib import Path
from typing import Mapping

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from matplotlib.colors import LinearSegmentedColormap, Normalize


TEMPERATURE_MIN_K = 2_500
TEMPERATURE_MAX_K = 15_000
LUMINOSITY_MIN_LSUN = 1e-4
LUMINOSITY_MAX_LSUN = 1e4
LUMINOSITY_EXPONENT_MIN = -4
LUMINOSITY_EXPONENT_MAX = 4
PARSEC_TO_CM = 3.085677581e18
WIEN_DISPLACEMENT_M_K = 2.897771955e-3
DATA_PATH = Path(__file__).resolve().parent.parent / "ASTRM402_data.csv"

app = Flask(__name__)


def load_catalog() -> pd.DataFrame:
    """Load valid catalog measurements and derive temperature and luminosity."""
    stars = pd.read_csv(DATA_PATH)
    required_columns = {"id", "parallax_arcsec", "flux_Lsuncm2", "peakLam_m"}
    missing_columns = required_columns.difference(stars.columns)
    if missing_columns:
        raise ValueError(f"Catalog is missing required columns: {', '.join(sorted(missing_columns))}")

    for column in ("parallax_arcsec", "flux_Lsuncm2", "peakLam_m"):
        stars[column] = pd.to_numeric(stars[column], errors="coerce")

    stars = stars.dropna(subset=["parallax_arcsec", "flux_Lsuncm2", "peakLam_m"])
    stars = stars[
        (stars["parallax_arcsec"] > 0)
        & (stars["flux_Lsuncm2"] > 0)
        & (stars["peakLam_m"] > 0)
    ].copy()

    stars["distance_pc"] = 1 / stars["parallax_arcsec"]
    stars["distance_cm"] = stars["distance_pc"] * PARSEC_TO_CM
    stars["luminosity_Lsun"] = (
        4 * np.pi * stars["distance_cm"] ** 2 * stars["flux_Lsuncm2"]
    )
    stars["temperature_K"] = WIEN_DISPLACEMENT_M_K / stars["peakLam_m"]
    stars = stars.replace([np.inf, -np.inf], np.nan)
    stars = stars.dropna(subset=["temperature_K", "luminosity_Lsun"])
    stars = stars[
        (stars["luminosity_Lsun"] > 0)
        & (stars["temperature_K"] > 0)
    ].copy()
    return stars


CATALOG = load_catalog()
VISIBLE_CATALOG = CATALOG[
    CATALOG["temperature_K"].between(TEMPERATURE_MIN_K, TEMPERATURE_MAX_K)
    & CATALOG["luminosity_Lsun"].between(LUMINOSITY_MIN_LSUN, LUMINOSITY_MAX_LSUN)
].copy()


def closest_catalog_star(temperature_K: float, luminosity_Lsun: float) -> pd.Series:
    """Find the nearest plotted catalog star in normalized diagram coordinates."""
    temperature_distance = (
        (VISIBLE_CATALOG["temperature_K"] - temperature_K)
        / (TEMPERATURE_MAX_K - TEMPERATURE_MIN_K)
    )
    luminosity_distance = (
        np.log10(VISIBLE_CATALOG["luminosity_Lsun"] / luminosity_Lsun)
        / log10(LUMINOSITY_MAX_LSUN / LUMINOSITY_MIN_LSUN)
    )
    distances = np.hypot(temperature_distance, luminosity_distance)
    closest_index = distances.idxmin()
    return VISIBLE_CATALOG.loc[closest_index]


def create_hr_diagram(temperature_K: float, luminosity_Lsun: float, closest_index: int) -> str:
    """Render the catalog, the user's submitted point, and its closest catalog match."""
    ordered_stars = VISIBLE_CATALOG.sort_values("temperature_K")
    temperature_cmap = LinearSegmentedColormap.from_list(
        "cold_to_hot", ["red", "white", "blue"]
    )

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.set_yscale("log")
    ax.set_xlim(TEMPERATURE_MAX_K, TEMPERATURE_MIN_K)
    ax.set_ylim(LUMINOSITY_MIN_LSUN, LUMINOSITY_MAX_LSUN)

    regions = [
        ("Red giants", (2_500, 5_000), (10, 1e3), "red"),
        ("Blue giants", (10_000, 15_000), (1e2, 1e4), "blue"),
        ("White dwarfs", (5_000, 15_000), (1e-4, 1e-1), "white"),
    ]
    for name, temperature_range, luminosity_range, color in regions:
        temp_min, temp_max = temperature_range
        luminosity_min, luminosity_max = luminosity_range
        ax.add_patch(
            plt.Rectangle(
                (temp_min, luminosity_min),
                temp_max - temp_min,
                luminosity_max - luminosity_min,
                facecolor=color,
                edgecolor=color,
                alpha=0.12,
                linewidth=1.5,
                zorder=1,
            )
        )
        ax.text(
            (temp_min + temp_max) / 2,
            np.sqrt(luminosity_min * luminosity_max),
            name,
            color=color,
            ha="center",
            va="center",
            fontsize=10,
            weight="bold",
            zorder=4,
        )

    points = ax.scatter(
        ordered_stars["temperature_K"],
        ordered_stars["luminosity_Lsun"],
        c=ordered_stars["temperature_K"],
        cmap=temperature_cmap,
        norm=Normalize(TEMPERATURE_MIN_K, TEMPERATURE_MAX_K),
        s=18,
        alpha=0.75,
        edgecolors="none",
        zorder=3,
        label="Catalog stars",
    )
    closest = VISIBLE_CATALOG.loc[closest_index]
    ax.scatter(
        closest["temperature_K"],
        closest["luminosity_Lsun"],
        marker="o",
        s=110,
        facecolors="none",
        edgecolors="#ffd166",
        linewidths=2,
        zorder=5,
        label="Closest catalog star",
    )
    ax.scatter(
        5778,
        1.0,
        marker="*",
        s=220,
        color="gold",
        edgecolors="black",
        linewidths=0.8,
        zorder=6,
        label="Our Sun",
    )
    ax.scatter(
        temperature_K,
        luminosity_Lsun,
        marker="D",
        s=100,
        color="#ff4fd8",
        edgecolors="white",
        linewidths=1,
        zorder=7,
        label="Your star",
    )
    ax.set_xlabel("Estimated surface temperature (K)", color="white")
    ax.set_ylabel("Luminosity (L$_\\odot$)", color="white")
    ax.set_title("Stars by temperature and luminosity", color="white")
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("white")
    ax.grid(True, which="both", linestyle=":", color="gray", alpha=0.4)
    legend = ax.legend(facecolor="#102a43", edgecolor="white", labelcolor="white")
    for text in legend.get_texts():
        text.set_color("white")
    colorbar = fig.colorbar(points, ax=ax)
    colorbar.set_label("Temperature (K)", color="white")
    colorbar.ax.tick_params(colors="white")
    colorbar.outline.set_edgecolor("white")
    fig.tight_layout()

    image = BytesIO()
    fig.savefig(image, format="png", dpi=130, facecolor=fig.get_facecolor())
    plt.close(fig)
    return base64.b64encode(image.getvalue()).decode("ascii")


def parse_measurements(form: Mapping[str, str]) -> tuple[float, float]:
    """Parse measurements and convert the submitted luminosity exponent to L☉."""
    temperature_raw = form.get("temperature_K", "").strip()
    luminosity_exponent_raw = form.get("luminosity_exponent", "").strip()
    if not temperature_raw or not luminosity_exponent_raw:
        raise ValueError("Enter both temperature and luminosity.")
    try:
        temperature_K = float(temperature_raw)
        luminosity_exponent = int(luminosity_exponent_raw)
    except ValueError as exc:
        raise ValueError("Enter a numeric temperature and a whole-number luminosity exponent.") from exc

    if not isfinite(temperature_K) or not TEMPERATURE_MIN_K <= temperature_K <= TEMPERATURE_MAX_K:
        raise ValueError(
            f"Temperature must be between {TEMPERATURE_MIN_K:,} and "
            f"{TEMPERATURE_MAX_K:,} K to appear on this diagram."
        )
    if not LUMINOSITY_EXPONENT_MIN <= luminosity_exponent <= LUMINOSITY_EXPONENT_MAX:
        raise ValueError(
            f"Luminosity exponent must be between {LUMINOSITY_EXPONENT_MIN} and "
            f"{LUMINOSITY_EXPONENT_MAX}."
        )
    return temperature_K, 10.0**luminosity_exponent


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None
    form_values = {"temperature_K": "", "luminosity_exponent": ""}

    if request.method == "POST":
        form_values = {
            "temperature_K": request.form.get("temperature_K", ""),
            "luminosity_exponent": request.form.get("luminosity_exponent", ""),
        }
        try:
            temperature_K, luminosity_Lsun = parse_measurements(request.form)
        except ValueError as exc:
            error = str(exc)
        else:
            closest = closest_catalog_star(temperature_K, luminosity_Lsun)
            result = {
                "temperature_K": temperature_K,
                "luminosity_Lsun": luminosity_Lsun,
                "closest_id": str(closest["id"]),
                "closest_temperature_K": float(closest["temperature_K"]),
                "closest_luminosity_Lsun": float(closest["luminosity_Lsun"]),
                "temperature_difference_percent": abs(
                    float(closest["temperature_K"]) - temperature_K
                )
                / temperature_K
                * 100,
                "luminosity_difference_percent": abs(
                    float(closest["luminosity_Lsun"]) - luminosity_Lsun
                )
                / luminosity_Lsun
                * 100,
                "diagram": create_hr_diagram(
                    temperature_K, luminosity_Lsun, int(closest.name)
                ),
                "catalog_size": len(VISIBLE_CATALOG),
            }

    return render_template(
        "index.html",
        error=error,
        result=result,
        form_values=form_values,
        temperature_min=TEMPERATURE_MIN_K,
        temperature_max=TEMPERATURE_MAX_K,
        luminosity_exponent_min=LUMINOSITY_EXPONENT_MIN,
        luminosity_exponent_max=LUMINOSITY_EXPONENT_MAX,
        catalog_size=len(VISIBLE_CATALOG),
    )


if __name__ == "__main__":
    app.run()
