from rocketcea.cea_obj_w_units import CEA_Obj
from util.eth75_card import *

C = CEA_Obj(oxName='LOX', fuelName='Eth75',
                pressure_units="psia",
                cstar_units="m/s",
                temperature_units="K",
                density_units="kg/m^3",
                specific_heat_units="J/kg-K",
                viscosity_units="poise")

from func_cea import func_cea
Prop, Gas = func_cea(C)

from func_inner_geometry import func_inner_geometry
Prop, InnerGeometry = func_inner_geometry(Prop)

from func_isentropic_stations import func_isentropic_stations
Gas = func_isentropic_stations(Prop, Gas, InnerGeometry) 

from func_heat_transfer import func_heat_transfer
Gas, Transport = func_heat_transfer(Prop, Gas, InnerGeometry)