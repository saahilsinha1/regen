from types import SimpleNamespace
import numpy as np
from util.material import Alum

def mat_prop(material, temp):

    Material = SimpleNamespace()
    Material.E = interp_prop(temp, material.E[0], material.E[1])
    Material.nu = interp_prop(temp, material.nu[0], material.nu[1])
    Material.alpha = interp_prop(temp, material.alpha[0], material.alpha[1])
    Material.k = interp_prop(temp, material.k[0], material.k[1])
    Material.cp = interp_prop(temp, material.cp[0], material.cp[1])
    Material.sy = interp_prop(temp, material.sy[0], material.sy[1])
    
    return Material

def interp_prop(temp, temp_arr, prop_arr):

    return np.interp(temp, temp_arr, prop_arr)
