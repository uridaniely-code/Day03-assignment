# Day 04: Going online

A Flask web app that plots user-provided stellar temperature and luminosity on the Day 03 Hertzsprung–Russell-style diagram and compares them with the supplied star catalog.

## Run locally

From this folder, install the dependencies and start the app:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open the local address printed by Flask (usually `http://127.0.0.1:5000`).

## Input ranges and comparison

The form accepts temperatures from **2,500 to 15,000 K** and luminosities from **10⁻⁴ to 10⁴ L☉**, matching the existing diagram axes. Both ranges are also checked by the server.

The app loads `ASTRM402_data.csv` from the parent `Day03-assignment` folder. As in the notebook, it derives luminosity from inverse-square flux and distance and estimates temperature from Wien’s displacement law. Rows missing required values or having nonpositive measurements are excluded.

The submitted point and the closest visible catalog sample are marked on the diagram. The closest sample is selected using normalized diagram coordinates (linear temperature and logarithmic luminosity); the result also reports each measurement’s percentage difference. This indicates similarity to the supplied catalog, not whether a star is genuine.
