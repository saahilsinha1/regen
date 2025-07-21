from types import SimpleNamespace
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def func_isentropic_stations(Prop, Gas, InnerGeometry):

    # Define Stations
    stations = np.linspace(0, InnerGeometry.contour[0][len(InnerGeometry.contour[0])-1], 50)
    

    # Interpolate Specific Heat Ratio at each station
    gamma_stations = np.zeros(len(stations))
    for i in range(len(gamma_stations)):
        gamma_stations[i] = np.interp(stations[i], InnerGeometry.main_stations, Gas.gamma)
    
    # Calculate Area at each station
    r_stations = np.zeros(len(stations))
    for i in range(len(r_stations)):
        r_stations[i] = np.interp(stations[i], InnerGeometry.contour[0], InnerGeometry.contour[1])

    A_stations = np.zeros(len(stations))
    for i in range(len(A_stations)):
        A_stations[i] = np.pi * r_stations[i]**2

    # Calculate Mach Number at each station
    M_stations = np.zeros(len(stations))
    for i in range(len(M_stations)):

        area_ratio = A_stations[i]/Prop.A_t
        gamma = gamma_stations[i]

        if stations[i]<InnerGeometry.main_stations[2]:
            M_stations[i] = fsolve(area_mach, 0.2, args=(area_ratio, gamma))[0]

        if stations[i]>InnerGeometry.main_stations[2]:
            M_stations[i] = fsolve(area_mach, 3, args=(area_ratio, gamma))[0]
    
    # Calculate Temperature at each station
    T_stations = np.zeros(len(stations))
    for i in range(len(T_stations)):
        T_stations[i] = Gas.temps[1]/( 1 + ((gamma_stations[i]-1)/2)*(M_stations[i]**2) )

    # # Calculate Static Pressure at each station
    # P_stations = np.zeros(len(stations))
    # for i in range(len(P_stations)):
    #     P_stations[i] = 
    
    Gas.stations = stations
    Gas.gamma = gamma_stations
    Gas.r_stations = r_stations
    Gas.A_stations = A_stations
    Gas.mach = M_stations
    Gas.temp = T_stations

    return Gas

def area_mach(M, area_ratio, gamma):
    temp = (2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * M**2)
    return (1/M) * temp**((gamma + 1)/(2*(gamma - 1))) - area_ratio