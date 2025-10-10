## Inputs and results of codes participating in the first CHILI protocols paper

This directory contains the results of the first protocol results developed in the first CHILI protocol paper.

## Output format

### Evolution models
Output data is saved as CSV files in this format

| time (yr) | Tsurf (K) | pH2O (bar) | phi (vol_frac) |
|-----------|-----------|------------|----------------|
| ...       | ...       | ...        | ...            |
| ...       | ...       | ...        | ...            |

with

- ```time (yr)```: Time in years
- ```Tsurf (K)```: Surface temperature in K
- ```pH2O (bar)```: Partial pressure of water in the atmosphere
- ```phi (vol_frac)```: Mantle total volume fraction of melt

### Static models

## Directory structure

Each model has its own directory in ``inputs`` and ``outputs`` to store input files and outputs.
Each model should adhere to the following structure:
```
inputs/
├── model1/
│   └── <input file 1>
│   └── <input file 2>
│   └── ...
├── model2/
│   └── <input file 1>
│   └── ...
outputs/
├── model1/
│   └── model1-earth.csv
│   └── model1-trappist1b.csv
├── model2/
│   └── model2-earth.csv
│   └── model2-trappist1b.csv
```

The output files should all be named as ``<model_name>-earth.csv`` or ``<model_name>-trappist1b.csv``.
