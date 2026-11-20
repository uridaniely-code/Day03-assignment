# Day 05: Business-logic tests

This folder contains [test_star_business_logic.ipynb](./test_star_business_logic.ipynb), a Jupyter notebook that checks the calculations and input handling behind the Day 04 star app. It tests the underlying logic directly rather than checking web pages or HTML; the existing `test_app.py` covers those routes.

## What the tests check

- **Catalog calculations:** valid catalog measurements are converted to numeric values, then used to calculate distance from parallax, luminosity from flux and distance, and temperature from peak wavelength.
- **Invalid catalog rows:** missing, non-numeric, or nonpositive measurements are excluded, and a catalog missing required columns is reported as an error.
- **Measurement parsing:** valid temperatures and whole-number luminosity exponents are converted to kelvin and solar luminosities. Boundary values are accepted, while missing, malformed, non-finite, or out-of-range values are rejected.
- **Closest catalog star:** the selected sample is the closest one using the diagram's normalized coordinates: linear temperature and logarithmic luminosity.

The notebook uses a small in-memory catalog fixture for the catalog tests, so it does not edit the real CSV. Importing the app still loads its real catalog once, just as it does when the web app starts.

## Run the notebook

Install the packages listed in the parent folder's `requirements.txt` if needed. Open the notebook in VS Code or Jupyter and run all cells from top to bottom. The test cell prints a summary and raises an error if any test fails.

Alternatively, open a terminal in this folder and start Jupyter with:

```powershell
python -m notebook test_star_business_logic.ipynb
```
