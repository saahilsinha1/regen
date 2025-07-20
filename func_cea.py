from rocketcea.cea_obj_w_units import CEA_Obj
from util.eth75_card import *
from input.input_variables import *
from types import SimpleNamespace
import numpy as np

def func_cea(C):

    Prop = SimpleNamespace()

    # UNIT CONVERSIONS
    thrust_N = thrust * 4.44822 # lbf -> N
    p_c_Pa = p_c * 6894.76 # psia -> Pa

    # CALCULATE OPTIMAL O/F RATIO
    ofr_array = np.linspace(0.5, 2, 150)
    cstar_array = np.zeros(len(ofr_array))

    for i in range(len(ofr_array)):

        cstar_array[i] = C.get_Cstar(Pc=p_c, MR = ofr_array[i])

    Prop.ofr = ofr_array[np.argmax(cstar_array)]

    # CALCULATE SUPERSONIC AREA RATIO
    Prop.eps = C.get_eps_at_PcOvPe(Pc=p_c, MR=Prop.ofr, PcOvPe=p_c/p_amb)

    # FIND CSTAR AND CTAU
    cstar = C.get_Cstar(Pc=p_c, MR=Prop.ofr) # m/s
    Ctau = C.get_PambCf(Pamb=p_amb, Pc=p_c, MR=Prop.ofr, eps=Prop.eps)[0]

    # CALCULATE MASS FLOW RATES
    Prop.mdot_prop = thrust_N/(cstar*cstar_eff*Ctau*Ctau_eff) # kg/s
    Prop.mdot_fuel = Prop.mdot_prop/(1+Prop.ofr)
    Prop.mdot_ox = Prop.mdot_prop - Prop.mdot_fuel

    # CALCULATE THROAT GEOMETRY
    Prop.A_t = (cstar_eff * cstar * Prop.mdot_prop)/p_c_Pa # m^2
    Prop.r_t = np.sqrt(Prop.A_t/np.pi)

    # CALCULATE EXIT GEOMETRY
    Prop.A_e = Prop.A_t * Prop.eps
    Prop.r_e = np.sqrt(Prop.A_e/np.pi)
    
    Prop.temps = C.get_Temperatures(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)

    return Prop


