
# coding: utf-8

# In[ ]:

def unit_conversion(input_value, unit, dimension):

    import scipy.constants as sc

    if dimension == 'length':
        if unit.lower() == 'nm':
            value = input_value*sc.nano
        elif unit.lower() == 'μm' or unit.lower() == 'um':
            value = input_value*sc.micro
        elif unit.lower() == 'mm':
            value = input_value*sc.milli
        elif unit.lower() == 'cm':
            value = input_value*sc.centi
        elif unit.lower() == 'm':
            value = input_value
        elif unit.lower() == 'mil':
            value = input_value*sc.mil
        elif unit.lower() == 'in':
            value = input_value*sc.inch
        elif unit.lower() == 'ft':
            value = input_value*sc.foot
        else: 
            raise ValueError
    elif dimension == 'temperature':
        if unit.lower() == 'k':
            value = input_value
        elif unit.lower() == 'c':
            value = sc.convert_temperature(input_value,'C','K')
        elif unit.lower() == 'f':
            value = sc.convert_temperature(input_value,'F','K')
        else:
            raise ValueError
    elif dimension == 'pressure':
        if unit.lower() == 'pa':
            value = input_value
        elif unit.lower() == 'kpa':
            value = input_value*sc.kilo
        elif unit.lower() == 'atm':
            value = input_value*sc.atm
        else:
            raise ValueError
    elif dimension == 'velocity':
        if unit.lower() == 'cm/s':
            value = input_value*sc.centi
        elif unit.lower() == 'm/s':
            value = input_value
        elif unit.lower() == 'ft/min':
            value = input_value*sc.foot/sc.minute
        else:
            raise ValueError
    return value

