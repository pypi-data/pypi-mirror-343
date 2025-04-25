import numpy as np
from .helpers import expand_dims, match_dims, standard_seawater, calc_Istr, calc_KF, calc_KS
from .params import TABLES, calc_lambda_zeta, calc_seawater_ions, get_ion_index, calc_ionpair_association, CATION_CHG, ANION_CHG, ION_IND, N_CATION, N_ANION

# TODO: new file for user-facing functions.

def calc_gKs(TC, Sal, Na=None, K=None, Ca=None, Mg=None, Sr=None, Cl=None, BOH4=None, HCO3=None, CO3=None, SO4=None,
                  beta_0=None, beta_1=None, beta_2=None, C_phi=None, Theta_negative=None, Theta_positive=None, Phi_NNP=None, Phi_PPN=None):
    """
    Calculates activity coefficient (gamma) ratios to apply to stoichiometric Ks using MyAMI model.

    Parameters
    ----------
    TC : array-like
        Temperature in Celcius
    Sal : array-like
        Salinity
    Na, K, Ca, Mg, Sr, Cl, BOH4, HCO3, CO3, SO4 : array-like
        Average concentration of ions in seawater in mol kg-1, by default None
        If none, values are calculated from salinity using seawater composition of
        Millero et al., 2008.
    beta_0, beta_1, beta_2, C_phi : numpy.NDarray
        Matrices of ion interaction coefficients from tables A1-A9 of
        Millero and Pierrot (1998; doi:10.1023/A:1009656023546) provided
        by the params.PitzerParams function.
    Theta_negative, Theta_positive, Phi_NNP, Phi_PPN : numpy.NDarray
        Matrices of ion interaction coefficients from tables A10 and A11 of
        Millero and Pierrot (1998; doi:10.1023/A:1009656023546) provided
        by the params.PitzerParams function.

    Returns
    -------
    dict of array-like
        Containing {gKspC, gKspA, gK1, gK2, gKW, gKB, gK0, gKS}
    """

    TK = TC + 273.15
    Istr = calc_Istr(Sal)
    m_cation, m_anion = calc_seawater_ions(Sal, Na=Na, K=K, Mg=Mg, Ca=Ca, Sr=Sr, Cl=Cl, BOH4=BOH4, HCO3=HCO3, CO3=CO3, SO4=SO4)

    gammas, alphas = calc_gamma_alpha(
        TK=TK, Sal=Sal, Istr=Istr, m_cation=m_cation, m_anion=m_anion, 
        beta_0=beta_0, beta_1=beta_1, beta_2=beta_2, C_phi=C_phi,
        Theta_negative=Theta_negative, Theta_positive=Theta_positive,
        Phi_NNP=Phi_NNP, Phi_PPN=Phi_PPN)

    gammaT_OH = gammas['anion'][0] * alphas['OH']
    gammaT_BOH4 = gammas['anion'][2]
    gammaT_HCO3 = gammas['anion'][3]
    gammaT_CO3 = gammas['anion'][5] * alphas['CO3']
    
    gammaT_Ht = gammas['cation'][0] * alphas['Ht']  # remove the alpha to put everything on free scale?
    gammaT_Ca = gammas['cation'][4]

    gammaCO2_gammaB = calc_gammaCO2_gammaB(TK, m_anion, m_cation)

    out = {
    'gKspC': 1 / gammaT_Ca / gammaT_CO3,
    'gKspA': 1 / gammaT_Ca / gammaT_CO3,
    'gK1': 1 / gammaT_Ht / gammaT_HCO3 * gammaCO2_gammaB['gammaCO2'],
    'gK2': 1 / gammaT_Ht / gammaT_CO3 * gammaT_HCO3,
    'gKW': 1 / gammaT_Ht / gammaT_OH,
    'gKB': 1 / gammaT_BOH4 / gammaT_Ht * gammaCO2_gammaB['gammaB'],
    'gK0': 1 / gammaCO2_gammaB['gammaCO2'] * gammaCO2_gammaB['gammaCO2gas'],
    'gKS': 1 / gammas['anion'][6] / gammaT_Ht * gammas['anion'][4],
    }

    return out

def calc_A_phi(TK):
    """
    Calculate A_phi from equation A10 of Millero and Pierrot (1998; doi:10.1023/A:1009656023546).
    
    Parameters
    ----------
    TK : array-like
        Temperature in Kelvin
    """
    # TODO: put these in an external file?
    return (
        3.36901532e-01
        - 6.32100430e-04 * TK
        + 9.14252359 / TK
        - 1.35143986e-02 * np.log(TK)
        + 2.26089488e-03 / (TK - 263)
        + 1.92118597e-6 * TK * TK
        + 4.52586464e01 / (680 - TK)
    )  
    
    # relic comment from original MyAMI code:
        # note correction of last parameter, E + 1 instead of E-1
        # A_phi = 8.66836498e1 + 8.48795942e-2 * T - 8.88785150e-5 * T * T +
        # 4.88096393e-8 * T * T * T -1.32731477e3 / T - 1.76460172e1 * np.log(T)
        # # Spencer et al 1990


# # Equation in line with Simonson88:
# def calc_BMX_2_2(cat, an, beta_0, beta_1, beta_2, Istr, sqrtI):
#     """Calculate BMX_phi, BMX and BMX_apostrophe for 2-2 electrolytes.

#     The formulation is given in Eqns A15-A17 of Miller and Pierrot (1998; doi:10.1023/A:1009656023546).
    
#     Following Hain et al. (2008; doi:10.1029/2007JC002651), the value of alpha_2 differs for SO4 and B(OH)4.
    
#     alpha_2 is used as determined by Simonson (1988; doi:10.1029/J90-D01010), and is 6 for B(OH)4 and 12 for SO4.
#     However, Simonson does not provide equations for BMX_phi and BMX_apostrophe, so these formulations are taken
#     from Miller and Pierrot (1998; doi:10.1023/A:1009656023546).
    
#     Parameters
#     ----------
#     cat : int
#         numeric index of the cation.
#     an : int
#         numeric index of the anion.
#     beta_0, beta_1, beta_2 : float
#         coefficients to calculate BMX values
#     Istr : _type_
#         Ionic strength of solution
#     sqrtI : _type_
#         Sqare root of ionic strength of solution

#     Returns
#     -------
#     tuple
#         (BMX_phi, BMX, BMX_apostrophe)
#     """
    
#     alpha_1 = 1.4
#     # the value of alpha_2 depends on the anion (see Simonson88)
#     if an == 2:  # B(OH)4 case
#         alpha_2 = 6.
#     if an == 6:  # SO4 case
#         alpha_2 = 12.
    
#     # What is BMX_phi?
#     BMX_phi = (
#         beta_0[cat, an] + 
#         beta_1[cat, an] * np.exp(-alpha_1 * sqrtI) + 
#         beta_2[cat, an] * np.exp(-alpha_2 * sqrtI)
#         )  # Eq. A15
    
#     # This is the quantity calculated in Simonson88 Eq. 5   
#     BMX = (
#         beta_0[cat, an] + 
#         beta_1[cat, an] * 2 / (alpha_1**2 * Istr) * (1 - (1 + alpha_1 * sqrtI) * np.exp(-alpha_1 * sqrtI)) + 
#         beta_2[cat, an] * 2 / (alpha_2**2 * Istr) * (1 - (1 + alpha_2 * sqrtI) * np.exp(-alpha_2 * sqrtI))
#         )  # Eq. A16
    
#     # Simonson also specifies the CMX is different for 2-2 electrolytes, but this was not used in Miller and Pierrot (1998; doi:10.1023/A:1009656023546).
#     # CMX = CMX_phi / 2 * sqrt(z_M * z_X)
    
#     # BMX_apostroph defined in Simonson88 Eq. 11 (which only apply to solutes where beta_0 == 0).
#     BMX_apostroph = (
#         beta_1[cat, an] * 2 / (alpha_1**2 * Istr**2) * (-1 + (1 + alpha_1 * sqrtI + alpha_1**2 * Istr / 2) * np.exp(-alpha_1 * sqrtI)) + 
#         beta_2[cat, an] * 2 / (alpha_2**2 * Istr   ) * (-1 - (1 + alpha_2 * sqrtI + alpha_2**2 * Istr / 2) * np.exp(-alpha_2 * sqrtI))
#         )   # Eq. A17

#     return BMX_phi, BMX, BMX_apostroph

def calc_gamma_alpha(TK, Sal, Istr, m_cation, m_anion,
                  beta_0=None, beta_1=None, beta_2=None, C_phi=None, Theta_negative=None, Theta_positive=None, Phi_NNP=None, Phi_PPN=None):
    """Calculate Gammas and Alphas for K calculations.

    Parameters
    ----------
    TK : array-like
        Temperature in Kelvin
    S : array-like
        Salinity in PSU
    Istr : array-like
        Ionic strength of solution
    m_cation : array-like
        Matrix of major cations in seawater in mol/kg in order:
        [H, Na, K, Mg, Ca, Sr]
    m_anion : array-like
        Matrix of major anions in seawater in mol/kg in order:
        [OH, Cl, B(OH)4, HCO3, HSO4, CO3, SO4]

    Returns
    -------
    tuple of dicts
        (gammas: {cations, anions},
         alphas: {Hsws, Ht, OH, CO3})
    """
    # TODO: Derive this from paper tables?
    
    # Testbed case T=25C, I=0.7, seawatercomposition
    sqrtI = np.sqrt(Istr)
    
    # make tables of ion charges used in later calculations

    # cation order: [H, Na, K, Mg, Ca, Sr]
    Z_cation = np.full(
        (CATION_CHG.size, *TK.shape),
        expand_dims(CATION_CHG, TK)
        )

    # anion order: [OH, Cl, B(OH)4, HCO3, HSO4, CO3, SO4]
    Z_anion = np.full(
        (ANION_CHG.size, *TK.shape),
        expand_dims(ANION_CHG, TK)
        )
    
    A_phi = calc_A_phi(TK=TK)  # Eq A10

    f_gamma = -A_phi * (sqrtI / (1 + 1.2 * sqrtI) + (2 / 1.2) * np.log(1 + 1.2 * sqrtI))  # Eq A9

    # E_cat = sum(m_cation * Z_cation)
    E_an = -sum(m_anion * Z_anion)
    E_cat = -E_an  # this enforces charge balance.

    # Calculate second and third virial coefficients
    
    # functional forms combined from Simonson 1988 (alpha_1 and alpha_2) and Miller and Pierrot (1998), Eq A11-A17
    alpha_1 = np.full(beta_0.shape, 2.0)  # alpha_1 is 2 for single ion pairs (Eq A11-A13)
    
    # alpha_1 for 2-2 pairs is 1.4 (Eq A15-A17)
    alpha_1[tuple(zip(*[
        get_ion_index('Mg-B(OH)4'),
        get_ion_index('Ca-B(OH)4'),
        get_ion_index('Sr-B(OH)4'),
        get_ion_index('Mg-SO4'),
        get_ion_index('Ca-SO4'),
    ]))] = 1.4
    
    alpha_2 = np.full(beta_0.shape, 12.0)  # alpha_2 is 12 for single ion pairs (Eq A11-A13)
    
    # alpha_2 is 6 for borate pairs (Simonson 1988)
    alpha_2[tuple(zip(*[
        get_ion_index('Mg-B(OH)4'),
        get_ion_index('Ca-B(OH)4'),
        get_ion_index('Sr-B(OH)4'),
    ]))] = 6.0
    
    
    # BMX_phi = (
    #     beta_0 + 
    #     beta_1 * np.exp(-alpha_1 * sqrtI) + 
    #     beta_2 * np.exp(-alpha_2 * sqrtI)
    #     )  # Eq. A11 and A15
    
    BMX = (
        beta_0 + 
        beta_1 * 2 / (alpha_1**2 * Istr) * (1 - (1 + alpha_1 * sqrtI) * np.exp(-alpha_1 * sqrtI)) + 
        beta_2 * 2 / (alpha_2**2 * Istr) * (1 - (1 + alpha_2 * sqrtI) * np.exp(-alpha_2 * sqrtI))
        )  # Eq. A12 and A16
    
    # Note: the equations in the paper just show constants calculated from fixed values of alpha_1
    # and alpha_2.
    # The calculations here are equivalent to the paper, but write out the full pitzer equations for
    # using alpha_1 and alpha_2. 
    
    BMX_apostroph = (
        beta_1 * 2 / (alpha_1**2 * Istr**2) * (-1 + (1 + alpha_1 * sqrtI + alpha_1**2 * Istr / 2) * np.exp(-alpha_1 * sqrtI)) + 
        beta_2 * 2 / (alpha_2**2 * Istr   ) * (-1 - (1 + alpha_2 * sqrtI + alpha_2**2 * Istr / 2) * np.exp(-alpha_2 * sqrtI))
        )   # Eq. A13 and A17

    CMX = C_phi / (2 * np.sqrt(-np.expand_dims(Z_anion, 0) * np.expand_dims(Z_cation, 1)))  # Eq. A14

    # TODO: ask Mathis about typo
    # keep sqrtI -> Istr typo so that tests keep passing
    # BMX_apostroph = (
    #     beta_1 * 2 / (alpha_1**2 * Istr**2) * (-1 + (1 + alpha_1 * sqrtI + alpha_1**2 * sqrtI / 2) * np.exp(-alpha_1 * sqrtI)) + 
    #     beta_2 * 2 / (alpha_2**2 * Istr   ) * (-1 - (1 + alpha_2 * sqrtI + alpha_2**2 * sqrtI / 2) * np.exp(-alpha_2 * sqrtI))
    #     )   # Eq. A13 and A17
    
    # old calculations
    # BMX_phi = beta_0 + beta_1 * np.exp(-2 * sqrtI)  # Eq. A11
    # BMX = beta_0 + (beta_1 / (2 * Istr)) * (1 - (1 + 2 * sqrtI) * np.exp(-2 * sqrtI))  # Eq. A12
    # NOTE: Typo in original -                                                 v    should be Istr!!
    # BMX_apostroph = (beta_1 / (2 * Istr**2)) * (-1 + (1 + (2 * sqrtI) + (2 * sqrtI)) * np.exp(-2 * sqrtI))  # Eq. A13
    # CMX = C_phi / (2 * np.sqrt(-np.expand_dims(Z_anion, 0) * np.expand_dims(Z_cation, 1)))  # Eq. A14

    # # H-SO4
    # # TODO: unclear how this comes from Clegg et al, 1994...
    # # This does nothing because beta params for for H-SO4 are all zeros -
    # # they're commented out in TabA9 because they were not used in MyAMI.
    # cat, an = get_ion_index('H-SO4')
    # # BMX* is calculated with T-dependent alpha for H-SO4; see Clegg et al.,
    # # 1994 --- Millero and Pierrot are completly off for this ion pair
    # xClegg = (2 - 1842.843 * (1 / TK - 1 / 298.15)) * sqrtI
    # # xClegg = (2) * sqrtI
    # gClegg = 2 * (1 - (1 + xClegg) * np.exp(-xClegg)) / (xClegg * xClegg)
    # # alpha = (2 - 1842.843 * (1 / T - 1 / 298.15)) see Table 6 in Clegg et al 1994
    # BMX[cat, an] = beta_0[cat, an] + beta_1[cat, an] * gClegg
    # BMX_apostroph[cat, an] = beta_1[cat, an] / Istr * (np.exp(-xClegg) - gClegg)

    # C1_HSO4 = 0  # TODO: If this is zero, CMX is not modified.
    # CMX[cat, an] = (
    #     C_phi[cat, an] + 4 * C1_HSO4 * 
    #     (6 - (6 + 2.5 * sqrtI * (6 + 3 * 2.5 * sqrtI + 2.5 * sqrtI * 2.5 * sqrtI)) *
    #     np.exp(-2.5 * sqrtI)) / 
    #     (.5 * sqrtI * 2.5 * sqrtI * 2.5 * sqrtI * 2.5 * sqrtI)
    #     )  # w = 2.5 ... see Clegg et al., 1994

    # unusual alpha=1.7 for Na2SO4  # TODO: where does this come from?
    # BMX[1, 6] = beta_0[1, 6] + (beta_1[1, 6] / (2.89 * Istr)) * 2 * (1 - (1 + 1.7 * sqrtI) * np.exp(-1.7 * sqrtI))
    # BMX[1, 6] = beta_0[1, 6] + (beta_1[1, 6] / (1.7 * Istr)) * (1 - (1 + 1.7 * sqrtI) * np.exp(-1.7 * sqrtI))

    # BMX[4, 6] =BMX[4, 6] * 0  # knock out Ca-SO4
    
    ################################################################################
    # Calculate gamma_anion and gamma_cation from BMX and CMX    
    ################################################################################
    
    # anion * cation * BMX or CMX matrices  TODO: how do these relate to Eq A18-  ?
    mR = (m_anion * np.expand_dims(m_cation, 1) * BMX_apostroph).sum((0,1))
    mS = (m_anion * np.expand_dims(m_cation, 1) * CMX).sum((0,1))

    # ln_gammaCl = Z_anion[1] * Z_anion[1] * f_gamma + R - S

    # Original ln_gamma_anion calculation loop:
    ln_gamma_anion = Z_anion * Z_anion * (f_gamma + mR) + Z_anion * mS
    for an in range(0, N_ANION):
        for cat in range(0, N_CATION):
            ln_gamma_anion[an] += 2 * m_cation[cat] * (
                BMX[cat, an] + E_cat * CMX[cat, an]
            )
        for an2 in range(0, N_ANION):
            ln_gamma_anion[an] += m_anion[an2] * (
                2 * Theta_negative[an, an2]
            )
        for an2 in range(0, N_ANION):
            for cat in range(0, N_CATION):
                ln_gamma_anion[an] += (
                    m_anion[an2] * m_cation[cat] * Phi_NNP[an, an2, cat]
                )
        for cat in range(0, N_CATION):
            for cat2 in range(cat + 1, N_CATION):
                ln_gamma_anion[an] += (
                    m_cation[cat] * m_cation[cat2] * Phi_PPN[cat, cat2, an]
                )
    
    # vectorised ln_gamma_anion calculation:
    # TODO: Runs into memory problems with large inputs. Could be simplified further? 
    # cat, cat2 = np.triu_indices(6, 1)
    # ln_gamma_anion = (
    #     Z_anion * Z_anion * (f_gamma + R) + Z_anion * S + 
    #     (2 * np.expand_dims(m_cation, 1) * (BMX + E_cat * CMX)).sum(0) + 
    #     (np.expand_dims(m_anion, 1) * 2 * Theta_negative).sum(0) + 
    #     (np.expand_dims(m_anion, (0,2)) * np.expand_dims(m_cation, (0,1)) * Phi_NNP).sum(axis=(1,2)) +
    #     (np.expand_dims(m_cation[cat], 1) * np.expand_dims(m_cation[cat2], 1) * Phi_PPN[cat, cat2]).sum(axis=0)
    # )  
    gamma_anion = np.exp(ln_gamma_anion)


    # ln_gammaCl = Z_anion[1] * Z_anion[1] * f_gamma + R - S

    # Original ln_gamma_cation calculation loop:
    ln_gamma_cation = Z_cation * Z_cation * (f_gamma + mR) + Z_cation * mS
    for cat in range(0, N_CATION):
        for an in range(0, N_ANION):
            ln_gamma_cation[cat] += 2 * m_anion[an] * (
                BMX[cat, an] + E_cat * CMX[cat, an]
            )
        for cat2 in range(0, N_CATION):
            ln_gamma_cation[cat] += m_cation[cat2] * (2 * Theta_positive[cat, cat2])
        for cat2 in range(0, N_CATION):
            for an in range(0, N_ANION):
                ln_gamma_cation[cat] += (
                    m_cation[cat2] * m_anion[an] * Phi_PPN[cat, cat2, an]
                )
        for an in range(0, N_ANION):
            for an2 in range(an + 1, N_ANION):
                ln_gamma_cation[cat] += (
                    + m_anion[an] * m_anion[an2] * Phi_NNP[an, an2, cat]
                )

    # vectorised ln_gamma_cation calculation:
    # TODO: Runs into memory problems with large inputs. Could be simplified further? 
    # an, an2 = np.triu_indices(7, 1)
    # ln_gamma_cation = (
    #     Z_cation * Z_cation * (f_gamma + R) + Z_cation * S +
    #     (2 * np.expand_dims(m_anion, 0) * (BMX + E_cat * CMX)).sum(axis=1) +
    #     (np.expand_dims(m_cation, 1) * (2 * Theta_positive)).sum(axis=0) +
    #     (np.expand_dims(m_cation, (0,2)) * np.expand_dims(m_anion, (0,1)) * Phi_PPN).sum(axis=(1,2))+
    #     (np.expand_dims(m_anion[an], 1) * np.expand_dims(m_anion[an2], 1) * Phi_NNP[an, an2]).sum(axis=0)
    # )
    gamma_cation = np.exp(ln_gamma_cation)

    # choice of pH-scale = total pH-scale [H]T = [H]F + [HSO4]
    # so far gamma_H is the [H]F activity coefficient (= free-H pH-scale)
    # thus, conversion is required
    K_HSO4_conditional = calc_KS(TK=TK, Sal=Sal, Istr=Istr)
    K_HF_conditional = calc_KF(TK=TK, Sal=Sal)
    TF = 0.0000683 * Sal / 35
    TS = m_anion[6]
    
    alpha_Hsws = 1 / (1 + TS / K_HSO4_conditional + TF / K_HF_conditional)
    alpha_Ht = 1 / (1 + TS / K_HSO4_conditional)

    # A number of ion pairs are calculated explicitly: MgOH, CaCO3, MgCO3, SrCO3
    # since OH and CO3 are rare compared to the cations the anion alpha (free /
    # total) are assumed to be unity
    gamma_MgCO3 = gamma_CaCO3 = gamma_SrCO3 = 1

    ii = get_ion_index('Mg-OH')
    # TODO: can't see a clean way to get around hard-coding this parameter, as it isn't imported in the Phi_NNP array... why?
    Phi_MgOH = 0.028  # from Table A11 MgOH-Mg-OH interaction parameter
    ln_gamma_MgOH = (
        1 * (f_gamma + mR) + 1 * mS +
        2 * m_anion[1] * (BMX[ii[0], ii[1]] + E_cat * CMX[ii[0], ii[1]]) +  # interaction between MgOH-Cl affects MgOH gamma
        m_cation[3] * m_anion[1] * Phi_MgOH  # interaction between MgOH-Mg-OH affects MgOH gamma
    )
    gamma_MgOH = np.exp(ln_gamma_MgOH)
    
    # Correct OH and CO3 gammas for ion pairing - section 7 & 8 and Table II of Millero and Pierrot (1998)
    Kion = calc_ionpair_association(TK)
    
    K_MgOH = Kion['MgOH+'] / (gamma_cation[3] * gamma_anion[0] / gamma_MgOH)
    
    alpha_OH = 1 / (1 + (m_cation[3] / K_MgOH))
    
    K_MgCO3 = Kion['MgCO3'] / (gamma_cation[3] * gamma_anion[5] / gamma_MgCO3)
    K_CaCO3 = Kion['CaCO3'] / (gamma_cation[4] * gamma_anion[5] / gamma_CaCO3)
    K_SrCO3 = Kion['SrCO3'] / (gamma_cation[5] * gamma_anion[5] / gamma_SrCO3)

    alpha_CO3 = 1 / (1 + (m_cation[3] / K_MgCO3) + (m_cation[4] / K_CaCO3) + (m_cation[5] / K_SrCO3))

    return ({'cation': gamma_cation, 'anion': gamma_anion}, 
            {'Hsws': alpha_Hsws, 'Ht': alpha_Ht, 'OH': alpha_OH, 'CO3': alpha_CO3})

def calc_gammaCO2_gammaB(TK, m_an, m_cat):
    """
    Calculate gammaCO2 and gammaB

    Parameters
    ----------
    TC : array-like
        Temperature in Kelvin, used to determine array shapes
    m_an : dict
        Containing cation concentrations in mol/kgsw 
    m_cat : dict
        Containing anion concentrations in mol/kgsw

    Returns
    -------
    dict
        Containing {gammaCO2, gammaCO2gas, gammaB}
    """

    cations = ['H', 'Na', 'K', 'Mg', 'Ca']
    anions = ['Cl', 'SO4']
    
    m_cation = np.array([m_cat[ION_IND[c]] for c in cations])
    m_anion = np.array([m_an[ION_IND[a]] for a in anions])
    m_ion = np.concatenate([m_cation, m_anion])
    
    m_zeta = (np.expand_dims(m_anion,1) * np.expand_dims(m_cation,0))  # matrix for zeta calculation
        
    lambda_zeta = calc_lambda_zeta(TK)
    
    lambdaCO2 = lambda_zeta['lambdaCO2']
    zetaCO2 = lambda_zeta['zetaCO2']  # not used in Hain's MyAMI?
    lambdaB = lambda_zeta['lambdaB']
    zetaB = lambda_zeta['zetaB']
    
    ##########################
    # CALCULATION OF gammaCO2

    ln_gammaCO2 = (m_ion * 2 * lambdaCO2).sum(0)  # lambdaCO2
    # ln_gammaCO2 += (m_zeta * zetaCO2).sum((0,1))  # TODO: zetaCO2 not used in original MyAMI... why? Introduces small differences...
    gammaCO2 = np.exp(ln_gammaCO2)  # as according to He and Morse 1993

    # TODO: unclear where this comes from
    gammaCO2gas = np.exp(
        1 / (8.314462175 * TK *
            (0.10476 - 61.0102 / TK - 660000 / TK / TK / TK - 2.47e27 / np.power(TK, 12))
        )
    )

    ##########################
    # CALCULATION OF gammaB
        
    ln_gammaB = (m_ion * 2 * match_dims(lambdaB, m_ion)).sum(0)  # lambdaB
    ln_gammaB += (m_zeta * match_dims(zetaB, m_zeta)).sum()  # zetaB
    
    gammaB = np.exp(ln_gammaB)  # as according to Felmy and Wear 1986
    # print gammaB

    return {
        'gammaCO2': gammaCO2, 
        'gammaCO2gas': gammaCO2gas, 
        'gammaB': gammaB
        }