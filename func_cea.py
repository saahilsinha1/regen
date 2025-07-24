from rocketcea.cea_obj_w_units import CEA_Obj
from util.eth75_card import *
from input.input_variables import *
from types import SimpleNamespace
import numpy as np

def func_cea(C):

    Prop = SimpleNamespace()
    Gas = SimpleNamespace()

    # UNIT CONVERSIONS
    thrust_N = thrust * 4.44822 # lbf -> N
    p_c_Pa = p_c * 6894.76 # psia -> Pa

    # CALCULATE OPTIMAL O/F RATIO
    ofr_array = np.linspace(1.3, 1.4, 50)
    cstar_array = np.zeros(len(ofr_array))

    for i in range(len(ofr_array)):

        cstar_array[i] = C.get_Cstar(Pc=p_c, MR = ofr_array[i])

    Prop.ofr = ofr_array[np.argmax(cstar_array)]

    # CALCULATE SUPERSONIC AREA RATIO
    Prop.eps = C.get_eps_at_PcOvPe(Pc=p_c, MR=Prop.ofr, PcOvPe=p_c/p_amb)

    # FIND CSTAR AND CTAU
    cstar = C.get_Cstar(Pc=p_c, MR=Prop.ofr) # m/s
    Ctau = C.get_PambCf(Pamb=p_amb, Pc=p_c, MR=Prop.ofr, eps=Prop.eps)[0]
    Prop.cstar = cstar

    # CALCULATE MASS FLOW RATES
    Prop.mdot_prop = thrust_N/(cstar*cstar_eff*Ctau*Ctau_eff) # kg/s
    Prop.mdot_fuel = Prop.mdot_prop/(1+Prop.ofr)
    Prop.mdot_ox = Prop.mdot_prop - Prop.mdot_fuel

    # CALCULATE THROAT GEOMETRY
    Prop.A_t = (cstar_eff * cstar * Prop.mdot_prop)/p_c_Pa # m^2
    Prop.r_t = np.sqrt(Prop.A_t/np.pi) # m

    # CALCULATE EXIT GEOMETRY
    Prop.A_e = Prop.A_t * Prop.eps
    Prop.r_e = np.sqrt(Prop.A_e/np.pi)
    
    # GAS PROPERTIES
    Gas.temps = C.get_Temperatures(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)
    Gas.gamma = np.array([C.get_Chamber_MolWt_gamma(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)[1], # Injector Face (is this same as chamber?***)
                           C.get_Chamber_MolWt_gamma(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)[1], # Chamber
                           C.get_Throat_MolWt_gamma(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)[1], # Nozzle Throat
                           C.get_exit_MolWt_gamma(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)[1]]) # Nozzle Exit
    
    chamber_transport = C.get_Chamber_Transport(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)
    throat_transport = C.get_Throat_Transport(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)
    exit_transport = C.get_Exit_Transport(Pc=p_c, MR=Prop.ofr, eps=Prop.eps)

    Gas.Cp_vals = np.array([chamber_transport[0], chamber_transport[0], throat_transport[0], exit_transport[0]]) # J/kg/K
    Gas.mu_vals = np.array([chamber_transport[1], chamber_transport[1], throat_transport[1], exit_transport[1]])/10 # Pa s
    Gas.k_vals = np.array([chamber_transport[2], chamber_transport[2], throat_transport[2], exit_transport[2]]) 
    Gas.Pr_vals = np.array([chamber_transport[3], chamber_transport[3], throat_transport[3], exit_transport[3]]) # unitless

    print(Gas.Cp_vals[3])
    print(Gas.mu_vals[3])
    print(Gas.k_vals[3])
    print(Gas.Pr_vals[3])

    return Prop, Gas


