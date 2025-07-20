from rocketcea.cea_obj_w_units import CEA_Obj
from util.eth75_card import *
from func_cea import func_cea
from func_inner_geometry import func_inner_geometry

C = CEA_Obj(oxName='LOX', fuelName='Eth75',
                pressure_units="psia",
                cstar_units="m/s",
                temperature_units="K")

Prop = func_cea(C)

Prop, InnerGeometry = func_inner_geometry(Prop)

