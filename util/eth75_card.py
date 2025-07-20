from rocketcea.cea_obj import add_new_fuel

card_str = """

fuel C2H5OH(L)   C 2 H 6 O 1  wt%=75.
h,cal=-66370.0      t(k)=298.15       

fuel water H 2.0 O 1.0  wt%=25.
h,cal=-68308.  t(k)=298.15 rho,g/cc = 0.9998

"""

add_new_fuel( 'Eth75', card_str )