from types import SimpleNamespace
import numpy as np
from input.input_variables import *
import matplotlib.pyplot as plt

def func_heat_transfer(Prop, Gas, InnerGeometry):

    Transport = SimpleNamespace()

    ##### BY-STATION GAS PROPERTIES #####

    # Specific heat
    Cp = np.zeros(len(Gas.stations))
    for i in range(len(Cp)):
        Cp[i] = np.interp(Gas.stations[i], InnerGeometry.main_stations, Gas.Cp_vals)
    
    # Dynamic viscosity
    mu = np.zeros(len(Gas.stations))
    for i in range(len(mu)):
        mu[i] = np.interp(Gas.stations[i], InnerGeometry.main_stations, Gas.mu_vals)
    
    # Thermal conductivity
    k = np.zeros(len(Gas.stations))
    for i in range(len(k)):
        k[i] = np.interp(Gas.stations[i], InnerGeometry.main_stations, Gas.k_vals)

    # Prandtl number
    Pr = np.zeros(len(Gas.stations))
    for i in range(len(Pr)):
        Pr[i] = np.interp(Gas.stations[i], InnerGeometry.main_stations, Gas.Pr_vals)

    Transport.Cp_stations = Cp
    Transport.mu_stations = mu
    Transport.k_stations = k
    Transport.Pr_stations = Pr



    ##### ADIABATIC WALL TEMPERATURE DETERMINATION #####

    # Chamber temperature from CEA data
    T_c = Gas.temps[0]

    # Calculate local recovery factors
    local_recovery = np.zeros(len(Gas.stations))
    for i in range(len(local_recovery)):

        # Calculates local recovery factor for turbulent flow [Huzel & Huang, p. 85]
        local_recovery[i] = Pr[i]*0.33

    # Calculate adiabatic wall temperatures
    T_aw = np.zeros(len(Gas.stations))
    for i in range(len(T_aw)):

        # Calculates adiabatic wall temperature [Huzel & Huang, p. 85, eqn. 4-10-a]
        r = local_recovery[i]
        gamma = Gas.gamma[i]
        M = Gas.mach[i]
        T_aw[i] = T_c * ((1 + r*((gamma-1)/2)*M**2)/
                                  (1 + ((gamma-1)/2)*M**2))



    ##### PROPERTY VARIATION FACTOR (BARTZ BOUNDARY LAYER CORRECTION FACTOR) #####

    # Experimentally determined [Negishi et al.]
    omega = 0.6 
    
    # Guessed hot wall temperature
    T_wg_guess = 700 # K
    
    # Calculate property variation factor
    pvf = np.zeros(len(Gas.stations))
    for i in range(len(pvf)):

        # Calculates PVF for Bartz equation [Huzel & Huang, p. 86, eqn. 4-14]
        pvf[i] = 1/( (0.5*(T_wg_guess/T_c)*(1+0.5*Gas.mach[i]**2*(Gas.gamma[i]-1)) + 0.5)**(0.5-omega/5) 
                    * (1+0.5*Gas.mach[i]**2*(Gas.gamma[i]-1))**(omega/5))
        
    Transport.bartz_pvf = pvf

    

    ##### BARTZ EQUATION/CORRELATION #####

    # Evaluate Bartz correlation
    h_g = np.zeros(len(Gas.stations))
    for i in range(len(h_g)):

        # Calculates gas-side heat transfer coefficient h_g [Huzel & Huang, p. 86, eqn. 4-13]
        h_g[i] = ((0.026/(Prop.r_t*2)**0.2) 
                  * ((Transport.mu_stations[i]**0.2*Transport.Cp_stations[i])/(Transport.Pr_stations[i]**0.6)) 
                  * ((p_c*6894.76)/(Prop.cstar))**0.8 
                  * ((Prop.r_t*2)/(1.5 * Prop.r_t))**0.1 
                  * (Prop.A_t/Gas.A_stations[i])**0.9 
                  * Transport.bartz_pvf[i])
        
    

    ##### INITIAL HOT-GAS SIDE HEAT FLUX #####

    # Calculate heat flux
    q_g = np.zeros(len(Gas.stations))
    for i in range(len(q_g)):

        # Evaluate heat flux from adiabatic wall temp and guessed hot wall temp [Huzel & Huang, p. 85, eqn. 4-10]
        q_g[i] = h_g[i]*(T_aw[i]-T_wg_guess)



    plt.figure("Gas Side Heat Transfer Coefficient")
    plt.plot(Gas.stations*39.3701, h_g, color="orange")
    plt.title("Gas Side Heat Transfer Coefficient")
    plt.xlabel("Position (in)")
    plt.ylabel("hg (W/m^2/K)")

    plt.figure("Gas Side Heat Flux")
    plt.plot(Gas.stations*39.3701, q_g, color="red")
    plt.title("Gas Side Heat Flux")
    plt.xlabel("Position (in)")
    plt.ylabel("qg (W/m^2)")

    return Gas, Transport