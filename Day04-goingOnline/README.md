# Day 04: Going online

A Flask web app that plots user-provided stellar temperature and luminosity on the Day 03 Hertzsprung–Russell-style diagram and compares them with the supplied star catalog.

## Run locally

From this folder, install the dependencies and start the app:

```powershell
cd /d "C:\Users\erezd\OneDrive\שולחן העבודה\אוניברסיטה\תואר שני\קורסים\Python programming with AI\Day03-assignment\Day04-goingOnline"
python -m pip install -r requirements.txt
python app.py
```

Open the local address printed by Flask (usually `http://127.0.0.1:5000`).

## Input ranges and comparison

The form accepts temperatures from **2,500 to 15,000 K** and asks for the **whole-number exponent** in the luminosity `10^exponent L☉`, from **−4 to 4**. For example, enter `-2` for `10⁻² L☉`. The app converts the exponent to luminosity before plotting and comparing; both ranges are checked by the server.

The app loads `ASTRM402_data.csv` from the parent `Day03-assignment` folder. As in the notebook, it derives luminosity from inverse-square flux and distance and estimates temperature from Wien’s displacement law. Rows missing required values or having nonpositive measurements are excluded.

The submitted point and the closest visible catalog sample are marked on the diagram. The closest sample is selected using normalized diagram coordinates (linear temperature and logarithmic luminosity); the result also reports each measurement’s percentage difference. This indicates similarity to the supplied catalog, not whether a star is genuine.
