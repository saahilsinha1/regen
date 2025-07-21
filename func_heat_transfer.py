from types import SimpleNamespace
import numpy as np
from input.input_variables import *
import matplotlib.pyplot as plt

def func_heat_transfer(Prop, Gas, InnerGeometry):

    Transport = SimpleNamespace()

    # INITIAL BARTZ EQUATION CALCULATION

    # Property Variation Factor (sigma)
    om = 0.6
    T_w_guess = 700 # K
    T_c = Gas.temps[0]
    
    pvf = np.zeros(len(Gas.stations))
    for i in range(len(pvf)):

        pvf[i] = 1/( (0.5*(T_w_guess/T_c)*(1+0.5*Gas.mach[i]**2*(Gas.gamma[i]-1)) + 0.5)**(0.5-om/5) 
                    * (1+0.5*Gas.mach[i]**2*(Gas.gamma[i]-1))**(om/5))
        
    Transport.bartz_pvf = pvf

    # Estimate Gas Properties at each Station

    Cp_stations = np.zeros(len(Gas.stations))
    for i in range(len(Cp_stations)):
        Cp_stations[i] = np.interp(Gas.stations[i], InnerGeometry.main_stations, Gas.Cp_vals)
    
    mu_stations = np.zeros(len(Gas.stations))
    for i in range(len(Cp_stations)):
        mu_stations[i] = np.interp(Gas.stations[i], InnerGeometry.main_stations, Gas.mu_vals)
    
    k_stations = np.zeros(len(Gas.stations))
    for i in range(len(Cp_stations)):
        k_stations[i] = np.interp(Gas.stations[i], InnerGeometry.main_stations, Gas.k_vals)

    Pr_stations = np.zeros(len(Gas.stations))
    for i in range(len(Cp_stations)):
        Pr_stations[i] = np.interp(Gas.stations[i], InnerGeometry.main_stations, Gas.Pr_vals)

    Transport.Cp_stations = Cp_stations
    Transport.mu_stations = mu_stations
    Transport.k_stations = k_stations
    Transport.Pr_stations = Pr_stations

    # Bartz Equation

    h_g = np.zeros(len(Gas.stations))
    for i in range(len(h_g)):

        h_g[i] = ((0.026/(Prop.r_t*2)**0.2) 
                  * ((Transport.mu_stations[i]**0.2*Transport.Cp_stations[i])/(Transport.Pr_stations[i]**0.6)) 
                  * ((p_c*6894.76)/(Prop.cstar))**0.8 
                  * ((Prop.r_t*2)/(1.5 * Prop.r_t))**0.1 
                  * (Prop.A_t/Gas.A_stations[i])**0.9 
                  * Transport.bartz_pvf[i])

    plt.plot(Gas.stations*39.3701, h_g)
    plt.title("Gas Side Heat Transfer Coefficient")
    plt.xlabel("Position (in)")
    plt.ylabel("hg (W/m^2/K)")
    plt.show()

    return Gas, Transport