from types import SimpleNamespace
import numpy as np

Alum = SimpleNamespace() # AlSi10Mg

# Modulus of Elasticity
Alum.E = np.array([
    [298,      373,      473,      573,      673,      823], # K
    [72e9,     70e9,     60e9,     50e9,     40e9,     30e9] # GPa -> Pa
])

# Poisson's Ratio
Alum.nu = np.array([
    [298,  373,  473,  573,  673,  823], # K
    [0.33, 0.33, 0.33, 0.33, 0.33, 0.33] # unitless
])

# Coefficient of Thermal Expansion
Alum.alpha = np.array([
    [298,         373,         473,         573,         673,         823],  # K
    [20e-6,       22e-6,       22e-6,       27e-6,       29e-6,       30e-6] # 1/K
])

# Thermal Conductivity
Alum.k = np.array([
    [298, 373, 400, 473, 500, 570, 620, 640, 700], # K
    [115, 110, 116, 114, 109, 101, 54,  48,  51]   # W/m*K
])

# Specific Heat 
Alum.cp = np.array([
    [298, 373, 473,  573,  673,  698,  823], # K
    [910, 960, 1000, 1040, 1100, 1136, 1326] # J/kg*K
])

# Yield Strength
Alum.sy = np.array([
    [298,       373,       473,       573,       673,      823], # K
    [169e6,     160e6,     140e6,     120e6,     60e6,     32e6] # MPa -> Pa
])
