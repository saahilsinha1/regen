import numpy as np
from types import SimpleNamespace
from input.input_variables import *
import matplotlib.pyplot as plt


def func_inner_geometry(Prop):

    InnerGeometry = SimpleNamespace()

    # RAO NOZZLE

    a_n, a_e = calc_rao_angles(Prop)

    # Converging arc
    s_a_con = -135*0.0174533 # deg -> rad
    e_a_con = -np.pi/2 # rad
    angles_con = np.linspace(s_a_con, e_a_con, 100)

    x_con = np.zeros(len(angles_con))
    y_con = np.zeros(len(angles_con))

    for angle in range(len(angles_con)):

        x_con[angle] = 1.5 * Prop.r_t * np.cos(angles_con[angle])
        y_con[angle] = 1.5 * Prop.r_t * np.sin(angles_con[angle]) + 2.5 * Prop.r_t

    # Diverging arc
    s_a_div = -np.pi/2 # rad
    e_a_div = a_n - np.pi/2
    angles_div = np.linspace(s_a_div, e_a_div, 100)

    x_div = np.zeros(len(angles_div))
    y_div = np.zeros(len(angles_div))

    for angle in range(len(angles_div)):

        x_div[angle] = 0.382 * Prop.r_t * np.cos(angles_div[angle])
        y_div[angle] = 0.382 * Prop.r_t * np.sin(angles_div[angle]) + 1.382 * Prop.r_t

    # Bell (Bezier Curve)

    L_n = 0.8 * (((Prop.r_e/Prop.r_t)-1)*Prop.r_t)/np.tan(0.261799)

    pN = (0.382 * Prop.r_t * np.cos(a_n - np.pi/2), 0.382 * Prop.r_t * np.sin(a_n - np.pi/2) + 1.382 * Prop.r_t)
    pE = (1.5 * Prop.r_t * np.cos(-np.pi/2) + L_n, Prop.r_e)

    m1, m2 = np.tan(a_n), np.tan(a_e)
    C1, C2 = pN[1] - m1*pN[0], pE[1] - m2*pE[0]
    pQ = ((C2-C1)/(m1-m2), (m1*C2 - m2*C1)/(m1-m2))

    t = np.linspace(0,1,100)
    x_par = np.zeros(len(t))
    y_par = np.zeros(len(t))

    for i in range(len(t)):

        x_par[i] = (1-t[i])**2*pN[0] + 2*(1-t[i])*t[i]*pQ[0] + t[i]**2*pE[0]
        y_par[i] = (1-t[i])**2*pN[1] + 2*(1-t[i])*t[i]*pQ[1] + t[i]**2*pE[1]

    # Converging straight

    InnerGeometry.r_c = r_c_in*0.0254 # in -> m

    r_con_f = 2*0.0254 # in -> m

    y_con_s = np.linspace(InnerGeometry.r_c - (r_con_f*(1-np.sin(np.pi/4))), y_con[0], 100)
    C_con_s = y_con[0]+x_con[0]
    x_con_s = -(y_con_s-C_con_s)

    angles_con_f = np.linspace(np.pi/2, np.pi/4, 100)

    x_con_f = np.zeros(len(angles_con_f))
    y_con_f = np.zeros(len(angles_con_f))

    for angle in range(len(angles_con_f)):

        x_con_f[angle] = r_con_f * np.cos(angles_con_f[angle]) + x_con_s[0] - (r_con_f * np.cos(np.pi/4))
        y_con_f[angle] = r_con_f * np.sin(angles_con_f[angle]) + InnerGeometry.r_c - r_con_f

    # CALCULATE CHAMBER VOLUME
    InnerGeometry.V_c = Lstar * Prop.A_t # m^3

    x_con_all = np.concatenate((x_con_f, x_con_s, x_con))
    y_con_all = np.concatenate((y_con_f, y_con_s, y_con))

    V_con = 0
    for i in range(len(x_con_all)-1):
        dx = x_con_all[i+1] - x_con_all[i]
        V_con += dx * (y_con_all[i]**2 + y_con_all[i+1]**2) / 2
    V_con *= np.pi

    V_cyl = InnerGeometry.V_c - V_con
    L_cyl = V_cyl / (np.pi * InnerGeometry.r_c**2)

    x_cyl = np.linspace(x_con_f[0]-L_cyl, x_con_f[0], 100)
    y_cyl = InnerGeometry.r_c * np.ones(len(x_cyl))

    # Combining geometries

    x_arr = np.concatenate((x_cyl, x_con_f, x_con_s, x_con, x_div, x_par)) - x_cyl[0]
    y_arr = np.concatenate((y_cyl, y_con_f, y_con_s, y_con, y_div, y_par))

    InnerGeometry.contour = np.array([x_arr, y_arr])
    InnerGeometry.main_stations = np.array([0, L_cyl, L_cyl+x_con_all[len(x_con_all)-1]-x_con_all[0], L_cyl+x_con_all[len(x_con_all)-1]-x_con_all[0]+L_n])

    return Prop, InnerGeometry

def calc_rao_angles(Prop):

    # For 80% of conical nozzle, eps = 5
    # PLACEHOLDER
    a_n = 23*0.0174533 # deg -> rad
    a_e = 13*0.0174533 # deg -> rad

    return a_n, a_e