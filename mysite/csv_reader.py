def csv_reader(reader):

    import csv
    import numpy as np
    import scipy.constants as sc
    from unit_conversion import unit_conversion
    from willekes_relation import willekes_relation
    from sutherland_formula import sutherland_formula
    from air_density import air_density
    from sigma_fitting import sigma_fitting
    from sklearn.metrics import r2_score

    input_values = {'uncharged particles':{'d_p':[],'epsilon_p':[],
                                           'T':[],'lambda_g':[],'mu_g':[],'rho_g':[],'epsilon_g':[],'U_0':[],
                                           'electret layer':{'h':[],'alpha':[],'d_f_R':[],'d_f':[],'epsilon_f':[]},
                                           'mechanical layer 1':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                           'mechanical layer 2':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                           'mechanical layer 3':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                           'mechanical layer 4':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                           'penetration':[]},
                    'charged particles':{'d_p':[],'epsilon_p':[],'n':[],
                                         'T':[],'lambda_g':[],'mu_g':[],'rho_g':[],'epsilon_g':[],'U_0':[],
                                         'electret layer':{'h':[],'alpha':[],'d_f_R':[],'d_f':[],'epsilon_f':[]},
                                         'mechanical layer 1':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                         'mechanical layer 2':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                         'mechanical layer 3':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                         'mechanical layer 4':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                         'penetration':[]},
                    'neutralized particles':{'d_p':[],'epsilon_p':[],
                                             'T':[],'lambda_g':[],'mu_g':[],'rho_g':[],'epsilon_g':[],'U_0':[],
                                             'electret layer':{'h':[],'alpha':[],'d_f_R':[],'d_f':[],'epsilon_f':[]},
                                             'mechanical layer 1':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                             'mechanical layer 2':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                             'mechanical layer 3':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                             'mechanical layer 4':{'h':[],'alpha':[],'d_f_R':[],'d_f':[]},
                                             'penetration':[]}}
    dielectric_constants = {'dos':4.05,'metal':np.inf,'pbt':3.4,'pc':3.1,'pctfe':2.72,'pe':2.25,'pmp':2.4,'pp':2.28,'ps':2.55,
                           'ptfe':2.1,'kcl':4.86,'sio2':3.76,'nacl':5.92}
    index_solidity = [13,22,29,36,43]
    column_solidity = ['N','W','AD','AK','AR']
    index_thickness = [20,27,34,41,48]
    column_thickness = ['U or V','AB or AC','AI or AJ','AP or AQ','AW or AX']
    index_diameter = [[14,23,30,37,44],
                      [16,25,32,39,46]]
    column_length = [['O or P','X or Y','AE or AF','AL or AM','AS or AT'],
                     ['Q or R','Z or AA','AG or AH','AN or AO','AU or AV']]
    warning = ''

    next(reader, None)
    next(reader, None)
    next(reader, None)
    for row in reader:
        try:
            if int(row[6])==0:
                charge_key = 'uncharged particles'
            else:
                charge_key = 'charged particles'
                input_values[charge_key]['n'].append(float(row[6]))
        except ValueError:
            try:
                if float(row[6]):
                    warning = 'Check value in  '+str(reader.line_num)+' and column G (7)'
                    break
            except ValueError:
                charge_key = 'neutralized particles'
        try:
            input_values[charge_key]['d_p'].append(unit_conversion(float(row[0]),row[1],'length'))
        except ValueError:
            warning = 'Check values in row '+str(reader.line_num)+' and columns A or B (1 or 2)'
            break
        if row[5]:
            try:
                input_values[charge_key]['epsilon_p'].append(float(row[5]))
            except ValueError:
                warning = 'Check value in row '+str(reader.line_num)+' and column F (6)'
                break
        elif row[4]:
            try:
                input_values[charge_key]['epsilon_p'].append(dielectric_constants[row[4].lower()])
            except ValueError:
                warning = 'Check value in row '+str(reader.line_num)+' and column E (5)'
                break
        else:
            warning = 'Check value in row '+str(reader.line_num)+' and columns E or F (5 or 6)'
            break
        try:
            T = unit_conversion(float(row[7]),row[8],'temperature')
            input_values[charge_key]['T'].append(T)
        except ValueError:
            warning = 'Check values in row '+str(reader.line_num)+' and columns H or I (8 or 9)'
            break
        try:
            p = unit_conversion(float(row[9]),row[10],'pressure')
        except ValueError:
            warning = 'Check values in row '+str(reader.line_num)+' and columns J or K (10 or 11)'
            break
        input_values[charge_key]['lambda_g'].append(willekes_relation(p,T))
        input_values[charge_key]['mu_g'].append(sutherland_formula(T))
        input_values[charge_key]['rho_g'].append(air_density(p,T))
        input_values[charge_key]['epsilon_g'].append(1.001)
        try:
            input_values[charge_key]['U_0'].append(unit_conversion(float(row[11]),row[12],'velocity'))
        except ValueError:
            warning = 'Check values in row '+str(reader.line_num)+' and columns L or M (12 or 13)'
            break
        if row[3]:
            try:
                P = float(row[3])
            except ValueError:
                warning = 'Check value in row '+str(reader.line_num)+' and column D (4)'
                break
            if P>=0 and P<=1:
                input_values[charge_key]['penetration'].append(P)
            else:
                warning = ('Penetration is not greater than or equal to 0 and less than or equal to 1 in row '+
                           str(reader.line_num)+' and column '
                           +column_solidity[counter]+' ('+str(index_solidity[counter]+1)+')')
                break
        elif row[2]:
            try:
                P = 1-float(row[2])
            except ValueError:
                warning = 'Check value in row '+str(reader.line_num)+' and column C (3)'
                break
            if P>=0 and P<=1:
                input_values[charge_key]['penetration'].append(P)
            else:
                warning = ('Efficiency is not greater than or equal to 0 and less than or equal to 1 in row '+
                           str(reader.line_num)+' and column '
                           +column_solidity[counter]+' ('+str(index_solidity[counter]+1)+')')
                break
        else:
            warning = 'Check value in row '+str(reader.line_num)+' and column C or D (3 or 4)'
            break
        counter = 0
        for key in input_values[charge_key]:
            if key == 'electret layer':
                try:
                    input_values[charge_key][key]['h'].append(unit_conversion(float(row[index_thickness[counter]]),
                                                                              row[index_thickness[counter]+1],'length'))
                except ValueError:
                    warning = ('Check value in row '+str(reader.line_num)+' and columns '
                               +column_thickness[counter]+' ('+str(index_thickness[counter]+1)+')')
                    break
                try:
                    alpha = float(row[index_solidity[counter]])
                except ValueError:
                    warning = ('Check value in row '+str(reader.line_num)+' and column '
                               +column_solidity[counter]+' ('+str(index_solidity[counter]+1)+')')
                    break
                if alpha>0 and alpha<1:
                    input_values[charge_key][key]['alpha'].append(alpha)
                else:
                    warning = ('Solidity is not greater than 0 and less than 1 in row '+str(reader.line_num)+' and column '
                               +column_solidity[counter]+' ('+str(index_solidity[counter]+1)+')')
                    break
                try:
                    d_f_R =  unit_conversion(float(row[index_diameter[0][counter]]),row[index_diameter[0][counter]+1],'length')
                    input_values[charge_key][key]['d_f_R'].append(d_f_R)
                except ValueError:
                    warning = ('Check value in row '+str(reader.line_num)+' and columns '
                               +column_diameter[0][counter]+' ('+str(index_diameter[0][counter]+1)+')')
                    break
                if row[index_diameter[1][counter]]:
                    try:
                        input_values[charge_key][key]['d_f'].append(unit_conversion(float(row[index_diameter[1][counter]]),
                                                                                    row[index_diameter[1][counter]+1],'length'))
                    except ValueError:
                        warning = ('Check value in row '+str(reader.line_num)+' and columns '
                                   +column_diameter[1][counter]+' ('+str(index_diameter[1][counter]+1)+')')
                        break
                else:
                    input_values[charge_key][key]['d_f'].append(d_f_R)
                if row[19]:
                    try:
                        input_values[charge_key][key]['epsilon_f'].append(float(row[19]))
                    except ValueError:
                        warning = 'Check value in row '+str(reader.line_num)+' and column T (20)'
                        break
                elif row[18]:
                    try:
                        input_values[charge_key][key]['epsilon_f'].append(dielectric_constants[row[18].lower()])
                    except ValueError:
                        warning = 'Check value in row '+str(reader.line_num)+' and column S (19)'
                        break
                else:
                    warning = 'Check values in row '+str(reader.line_num)+' and columns S or T (19 or 20)'
                    break
            elif key.startswith('mechanical layer'):
                counter = counter+1
                if len(row)>index_thickness[counter] and row[index_thickness[counter]]:        
                    try:
                        input_values[charge_key][key]['h'].append(unit_conversion(float(row[index_thickness[counter]]),
                                                                                  row[index_thickness[counter]+1],'length'))
                        row_empty = False
                    except ValueError:
                        warning = ('Check value in row '+str(reader.line_num)+' and columns '
                                   +column_thickness[counter]+' ('+str(index_thickness[counter]+1)+')')
                        break
                else:
                    input_values[charge_key][key]['h'].append('')
                    row_empty = True                        
                if len(row)>index_solidity[counter] and row[index_solidity[counter]]:
                    try:
                        alpha = float(row[index_solidity[counter]])
                    except ValueError:
                        warning = ('Check value in row '+str(reader.line_num)+' and column '
                                   +column_solidity[counter]+' ('+str(index_solidity[counter]+1)+')')
                        break
                    if alpha>0 and alpha<1:
                        if row_empty:
                            warning = 'Check values for'+key+'in row '+str(reader.line_num)
                            break
                        else:
                            input_values[charge_key][key]['alpha'].append(alpha)
                    else:
                        warning = ('Solidity is not greater than 0 and less than 1 in row '+str(reader.line_num)+' and column '
                                   +column_solidity[counter]+' ('+str(index_solidity[counter]+1)+')')
                        break
                else:
                    input_values[charge_key][key]['alpha'].append('')
                    if row_empty:
                        input_values[charge_key][key]['alpha'].append('')
                    else:
                        warning = 'Check values for'+key+'in row '+str(reader.line_num)
                        break   
                if len(row)>index_diameter[0][counter] and row[index_diameter[0][counter]]:
                    try:
                        d_f_R =  unit_conversion(float(row[index_diameter[0][counter]]),
                                                 row[index_diameter[0][counter]+1],'length')
                        if row_empty:
                            warning = 'Check values for'+key+'in row '+str(reader.line_num)
                            break
                        else:
                            input_values[charge_key][key]['d_f_R'].append(d_f_R)
                    except ValueError:
                        warning = ('Check value in row '+str(reader.line_num)+' and columns '
                                   +column_diameter[0][counter]+' ('+str(index_diameter[0][counter]+1)+')')
                        break
                else:
                    if row_empty:
                        d_f_R = ''
                        input_values[charge_key][key]['d_f_R'].append(d_f_R)
                    else:
                        warning = 'Check values for'+key+'in row '+str(reader.line_num)
                        break   
                if len(row)>index_diameter[1][counter] and row[index_diameter[1][counter]] and not row_empty:
                    try:
                        input_values[charge_key][key]['d_f'].append(unit_conversion(float(row[index_diameter[1][counter]]),
                                                                                    row[index_diameter[1][counter]+1],'length'))
                    except ValueError:
                        warning = ('Check value in row '+str(reader.line_num)+' and columns '
                                   +column_diameter[1][counter]+' ('+str(index_diameter[1][counter]+1)+')')
                        break
                else:
                    input_values[charge_key][key]['d_f'].append(d_f_R)
    for key_1 in input_values:
        if  isinstance(input_values[key_1],dict):
            for key_2 in input_values[key_1]:
                if  isinstance(input_values[key_1][key_2],dict):
                    for key_3 in input_values[key_1][key_2]:
                        input_values[key_1][key_2][key_3] = np.transpose(np.atleast_2d(input_values[key_1][key_2][key_3]))
                else:
                    input_values[key_1][key_2] = np.transpose(np.atleast_2d(input_values[key_1][key_2]))
    results = sigma_fitting(input_values)
    return(results,warning)