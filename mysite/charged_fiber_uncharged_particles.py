
# coding: utf-8

# In[1]:

def charged_fiber_uncharged_particles(alpha,N_R,N_P):
    
    import os
    import numpy as np
    import scipy as sp
    import scipy.constants as sc
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.externals import joblib
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    KNN_classifier = joblib.load(os.path.join(BASE_DIR,'KNN_classifier_sigma_0.pkl'))
    KNN_classifier_hyperparameters = np.load(os.path.join(BASE_DIR,'KNN_classifier_sigma_0_hyperparameters.npz'))
    X_classifier_min = KNN_classifier_hyperparameters['x_min']
    X_classifier_max = KNN_classifier_hyperparameters['x_max']
    w_classifier = KNN_classifier_hyperparameters['w']
    
    KNN_regressor = joblib.load(os.path.join(BASE_DIR,'KNN_regressor_sigma_0.pkl'))
    KNN_regressor_hyperparameters = np.load(os.path.join(BASE_DIR,'KNN_regressor_sigma_0_hyperparameters.npz'))
    X_regressor_min = KNN_regressor_hyperparameters['x_min']
    X_regressor_max = KNN_regressor_hyperparameters['x_max']
    w_regressor = KNN_regressor_hyperparameters['w']
   
    pi = sc.pi
    
    parameters = np.append(np.append(alpha*np.ones([N_P.shape[0],1]),N_R,axis=1),N_P,axis=1)
    
    X_classifier_scaled = (np.log(parameters)-X_classifier_min)/(X_classifier_max-X_classifier_min)
    X_regressor_scaled = (np.log(parameters)-X_regressor_min)/(X_regressor_max-X_regressor_min)

    Y_classifier_predicted = KNN_classifier.predict(np.sqrt(w_classifier)*X_classifier_scaled)
    classifier_boolean = np.transpose(np.atleast_2d(np.equal(Y_classifier_predicted,1)))
    
    theta_b = pi/(np.exp(np.transpose(np.atleast_2d(KNN_regressor.predict(np.sqrt(w_regressor)*X_regressor_scaled))))+1)  
    #theta_b = pi/(np.exp(-KNN_regressor.predict(np.sqrt(w_regressor)*X_regressor_scaled))+1)  

    boolean_array = np.logical_and(np.logical_and(np.greater(1-alpha**(5/2)*N_P,0),np.less(1+N_R,1/np.sqrt(alpha))),classifier_boolean)
    
    eta_sigma_0 = 1/np.sqrt(alpha)*np.sin(theta_b)+alpha**2*N_P*(pi-theta_b)
    eta_sigma_0[np.squeeze(np.logical_not(boolean_array)),:] = np.inf

    return eta_sigma_0
