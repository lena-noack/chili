import pandas as pd
import numpy as np
import os

Rearth = 6371e3
Mearth = 5.972e24

_colors = {
    # H rich
    "H2": "#008C01",
    "H2O": "#027FB1",
    "CH4": "#C720DD",
    # C rich
    "CO": "#D1AC02",
    # S rich
    "H2S": "#640deb",
    "S2": "#FF8FA1",
    "SO2": "#00008B",
    # O rich
    "OH": "#00ffd4",
    "CO2": "#D24901",
    "O2": "#00dcc6",
    # N rich
    "NO2": "#eb0076",
    "H2SO4": "#46eba4",
    "N2": "#870036",
    "NH3": "#675200",

    # volatile elements
    "H"  : "#11B587",
    "C"  : "#D20F01",
    "O"  : "#00ff00",
    "N"  : "#ffaa00",
    "S" :  "#ff22ff",
    "P" :  "#33ccff",
    "He" : "#30FF71",

    "p_surf(bar)": "#444444",
}
gas_list = list(_colors.keys())
chili_gases = ["H2O", "CO2", "H2", "CO", "CH4", "O2"]

for k in gas_list:
    _colors[f"p_{k}(bar)"] = _colors[k]

chili_models = {
    "gooey":     ("GOOEY","#d62728"),
    "neongooey": ("NEONGOOEY","#ff7086"),
    "proteus":   ("PROTEUS","#F0833B"),
    "pacman":    ("PACMAN","#0e6eff"),
    "lincs":     ("LINCS","#2ca02c"),
    "moai":      ("MOAI","#9C028C"),
    "planatmo":  ("PlanAtMO","#8E8823"),
}

def get_color(thing:str):
    if thing in chili_models:
        return chili_models[thing][1]
    elif thing in _colors:
        return _colors[thing]
    else:
        print(f"WARNING: Plotting color for '{thing}' not defined")
        return "#222222"

def latexify(s:str):
    l = ""
    for c in s:
        if c.isnumeric():
            l += r"$_{" + c + "}$"
        else:
            l += c
    return l

_labels = {
"t(yr)":           "Model time [yr]" ,
"T_surf(K)":        r"$T_{\rm surf}$ [K]",
"T_pot(K)":         r"$T_{\rm pot}$ [K]",
"flux_surf(W/m2)":  r"$F_{\rm surf}$ [W m$^{-2}$]",
"flux_OLR(W/m2)":   r"$F_{\rm OLR}$ [W m$^{-2}$]",
"flux_ASR(W/m2)":   r"$F_{\rm ASR}$ [W m$^{-2}$]",
"phi(vol_frac)":    r"Melt volume fraction",
"phi(vol_pct)":     r"Melt fraction [vol%]",
"phi(mass_frac)":   r"Melt mass fraction",
"phi(mass_pct)":    r"Melt fraction [wt%]",
"fO2_solid(bar)":   r"$f_{\rm O2,solid}$ [bar]",
"fO2_melt(bar)":    r"$f_{\rm O2,melt}$ [bar]",
"thick_surf_bl(m)": r"$d_{\rm CBL}$ [m]",
"massC_solid(kg)":  r"$m_{\rm C,solid}$ [kg]",
"massC_melt(kg)":   r"$m_{\rm C,melt}$ [kg]",
"massC_atm(kg)":    r"$m_{\rm C,atm}$ [kg]",
"massH_solid(kg)":  r"$m_{\rm H,solid}$ [kg]",
"massH_melt(kg)":   r"$m_{\rm H,melt}$ [kg]",
"massH_atm(kg)":    r"$m_{\rm H,atm}$ [kg]",
"massO_atm(kg)":    r"$m_{\rm O,atm}$ [kg]",
"p_surf(bar)":      r"$p_{\rm surf}$ [bar]",
"p_H2O(bar)":       r"$p_{\rm H2O}$ [bar]",
"p_CO2(bar)":       r"$p_{\rm CO2}$ [bar]",
"p_CO(bar)":        r"$p_{\rm CO}$ [bar]",
"p_H2(bar)":        r"$p_{\rm H2}$ [bar]",
"p_CH4(bar)":       r"$p_{\rm CH4}$ [bar]",
"p_O2(bar)":        r"$p_{\rm O2}$ [bar]",
"p_N2(bar)":        r"$p_{\rm N2}$ [bar]",
"p_NH3(bar)":       r"$p_{\rm NH3}$ [bar]",
"p_S2(bar)":        r"$p_{\rm S2}$ [bar]",
"p_SO2(bar)":       r"$p_{\rm SO2}$ [bar]",
"p_H2S(bar)":       r"$p_{\rm H2S}$ [bar]",
"mmw(kg/mol)":      r"Outgassed MMW [kg/mol]",
"R_trans(m)":       r"$R_{\rm trans}$ [m]",
"R_solid(m)":       r"$R_{\rm solid}$ [m]",
"viscosity(Pa.s)":  r"Viscosity [Pa s]",

"earth": "Earth",
"venus": "Venus",
}

for k in gas_list:
    _labels[k] = latexify(k)

def get_label(thing:str):
    if thing in chili_models:
        return chili_models[thing][0]
    elif thing in _labels.keys():
        return _labels[thing]
    else:
        return thing

def list_planets():
    return ("earth", "venus")

def list_models():
    """List the available models in the outputs directory."""

    # expected models
    expected_models = list(chili_models.keys())

    # get output folders
    outputs_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    if not os.path.isdir(outputs_dir):
        raise FileNotFoundError(f"Outputs directory '{outputs_dir}' not found.")
    subdirs = os.listdir(outputs_dir)

    # check which expected models are present
    if set(expected_models) != set(subdirs):
        print(f"WARNING: Expected models do not match found models.")
        print(f"         Expected models: {expected_models}")
        print(f"         Found models: {subdirs}")

    # remove any expected models that are not found
    return [m for m in expected_models if m in subdirs]


def load_model_data(model:str, quiet=False):
    """Load the model data from the CSV file."""

    # check if model directory exists
    model = model.lower()
    model_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", model)
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"Model directory '{model_dir}' not found.")

    print("Loading model " + model)

    # load files for each planet
    model_data = {"earth":{}, "venus":{}}
    for planet in ["earth", "venus"]:
        quiet or print(f"    {planet}")

        # for nominal case
        f = os.path.join(model_dir,  f"evolution-{model}-{planet}-data.csv")
        if os.path.isfile(f):
            quiet or print("        nominal")
            model_data[planet]["nominal-evo"] = pd.read_csv(f)

        # for each H/C combination
        for Hk in ["Hhigh", "Hmid", "Hlow"]:
            for Ck in ["Chigh", "Cmid", "Clow"]:
                k = f"{Hk}-{Ck}"
                quiet or print(f"        {k}")

                # evolution data
                f = os.path.join(model_dir,  f"evolution-{model}-{planet}-grid-{Hk}-{Ck}-data.csv")
                if os.path.isfile(f):
                    model_data[planet][f"{k}-evo"] = pd.read_csv(f)

                else:
                    f = os.path.join(model_dir,  f"evolution-{model}-{planet}-grid-{Hk}-data.csv") # no carbon
                    if os.path.isfile(f):
                        model_data[planet][f"{k}-evo"] = pd.read_csv(f)

                # atmosphere profile data
                for tau in [1,2,3,4,5,6,7,8,9]:
                    f = os.path.join(model_dir,  f"evolution-{model}-{planet}-grid-{Hk}-{Ck}-tau{tau}-data.csv")
                    if os.path.isfile(f):
                        model_data[planet][f"{k}-tau{tau}"] = pd.read_csv(f)

    # check we loaded something...
    if all(v is None for v in model_data[planet].values()):
        print(f"    WARNING: No evolution data found for model '{model}', planet '{planet}'.")
        
    return model_data

def get_melting_curves(model):
    out = None

    # directory
    melting_dir = "../melting_curves"

    # find the file
    file = None
    for f in os.listdir(melting_dir):
        if f.startswith(model):
            if file is not None:
                print(f"WARNING: Multiple meltings found for '{model}'")
            file = os.path.abspath(os.path.join(melting_dir, f))

    if file is None:
        print(f"WARNING: No melting curve found for '{model}'")
        return out
    
    # load the file
    data = pd.read_csv(file, sep=r"\s+")

    out = {"p":None, "d":None}
    # independent variables
    if "pressure[Pa]" in data.columns:
        out["p"] = data["pressure[Pa]"].values / 1e9  # GPa
    if "radius[km]" in data.columns:
        x = data["radius[km]"].values
        out["d"] = np.amax(x) - x
    elif "depth[km]" in data.columns:
        out["d"] = data["depth[km]"].values

    if out["p"] is None and out["d"] is None:
        print(f"WARNING: No independent variable found for melting curve '{model}'")

    # dependent variables
    out["tsol"] = data["solidus[K]"].values
    out["tliq"] = data["liquidus[K]"].values

    return out
