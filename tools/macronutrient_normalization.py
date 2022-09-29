# Author: A.Wachholz
# Date: 11.02.22

"""
"""

# imports
import numpy as np
import pandas as pd

# define constants
# * atomic weights of Carbon, Nitrogen and Phosphorus
AU_C = 12.010
AU_N = 14.007
AU_P = 30.974
# * nutrient ratios
REDFIELD = (106, 16, 1)
GODWIN_COTNER = (68, 14, 1)

# define functions


def ternary_normalization(c_array, n_array, p_array, ratio=REDFIELD):
    """
    Normalizes C, N, P concentrations according to a give molar ratio (C:N:P),
    e.g.
        * 'redfield' = 106:16:1
            (
                On the proportions of organic derivatives in sea water and their
                relation to the composition of plankton, Redfield 1934
            )
        * 'godwin_cotner' = 68:14:1
            (doi: 10.1038/ismej.2017.195)

    see Graeber et al., 2021 (https://doi.org/10.1007/s10533-021-00809-4) for
    further details

    Parameters
    ----------
    c_array : 1d numpy array/ list
        contains dissolved organic carbon (DOC) concentrations in mg/l.
    n_array : 1d numpy array / list
        contains no3-n concentrations in mg/l.
    p_array : 1d numpy array / list
        contains po4-p concentrations in mg/l.
    ratio : 3-tuple w/ C:N:P ratio, e.g. (106, 16, 1) for Redfield

    Returns
    -------
    export_array : numpy nd array
        column 1 is C, column 2 is N, column 3 is P, each normalized (0, 100)
        according to the defined ratio

    """

    # input arrays into pandas dataframe
    cnp = pd.DataFrame(zip(c_array, n_array, p_array))
    cnp.columns = ['C', 'N', 'P']

    # mg/l -> mmol/l
    cnp['mmolC'] = cnp['C'] / AU_C
    cnp['mmolN'] = cnp['N'] / AU_N
    cnp['mmolP'] = cnp['P'] / AU_P

    # calculate ratio
    cnp['C_ratio'] = cnp.mmolC
    cnp['N_ratio'] = cnp.mmolN * (ratio[0]/ratio[1])
    cnp['P_ratio'] = cnp.mmolP * ratio[0]

    # normalize ratios
    cnp['Ratio_sum'] = cnp.C_ratio + cnp.N_ratio + cnp.P_ratio
    cnp['C_r'] = cnp.C_ratio / cnp.Ratio_sum * 100
    cnp['N_r'] = cnp.N_ratio / cnp.Ratio_sum * 100
    cnp['P_r'] = cnp.P_ratio / cnp.Ratio_sum * 100

    # export: watch out for different order of nutrients!
    # (this is done to make plotting easier)
    export_array = np.asarray(cnp[['N_r', 'C_r', 'P_r']])

    return export_array


if __name__ == '__main__':

    # test ternary_normalization function
    # * build c, n and p concentrations according to redfield ratio
    c_value = 10
    n_value = c_value / ((REDFIELD[0]/REDFIELD[1] / AU_N) * AU_C)
    p_value = c_value / ((REDFIELD[0]/ AU_P) * AU_C)

    # define test input, target and func to be tested
    test_input = [[c_value], [n_value], [p_value]]
    func = ternary_normalization
    target = 100/3

    # run test
    test_return = func(
        c_array=test_input[0],
        n_array=test_input[1],
        p_array=test_input[2],
        ratio=REDFIELD
    )

    # evaluate results
    for t in test_return[0]:
        if np.round(t, 2) == np.round(target, 2):
            pass
        else:
            raise ValueError('unit test for', func.__name__, 'failed')

