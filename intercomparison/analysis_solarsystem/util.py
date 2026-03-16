import pandas as pd
import os

_gas_colors = {
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
    "O2": "#00ff00",
    # N rich
    "NO2": "#eb0076",
    "H2SO4": "#46eba4",
    "N2": "#870036",
    "NH3": "#675200",
}

_model_colors = {
    "proteus":   "#1f77b4",
    "pacman":    "#ff7f0e",
    "lincs":     "#2ca02c",
    "gooey":     "#d62728",
    "neongooey": "#ff7086",
    "moai":      "#8c564b",
}

_labels = {
"t(yr)":           "Time [yr]" ,
"T_surf(K)":        r"$T_{\rm surf}$ [K]",
"T_pot(K)":         r"$T_{\rm pot}$ [K]",
"flux_surf(W/m2)":  r"$F_{\rm surf}$ [W m$^{-2}$]",
"flux_OLR(W/m2)":   r"$F_{\rm OLR}$ [W m$^{-2}$]",
"flux_ASR(W/m2)":   r"$F_{\rm ASR}$ [W m$^{-2}$]",
"phi(vol_frac)":    r"Melt frac.",
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

"proteus": "PROTEUS",
"pacman": "PACMAN",
"neongooey": "NeonGOOEY",
"gooey": "GOOEY",
"lincs": "LINCS",
"moai": "MOAI"
}

def get_label(key:str):
    if key in _labels.keys():
        return _labels[key]
    else:
        return key

def get_color(thing:str):
    if thing in _gas_colors:
        return _gas_colors[thing]
    elif thing in _model_colors:
        return _model_colors[thing]
    else:
        print(f"WARNING: Plotting color for '{thing}' not defined")
        return "#222222"


def list_planets():
    return ("earth", "venus")

def list_models():
    """List the available models in the outputs directory."""
    outputs_dir = os.path.join(os.path.dirname(__file__), "..", "outputs")
    if not os.path.isdir(outputs_dir):
        raise FileNotFoundError(f"Outputs directory '{outputs_dir}' not found.")
    return os.listdir(outputs_dir)

def load_model_data(model:str):
    """Load the model data from the CSV file."""

    # check if model directory exists
    model = model.lower()
    model_dir = os.path.join(os.path.dirname(__file__), "..", "outputs", model)
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"Model directory '{model_dir}' not found.")

    # load files for each combination of H/C/planet
    model_data = {"earth":{}, "venus":{}}
    for planet in ["earth", "venus"]:
        for Hf in ["Hhigh", "Hmid", "Hlow", ""]:
            if Hf == "":
                Hk = f"Hlow"
                Hf = ""
            else:
                Hk = Hf
                Hf = f"-{Hf}"
                
                
            for Cf in ["Chigh", "Cmid", "Clow", ""]:
                if Cf == "":
                    Ck = f"-Clow"
                    Cf = ""
                else:
                    Ck = f"-{Cf}"
                    Cf = f"-{Cf}"
                    

                k = f"{Hk}{Ck}"

                # evolution data
                f = os.path.join(model_dir,  f"evolution-{model}-{planet}-grid{Hf}{Cf}-data.csv")
                if os.path.isfile(f):
                    model_data[planet][f"{k}-evo"] = pd.read_csv(f)

                # atmosphere profile data
                for tau in [1,2,3,4,5,6,7,8,9]:
                    f = os.path.join(model_dir,  f"evolution-{model}-{planet}-grid{Hf}{Cf}-tau{tau}-data.csv")
                    if os.path.isfile(f):
                        model_data[planet][f"{k}-tau{tau}"] = pd.read_csv(f)

    # check we loaded something...
    if all(v is None for v in model_data[planet].values()):
        print(f"WARNING: No evolution data found for model '{model}', planet '{planet}'.")
    if all(v is None for v in model_data[planet].values()):
        print(f"WARNING: No atmosphere profile data found for model '{model}', planet '{planet}'.")
        
    return model_data