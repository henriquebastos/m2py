#!/usr/bin/env python
# -*- coding: utf-8 -*-

import __xsteam__ as xst


def tsat_p(p):
    """
    Saturation Temperature as function of Pressure [kPa]

    :param p:
    :return:
    """
    global fromSIunit_T

    # Kpa to MPa
    p = p / 1000.0

    if 0.000611657 < p < 22.06395:
        out = xst.fromSIunit_T(xst.T4_p(p))
    else:
        out = None
    return out


def tsat_s(s):
    """
    Saturation Temperature as Function of Entropy [°C]

    :param s:
    :return:
    """
    s = xst.toSIunit_s(s)
    if -0.0001545495919 < s < 9.155759395:
        ps = xst.p4_s(s)
        Out = xst.fromSIunit_T(xst.T4_p(ps))
    else:
        Out = None

    return Out


# case 'psat_t'
def psat_t(T):
    """
    Saturation Pressure as function of Temperature [kPa]

    :param T: Temperature in degC
    :return:  Saturation Pressure in kPa
    """

    T = xst.toSIunit_T(T)
    if 647.096 > T > 273.15:
        # Out = x.fromSIunit_p(x.p4_T(T))
        Out = xst.p4_T(T) * 1000.0
    else:
        Out = None

    return Out


def psat_s(s):
    """
    Saturation Pressure as Function of entropy [kPa]

    :param s:
    :return:
    """
    s = xst.toSIunit_s(s)
    if -0.0001545495919 < s < 9.155759395:
        Out = xst.p4_s(s) * 1000.0
    else:
        Out = None

    return Out


# case 'h_pt'
def h_pt(p, T):
    """

    :param p: Pressure in kPa
    :param T: Temperature in K
    :return:  Enthalpy in kJ/kg.K
    """

    # p = xst.toSIunit_p(p)
    p /= 1e3
    T = xst.toSIunit_T(T)
    Region = xst.region_pT(p, T)

    print "Region = ", Region

    if Region == 1:
        Out = xst.fromSIunit_h(xst.h1_pT(p, T))
    elif Region == 2:
        Out = xst.fromSIunit_h(xst.h2_pT(p, T))
    elif Region == 3:
        Out = xst.fromSIunit_h(xst.h3_pT(p, T))
    elif Region == 4:
        Out = None
    elif Region == 5:
        Out = xst.fromSIunit_h(xst.h5_pT(p, T))
    else:
        Out = None

    return Out


def hv_t(T):
    """
    Saturated Steam Entalphy as function of Temperature

    :param T: Temperature in °C
    :return:  Enthalpy in kJ/(kg.K)
    """
    T = xst.toSIunit_T(T)

    if T > 273.15 and T < 647.096:
        p = xst.p4_T(T)
        Out = xst.fromSIunit_h(xst.h4V_p(p))
    else:
        Out = None

    return Out


def h_px(p, x):
    """
    :param p: Pressure in kPa
    :param x:
    :return:
    """
    global xst

    p = xst.toSIunit_p(p)
    xst = xst.toSIunit_x(x)

    if xst > 1 or xst < 0 or p >= 22.064:
        Out = None
        return

    hL = xst.h4L_p(p)
    hV = xst.h4V_p(p)
    Out = hL + x * (hV - hL)
    return Out


def h_tx(T, x):
    """
    Entalphy of Saturated Steam as function of T and x
    
    :param T: Temperature in °C 
    :param x: Vapor Quality 0 <= x <= 1
    :return:  Enthalphy  kJ/kg.K 
    """
    T = xst.toSIunit_T(T)
    x = xst.toSIunit_x(x)
    if x > 1 or x < 0 or T >= 647.096:
        return

    p = xst.p4_T(T)
    hL = xst.h4L_p(p)
    hV = xst.h4V_p(p)
    Out = hL + x * (hV - hL)
    return Out


def x_ph(p, h):
    p = p / 1000
    h = xst.toSIunit_h(h)

    if p > 0.000611657 and p < 22.06395:
        Out = xst.fromSIunit_x(xst.x4_ph(p, h))
    else:
        Out = None

    return Out


# case {'v_pt','rho_pt'}


def v_pt(p, T):
    """
    Superheated Steam specific Volume as function of p and T

    :param p: Absolute Pressure in kPa
    :param T: Temperatur
    :return:  v Specific Volume of Superheated Steam in m3/kg
    """

    p = p / 1000.0
    # p = xst.toSIunit_p(p)
    T = xst.toSIunit_T(T)

    Region = xst.region_pT(p, T)

    print "Region  = ", Region

    if Region == 1:
        Out = xst.v1_pT(p, T)
    elif Region == 2:
        Out = xst.v2_pT(p, T)
    elif Region == 3:
        Out = xst.v3_ph(p, xst.h3_pT(p, T))
    elif Region == 4:
        Out = None
    elif Region == 5:
        Out = xst.v5_pT(p, T)
    else:
        Out = None

    return Out


def vl_t(T):
    T = xst.toSIunit_T(T)
    if  T > 273.15  and T < 647.096:
        if  T <= 623.15:
            Out = xst.v1_pT(xst.p4_T(T), T)
        else:
            Out = xst.v3_ph(xst.p4_T(T), xst.h4L_p(xst.p4_T(T)))

    else:
        Out = None
    return Out


def sv_p(p):
    from __xsteam__ import toSIunit_p, fromSIunit_s, s2_pT, T4_p, s3_rhoT, v3_ph, h4V_p

    p = p/1000.0

    if  p > 0.000611657  and p < 22.06395:
        if  p < 16.529:
            Out = fromSIunit_s(s2_pT(p, T4_p(p)))
        else:
            Out = fromSIunit_s(s3_rhoT(1 / (v3_ph(p, h4V_p(p))), T4_p(p)))

    else:
        Out = None

    return Out

def s_pt(p, T):
    from __xsteam__ import toSIunit_p, toSIunit_T, region_pT, v3_ph, h3_pT
    from __xsteam__ import fromSIunit_s, s1_pT, s2_pT, h3_rhoT, s5_pT, s3_rhoT
    p = p/1000.0
    T = toSIunit_T(T)

    Region = region_pT(p, T)


    if Region ==  1:
        Out = s1_pT(p, T)
    elif Region ==  2:
        Out = s2_pT(p, T)
    elif Region ==  3:
        hs = h3_pT(p, T)
        rhos = 1 / v3_ph(p, hs)
        Out = s3_rhoT(rhos, T)
    elif Region ==  4:
        Out = None
    elif Region ==  5:
        Out = s5_pT(p, T)
    else:
        Out = None

    return Out

def t_ph(p, h):
    
    p = p/1000.0
    h = xst.toSIunit_h(h)
    
    Region = xst.region_ph(p, h)
    
    if Region == 1:
        Out = xst.fromSIunit_T(xst.T1_ph(p, h))
    elif 2:
        Out = xst.fromSIunit_T(xst.T2_ph(p, h))
    elif 3:
        Out = xst.fromSIunit_T(xst.T3_ph(p, h))
    elif 4:
        Out = xst.fromSIunit_T(xst.T4_p(p))
    elif 5:
        Out = xst.fromSIunit_T(xst.T5_ph(p, h))
    else:
        Out = None

    return Out



# def v_ph(p h):
#
#     p = p/1000.0
#     h = h
#     Region = xst.region_ph(p, h)
#
#
#     if Region ==  1:
#         Out = v1_pT(p, T1_ph(p, h))
#     elif Region ==  2:
#         Out = v2_pT(p, T2_ph(p, h))
#     elif Region ==  3:
#         Out = v3_ph(p, h)
#     elif Region ==  4:
#         xs = x4_ph(p, h)
#         if  p < 16.529:
#             v4v = v2_pT(p, T4_p(p))
#             v4L = v1_pT(p, T4_p(p))
#         else:
#             v4v = v3_ph(p, h4V_p(p))
#             v4L = v3_ph(p, h4L_p(p))
#
#         Out = fromSIunit_v((xs * v4v + (1 - xs) * v4L))
#     elif Region ==  5:
#         Ts = T5_ph(p, h)
#         Out = v5_pT(p, Ts)
#     else:
#         Out = None
#
#     return Out



print v_pt(100.0, 300)

print v_pt(100.0, 1000)

print s_pt(100, 1000)

print t_ph(100, 4640.31)