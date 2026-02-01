## Solar System Simulation

A 2D N-body simulation of the Solar System with planets and selected moons, using pygame.

### Install

From the project root:

```bash
pip install -r requirements.txt
```

- **Simulation:** `numpy`, `pandas`, `pygame`
- **Scripts (optional):** `astroquery` — used to fetch initial conditions from JPL Horizons

### Run

From the project root:

```bash
python src/main.py
```

The app finds `data/initial_planets.csv` and `data/moons_vectors.csv` relative to the project directory, so it works whether you run from the project root or from `src/`.

### Regenerating data (optional)

To refresh positions/velocities from NASA JPL Horizons (requires network and `astroquery`):

```bash
python scripts/get_initial_conditions.py   # writes data/initial_planets.csv
python scripts/get_init_cond_moons.py      # writes data/moons_vectors.csv
```

Note: `get_initial_conditions.py` outputs columns that may differ from the current CSV format; you may need to add `color_r`, `color_g`, `color_b` and `radius` manually or adjust the script to match `data/initial_planets.csv`.

---

## Data Sources

- Planetary positions and velocities were obtained from NASA's [JPL Horizons system](https://ssd.jpl.nasa.gov/horizons.cgi).
- Masses and other physical parameters are from publicly available NASA data.