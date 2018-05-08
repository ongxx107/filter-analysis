# coding: utf-8

# In[1]:

def csv_writer(layers,caseNames,epsilon_p_input,n_input,
               T_input_units,T_input,p_input_units,p_input,U_0_input_units,U_0_input,
               layerNames,alpha_input,d_f_input,d_f_R_input,epsilon_f_input,h_input_units,h_input,sigma_0_input,
               notes_input,Re_f,Kn_f,delta_p_units,delta_p,warning,d_p,E,FOM):

    import numpy as np
    import scipy.constants as sc
    import csv
    import io    
    
    layer_logical_array = np.asarray(layers)
    first_text_block = 1

    #BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #with open(os.path.join(BASE_DIR,'personal','static','personal','report.csv'), 'w', newline='',encoding='utf16') as f:
    for i in range(layer_logical_array.shape[0]):
        layer_index_array = np.argwhere(layer_logical_array[i][:]==1)
        number_of_layers = sum(layer_logical_array[i])
        if number_of_layers > 0:
            text_block = np.array([[caseNames[i]],
                                   [''],
                                   ['particle properties'],
                                   ['particle dielectric constant (-)'],
                                   ['particle charge state'],
                                   [''],
                                   ['operational properties'],
                                   ['temperature ('+T_input_units[i]+')'],
                                   ['upstream pressure ('+p_input_units[i]+')'],
                                   ['face velocity ('+U_0_input_units[i]+')'],
                                   [''],
                                   ['filter properties'],
                                   ['solidity (-)'],
                                   ['layer thickness ('+h_input_units[i][0]+')'],
                                   ['pressure drop equivalent fiber diameter ('+'µ'+'m)'],
                                   ['geometric fiber diameter ('+'µ'+'m)'],
                                   ['fiber dielectric constant (-)'],
                                   ['charge density ('+'µ'+'C/m^2)'],[''],['notes:'],
                                   [''],
                                   ['intermediate calculations'],
                                   ['layer pressure drop ('+delta_p_units[i]+')'],
                                   ['fiber Reynolds number (-)'],
                                   ['fiber Knudsen number (-)'],
                                   ['warning:'],
                                   ['']],ndmin=2)
            for m in range(max(number_of_layers,2)):
                new_text_section = [[],
                                    [],
                                    [],
                                    []]
                if m == 0:
                    new_text_section[0] = np.array([[''],
                                                    [''],
                                                    [''],
                                                    [epsilon_p_input[i]],
                                                    [n_input[i]],
                                                    [''],
                                                    [''],
                                                    [T_input[i]],
                                                    [p_input[i]],
                                                    [U_0_input[i]],
                                                    ['']],ndmin=2)
                    new_text_section[2] = np.array([[notes_input[i]],
                                                    ['']],ndmin=2)
                else:
                    new_text_section[0] = np.array([[''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    ['']],ndmin=2)
                    new_text_section[2] = np.array([[''],
                                                    ['']],ndmin=2)
                if m < number_of_layers:
                    j = layer_index_array[m][0]
                    new_text_section[1] = np.array([[layerNames[i][j]],
                                                    [alpha_input[i][j]],
                                                    [h_input[i][j]],
                                                    [d_f_R_input[i][j]],
                                                    [d_f_input[i][j]],
                                                    [epsilon_f_input[i][j]],
                                                    [sigma_0_input[i][j]],
                                                    ['']],ndmin=2)
                    new_text_section[3] = np.array([[layerNames[i][j]],
                                                    [delta_p[i][j]],
                                                    [Re_f[i][j]],
                                                    [Kn_f[i][j]],
                                                    [warning[i][j]],
                                                    ['']],ndmin=2)
                else:
                    new_text_section[1] = np.array([[''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    ['']],ndmin=2)
                    new_text_section[3] = np.array([[''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    [''],
                                                    ['']],ndmin=2)
                for n in range(len(new_text_section)):
                    if n == 0:
                        new_text = new_text_section[n]
                    else:
                        new_text = np.append(new_text,new_text_section[n],axis=0)
                text_block = np.append(text_block,new_text,axis=1)
            results_section = d_p[i]
            results_section = np.append(results_section,E[i],axis=1)
            results_section = np.append(results_section,FOM[i],axis=1)
            results_section = np.append([['results','',''],
                                         ['particle diameter (nm)','filtration efficiency (-)',
                                          'figure of merit ('+delta_p_units[i]+'^-1)']],
                                        results_section,axis=0)
            results_section = np.append(results_section,[['']*(number_of_layers-2)]*results_section.shape[0],axis=1)
            text_block = np.append(text_block,results_section,axis=0)
            if first_text_block == 1:
                text = text_block
                first_text_block = 0
            else:
                text_block = np.append([['']]*text.shape[0],text_block,axis=1)
                text = np.append(text,text_block,axis=1)
                
        #with open(os.path.join(BASE_DIR,'personal','static','personal','report.csv'), 'w', newline='',encoding='utf16') as f:
    f = io.StringIO()
    writer = csv.writer(f,dialect='excel-tab')
    writer.writerows(text)
    f.seek(0)
 
    return f.getvalue().encode("utf16")
