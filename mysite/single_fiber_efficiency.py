
# coding: utf-8

# In[ ]:

def single_fiber_efficiency(alpha,Pe,N_R,N_P,N_C,N_I,d_f,d_f_R,n):
    import numpy as np
    from interception_efficiency import interception_efficiency
    from diffusion_efficiency import diffusion_efficiency
    from charged_fiber_uncharged_particles import charged_fiber_uncharged_particles
    from charged_fiber_charged_particles import charged_fiber_charged_particles

    
    Ku = -1/2*np.log(alpha)-3/4+alpha-alpha**2/4
    eta_D = diffusion_efficiency(alpha,Ku,Pe,d_f,d_f_R)
    if isinstance(n,float):
        if np.all(N_P==0):
            eta_R = interception_efficiency(alpha,Ku,N_R)
            eta_total = eta_D+eta_R
        elif np.all(N_I==0):
            eta_sigma_0 = charged_fiber_uncharged_particles(alpha*np.ones([N_P.shape[0],1]),N_R,N_P)
            eta_total = eta_D+eta_sigma_0
        else:
            eta_sigma_q = charged_fiber_charged_particles(alpha*np.ones([N_P.shape[0],1]),N_R,N_P,N_I,N_C)
            eta_total = eta_D+eta_sigma_q
    elif isinstance(n,np.ndarray) and n.shape[1] == 1:
            eta_sigma_q = charged_fiber_charged_particles(alpha,N_R,N_P,N_I,N_C)
            eta_total = eta_D+eta_sigma_q
    else:
        n_size = n.shape[1]
        d_p_size = N_P.shape[0]
        zero_indices = np.where(n==0)
        number_of_zeros = (zero_indices[1].shape)[0]
        eta_sigma_0 = charged_fiber_uncharged_particles(alpha*np.ones([N_P.shape[0],1]),N_R,N_P)
        eta_sigma_q = charged_fiber_charged_particles(np.tile(alpha*np.ones([d_p_size,1]),(n_size-number_of_zeros,1)),
                                                                 np.tile(N_R,(n_size-number_of_zeros,1)),
                                                                 np.tile(N_P,(n_size-number_of_zeros,1)),
                                                                 np.reshape(np.transpose(N_I[:,np.squeeze(n!=0)]),(-1,1)),
                                                                 np.reshape(np.transpose(N_C[:,np.squeeze(n!=0)]),(-1,1)))
        eta_sigma = np.concatenate(np.vsplit(eta_sigma_q,n_size-number_of_zeros),axis=1)
        for ii in np.nditer(zero_indices[1]):
            eta_sigma = np.insert(eta_sigma,np.array([ii]),eta_sigma_0,axis=1)
        eta_total = eta_sigma+eta_D
            
    return eta_total

