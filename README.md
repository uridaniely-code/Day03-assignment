# Day 03: Star temperature and luminosity

This assignment uses a Jupyter notebook to read a star catalogue, estimate stellar distances, luminosities, and temperatures, and plot the results on a Hertzsprung-Russell-style diagram.

## Files and requirements

- `stars_analysis.ipynb` - the step-by-step analysis and plot.
- `ASTRM402_data.csv` - the input data, with 9,171 rows and the columns `id`, `ra_deg`, `dec_deg`, `parallax_arcsec`, `flux_Lsuncm2`, and `peakLam_m`.

The notebook uses Python with `pandas`, `numpy`, and `matplotlib`. In VS Code, select a Python Jupyter kernel with these packages installed, then run the notebook from top to bottom. The file lookup supports running Jupyter either from this folder or from its parent folder.

## How the program was developed

The notebook was built incrementally from the requested data analysis and visualization:

1. Load the CSV and inspect its row count, columns, and sample records.
2. Check that the expected columns exist and convert measurement columns to numeric values.
3. Validate measurements before applying formulas. Nonpositive parallax, flux, or wavelength values stop the calculation. Rows with missing numeric measurements are reported and excluded because their derived quantities cannot be calculated.
4. Calculate distance, luminosity, and temperature, then show a summary and sample of the derived values.
5. Draw a Hertzsprung-Russell-style scatter plot, and refine its appearance and reference annotations in response to follow-up requests.

The dataset has 40 missing `peakLam_m` values, so 9,131 stars are used for temperature, luminosity, and the plot. The notebook reports the missing values and example IDs when it runs.

## Formulas and assumptions

### Distance from parallax

For parallax `p` in arcseconds:

```text
d_pc = 1 / p
```

This is the standard inverse-parallax estimate of distance in parsecs. It does not account for measurement uncertainty or bias in low-quality parallax measurements.

The distance is converted to centimeters for the luminosity calculation:

```text
d_cm = d_pc * 3.085677581e18 cm/pc
```

### Luminosity from flux

Assuming the `flux_Lsuncm2` values are measured in solar luminosities per square centimeter, the inverse-square relation for isotropic emission gives:

```text
L_Lsun = 4 * pi * d_cm^2 * flux_Lsuncm2
```

The result is luminosity in solar units (`L_sun`). This calculation depends on the flux unit interpretation indicated by the column name; verify the dataset documentation if its units are defined differently.

### Temperature from peak wavelength

The notebook estimates effective temperature using Wien's displacement law:

```text
T_K = 2.897771955e-3 m K / peakLam_m
```

`peakLam_m` is assumed to be the peak wavelength in meters. This is a blackbody-based estimate, not a direct temperature measurement.

## Diagram and star-class guide

The plot places estimated temperature (K) on the horizontal axis and luminosity (`L_sun`) on the vertical axis. The temperature axis is reversed so hotter stars appear on the left. The luminosity axis is logarithmic so faint and bright stars can be shown together. The chart has a black background and uses a red-white-blue temperature color scale, from red for cooler stars through white to blue for hotter stars.

Translucent labels show approximate regions for red giants, blue giants, and white dwarfs. These are visual guide areas, not precise boundaries or classifications; real stars do not fall into exact rectangular regions. The Sun is marked separately at approximately 5,778 K and 1 `L_sun`.

The chart currently shows 2,500 to 15,000 K and `10^-4` to `10^4 L_sun`. As a result, portions of the blue-giant guide and other stars outside these limits will not appear.

## Prompts used during development

The notebook was developed through these prompts and follow-up changes:

1. **Initial request:** "In the root of folder Day03-assignment start building a code in jupyter's notebook with a clear explanation between steps. The code will write a program that will get a dataset of stars with the headers `id`, `ra_deg`, `dec_deg`, `parallax_arcsec`, `flux_Lsuncm2`, `peakLam_m`. It will eventually calculate temperature and luminosity and will order the stars on a plot."
2. **Temperature colors:** "I want the spectrum of temperature to be from red (cold) to white to blue (hot)."
3. **Plot background:** "The background should be black."
4. **Classification regions and Sun:** "How can we add in code the areas where red giants are, the areas where blue giants are, where white dwarves are and also mark our sun specifically?"
5. **Plot limits:** "Can the diagram go back to order it was? Shorten the zone it reaches to 15000 degree kelvin and to 10^4 luminosity."

## Website reference

The astronomy reference used for the diagram is ESA's [Gaia Hertzsprung-Russell diagram](https://sci.esa.int/web/gaia/-/60198-gaia-hertzsprung-russell-diagram). The page explains the HR diagram as a way to compare stellar color/temperature with brightness, and describes features such as the main sequence, red-giant branch, and white-dwarf region. It also explains why hotter, bluer stars are conventionally placed on the left.

The linked page discusses a diagram based on Gaia's second data release (DR2). The notebook plots the supplied local CSV and uses the ESA page as an astronomy and diagram reference; this README does not claim that the CSV was downloaded from that page.

## Other files in this folder

- `ASTRM402_data.csv` - the input star catalogue.
- `star.py` - Python script that generates the decorative `star.svg` image.
- `star.svg` - generated star illustration.
- `solar_system.py` - Python script that generates the solar-system illustration.
- `solar_system.svg` - generated solar-system illustration.
