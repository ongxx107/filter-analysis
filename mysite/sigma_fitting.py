
# coding: utf-8

# In[ ]:

def sigma_fitting(input_values):

    import scipy.constants as sc
    import numpy as np
    from scipy.optimize import differential_evolution
    from single_fiber_efficiency import single_fiber_efficiency
    from wiedensohler_charge_distribution import wiedensohler_charge_distribution
    from sklearn.metrics import r2_score
    
    k_B = sc.k
    e = sc.e
    epsilon_0 = sc.epsilon_0
    pi = sc.pi     
            
    def evaluate_single_fiber_efficiency(d_p,n,sigma,d_f,lambda_g,T,mu_g,U,d_f_R,epsilon_g,epsilon_p,epsilon_f,alpha):
        q = np.absolute(n)*e
        N_R = d_p/d_f
        Kn_p = 2*lambda_g/d_p
        C = 1+Kn_p*(1.165+0.483*np.exp(-0.997/Kn_p))
        D = k_B*T*C/(3*pi*mu_g*d_p)
        Pe =  U*d_f/D
        N_Di = (2/3*(1-epsilon_g/epsilon_p)/(1+2*epsilon_g/epsilon_p)*epsilon_g*sigma**2*d_p**2*C/
                (epsilon_0*(epsilon_f+epsilon_g)**2*mu_g*U*d_f))
        N_Im = ((epsilon_f-epsilon_g)/(epsilon_f+epsilon_g)*q**2*C/
                (12*pi**2*epsilon_0*epsilon_g*mu_g*U*d_p*d_f**2))
        N_C = sigma*q*C/(3*pi*epsilon_0*(epsilon_f+epsilon_g)*mu_g*U*d_p)
        eta = single_fiber_efficiency(alpha,Pe,N_R,N_Di,N_C,N_Im,d_f,d_f_R,n)
        return eta

    def P_r_squared_min(sigma,*args):
        i = 0
        for charge_key in input_values:
            
            d_p = input_values[charge_key]['d_p']
            epsilon_p = input_values[charge_key]['epsilon_p']
            
            T = input_values[charge_key]['T']
            U_0 = input_values[charge_key]['U_0']
            rho_g = input_values[charge_key]['rho_g']
            lambda_g = input_values[charge_key]['lambda_g']
            epsilon_g = input_values[charge_key]['epsilon_g']
            mu_g = input_values[charge_key]['mu_g']
            
            P_mechanical_layers = np.ones_like(input_values[charge_key]['penetration'])
            
            for key in input_values[charge_key]:
                
                if 'layer' in key and input_values[charge_key]['d_p'].size > 0:
                
                    h = input_values[charge_key][key]['h']
                    d_f = input_values[charge_key][key]['d_f']
                    d_f_R = input_values[charge_key][key]['d_f_R']
                    alpha = input_values[charge_key][key]['alpha']
                    

                    if key == 'electret layer':
                        
                        U = U_0/(1-alpha)
                        epsilon_f = input_values[charge_key][key]['epsilon_f']
                        if charge_key == 'uncharged particles':
                            n = 0.0
                            P_electret_layer = (np.exp(-4*alpha*h*
                                                       evaluate_single_fiber_efficiency(d_p,n,sigma,d_f,lambda_g,T,mu_g,U,d_f_R,
                                                                                        epsilon_g,epsilon_p,epsilon_f,alpha)/
                                                       (pi*d_f*(1-alpha))))
                        elif charge_key == 'charged particles':
                            n = input_values[charge_key]['n']
                            P_electret_layer = (np.exp(-4*alpha*h*
                                                       evaluate_single_fiber_efficiency(d_p,n,sigma,d_f,lambda_g,T,mu_g,U,d_f_R,
                                                                                        epsilon_g,epsilon_p,epsilon_f,alpha)/
                                                       (pi*d_f*(1-alpha))))
                        else:
                            n = np.atleast_2d(np.arange(-11,12))
                            n_size = n.shape[1]
                            P_electret_layer = np.transpose(np.atleast_2d(np.sum(wiedensohler_charge_distribution(T,d_p,n)*
                                                       np.exp(-4*(alpha*np.ones(n_size))*(h*np.ones(n_size))*evaluate_single_fiber_efficiency(d_p,n,sigma,d_f,lambda_g,T,mu_g,U,d_f_R,
                                                                                        epsilon_g,epsilon_p,epsilon_f,alpha)/
                                                                                         (pi*(d_f*np.ones(n_size))*
                                                                                              (1-(alpha*np.ones(n_size))))),
                                                                                         axis=1)))
                    elif str.startswith(key,'mechanical'):
                        n = 0.0
                        active_layers = (input_values[charge_key][key]['h']!='')
                        if not np.all(np.invert(active_layers)):
                            U = U_0/(1-alpha[active_layers])
                            P_mechanical_layers[active_layers] = (np.exp(-4*alpha[active_layers]*h[active_layers]*
                                                                         evaluate_single_fiber_efficiency(d_p[active_layers],
                                                                                                          n[active_layers],0,
                                                                                                          d_f[active_layers],
                                                                                                          lambda_g[active_layers],
                                                                                                          T[active_layers],
                                                                                                          mu_g[active_layers],
                                                                                                          U,
                                                                                                          d_f_R[active_layers],
                                                                                                          epsilon_g[active_layers],
                                                                                                          epsilon_p[active_layers],
                                                                                                          epsilon_f[active_layers],
                                                                                                          alpha[active_layers])/
                                                                         (pi*d_f[active_layers]*(1-alpha[active_layers])))*
                                                                  P_mechanical_layers[active_layers])
                            P_mechanical_layers[np.invert(active_layers)] = P_mechanical_layers[np.inverts(active_layers)]                                                          
                    if i == 0:
                        try:
                            penetration = input_values[charge_key]['penetration']
                            P = P_electret_layer*P_mechanical_layers
                            i = i+1
                        except:
                            pass
                    else:
                        try:
                            penetration = np.append(penetration,input_values[charge_key]['penetration'])
                            P = np.append(P,P_electret_layer*P_mechanical_layers)
                            i = i+1
                        except:
                            pass
        if args[0] == 'r2':
            r2_results = {'r2':r2_score(penetration,P),'P_experiment':penetration,'P_theory':P}
            return r2_results
        else:
            return np.sum(np.square(penetration-P))
    res = differential_evolution(P_r_squared_min,bounds=[(1e-8,1e-2)],args=('optimize',),strategy='rand1bin',
                                  mutation=(0.5,1.0),recombination=0.9,popsize=10,disp=False)
    results = {'sigma':[],'r2':[],'P_experiment':[],'P_theory':[]}
    results['sigma'] = res.x[0]
    args = ('r2',)
    r2_results = P_r_squared_min(results['sigma'],*args)
    results['r2'] = r2_results['r2']
    results['P_experiment'] = r2_results['P_experiment']
    results['P_theory'] = r2_results['P_theory']
    return results

