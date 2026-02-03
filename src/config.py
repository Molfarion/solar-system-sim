from datetime import datetime

# Window / display
WIDTH = 1200
HEIGHT = 800


# Simulation time step (seconds of simulation time per integration step)
DEFAULT_DELTATIME = 43200.0  # 12 hours

# Physics / integration
SUBSTEPS = 15  # Integration substeps per frame for stability

# Visuals
STAR_COUNT = 40  # Number of background stars to generate

# Simulation epoch (matches initial conditions scripts)
SIM_EPOCH = datetime(2025, 1, 1)

