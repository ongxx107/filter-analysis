
# coding: utf-8

# In[ ]:

def diffusion_efficiency(alpha,Ku,Pe,d_f,d_f_R):
    import numpy as np
    
    eta_D = 0.84*(d_f/d_f_R)**1.43*((1-alpha)*Pe)**-0.43
    
    return eta_D

