
# coding: utf-8

# In[ ]:

def interception_efficiency(alpha,Ku,N_R):
    import numpy as np
    eta_R = (1+N_R)/(2*Ku)*(2*np.log(1+N_R)-1+alpha+(1/(1+N_R))**2*(1-alpha/2)-alpha/2*(1+N_R)**2)
    boolean_array = np.less(1+N_R,1/np.sqrt(alpha))
    eta_R[np.squeeze(np.logical_not(boolean_array)),:] = np.inf
    return eta_R

