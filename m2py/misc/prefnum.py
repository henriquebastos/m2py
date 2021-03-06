#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python Wrapper to Prefnum.m
Requires Octave and octpy

 Round numeric vector to nearest preferred number/value, using inbuilt/custom number series.

 (c) 2012 Stephen Cobeldick

 ### Function ###

 Round the elements of a horizontal numeric vector to values chosen
 from a Preferred Number Series (PNS). The PNS may be one of:
 - Standard PNS (1-2-5, Renard and electronic IEC 60063 are inbuilt)
 - Custom PNS numeric vector (repeating every decade)
 - Custom PNS function (handle of a continuous function in one variable)

 Syntax:
  PfA = prefnum(InA,PfTok)      Select an inbuilt PNS (see tables below).
  PfA = prefnum(InA,PfVec)      Use a custom PNS numeric vector (fast).
  PfA = prefnum(InA,PfFun)      Use a custom PNS function (slow).
  [PfA,PfSet,EdgeSet,HistCnt] = prefnum(...)  PNS range, edges and bin count.

 If using an inbuilt PNS:
  - InA zero-value elements are returned as zero in PfA.
  - InA element values must be finite, real and positive.

 If using a custom numeric vector PNS:
  - InA zero-value elements are returned as zero in PfA.
  - InA element values must be finite, real and positive.
  - The PNS vector element values must be over one decade only,
    monotonic increasing, finite, real and positive.

 If using a custom PNS function handle:
  - The PNS function f(X) must be monotonic increasing with X.
  - Returns f(X) that are best matches to the InA values, for integer X values.
  - InA element values must be finite and real.
  - Solution is found using MATLAB's "fzero", the optional inputs may be passed as well.
  - An error 'No solution found for given preferred number series...' means
    that the given function and element value does not have a real solution.

 If the whole PNS domain can be calculated, then use "hist"/"histc" directly.

 See also ROUND HISTC HIST LOG10 FZERO

 ### Examples ###

 prefnum([514,7.6,37,0.9],'E6')     Electronic, six steps per decade.
   ans = [470,6.8,33,1]

 prefnum([514,7.6,37,0.9],'E12')    Electronic, twelve steps per decade.
   ans = [560,8.2,39,0.82]

 prefnum([514,7.6,37,0.9],'R10')    Renard, ten steps per decade.
   ans = [500,8.0,40,1]

 prefnum([514,7.6,37,0.9],'R"5')    Renard, five steps per decade, twice rounded.
   ans = [600,6.0,40,1]

 prefnum([514,7.6,37,0.9],'125')    1-2-5, three steps per decade.
   ans = [500,10,50,1]

 prefnum([514,7.6,37,0.9],[25,75])  Custom vector, two steps per decade.
   ans = [750,7.5,25,0.75]

 prefnum([514,7.6,37,0.9],1)        Custom vector, nearest order of magnitude.
   ans = [100,10,10,1]

 prefnum([514,7.6,37,0.9],@(x)2^x)  Custom function handle, nearest binary / power of two.
   ans = [512,8,32,1]

 [A,P,E] = prefnum(-11:11,@(x)3*x)  Custom function handle, nearest multiple of three.
  A = [-12,-9,-9,-9,-6,-6,-6,-3,-3,-3,0,0,0,3,3,3,6,6,6,9,9,9,12]
  P = [-12,-9,-6,-3,0,3,6,9,12]
  E = [-13.5,-10.5,-7.5,-4.5,-1.5,1.5,4.5,7.5,10.5,13.5]

 [A,P] = prefnum([5,300],'E12')     Electronic, nearest E12 values from 5 to 300.
  A = [4.7,330]
  P = [4.7,5.6,6.8,8.2,10,12,15,18,22,27,33,39,47,56,68,82,100,120,150,180,220,270,330]

 [~,~,E,H] = prefnum(1:149,'125',0) Draw a histogram with a bin width
 bar(H)                             that increases as a ~geometric series.
 L = arrayfun(@num2str,E,'UniformOutput',false)
 set(gca,'XTickLabel',strcat(L(1:end-1),'<',L(2:end)))

 ### Inbuilt PNS Tokens ###

 # 1-2-5

  PNS token: '125' (three steps per decade).
  Tolerance default = 0.36, giving minimum tolerance overlap/separation.

 # Electronic (IEC 60063) (resistors, capacitors, inductors, zener diodes...)

  PNS token:        | E6  | E12 | E24  | E48  | E96  | E192  |
  ------------------|-----|-----|------|------|------|-------|
  Tolerance default | 0.2 | 0.1 | 0.05 | 0.02 | 0.01 | 0.005 |

 # Renard (defined to three significant digits) (tolerance default = zero)

  PNS token: Basic | R5  | R10  | R20  | R40  | R80 |
  -----------------|-----|------|------|------|-----|
   "       Rounded | R'5 | R'10 | R'20 | R'40 |     |
  -----------------|-----|------|------|------|-----|
   " Twice Rounded | R"5 | R"10 | R"20 |      |     |

 ### Rounding and Tolerance ###

 If using an inbuilt PNS or a custom numeric vector PNS:
  The tolerance defines the rounding edges (selection boundaries), between
  which the input vector elements round to the best matching PNS value.
  The selection edges (see "histc") are generated from the PNS values and
  the PNS tolerance: edge_2 = average of (1+Tol)*PNS_1 and (1-Tol)*PNS_2.

          | Edges halfway between  | Examples:          (PNS = [20,30,60])
  --------|------------------------|--------------------------------------
  Tol = 0 | PNS values             | [..,25,45,130,..]             (Tol=0)
  --------|------------------------|--------------------------------------
  Tol > 0 | tolerance limit values | [..,23.25,41.25,112.5,..]  (Tol=0.25)

  The tolerance may be set using the optional third argument.

 If using a custom PNS function handle:
  The edges are function values at the midpoints between the PNS range values.
  Example: fn = @(x)2^x -> PNS = [1,2,4,..], edges = [0.7,1.41,2.82,..].

 ### Inputs and Outputs ###

 All numeric vectors are horizontal. Outputs are empty if no matches found.

 Outputs:
  PfA = InA elements rounded to nearest PNS value, numel = A.
  PfS = PNS range over all InA values (InA domain), numel = P.
  EdS = Edge values corresponding to PNS vector PfS, numel = P+1.
  HsA = Number of elements matching each PNS element, numel = P.
  HsI = Index of HsA, such that HsA(k) = sum(HsI==k), numel = A.
 Inputs:
  InA = Numeric vector, finite and real element values, numel = A.
  PfT = String, as per tables above, to select an inbuilt PNS.
      = Numeric vector, values are finite, positive, monotonic increasing and of
        the same order of magnitude to define a PNS that repeats every decade.
      = Function handle, a monotonic increasing function in one variable.
 If using an inbuilt PNS or a custom numeric vector PNS:
  In1 = Numeric scalar, *optional decimal tolerance value (eg 0.2 = 20),
        for a custom PNS vector the tolerance default = zero.
 If using a custom PNS function handle:
  In1 = Numeric scalar, *optional seed for MATLAB's "fzero", default = zero.
  In2 = Struct, *optional settings structure for MATLAB's "fzero" function.

 Outputs = [PfA,PfS,EdS,HsA]
 Inputs = (InA,PfT,In1*,In2*)
"""

import utils as u
import os
import oct2py as op

this_dir = u.this_dir()

#print "this_dir = ", this_dir

pwd = os.getcwd() # Save directory
os.chdir(this_dir)

oc = op.Oct2Py()

os.chdir(pwd)


def prefnum(InA,PfT):
    """

    :param InA:
    :param PfT:
    :return:
     ### Examples ###

         prefnum([514,7.6,37,0.9],'E6')     Electronic, six steps per decade.
           ans = [470,6.8,33,1]

         prefnum([514,7.6,37,0.9],'E12')    Electronic, twelve steps per decade.
           ans = [560,8.2,39,0.82]

         prefnum([514,7.6,37,0.9],'R10')    Renard, ten steps per decade.
           ans = [500,8.0,40,1]

         prefnum([514,7.6,37,0.9],'R"5')    Renard, five steps per decade, twice rounded.
           ans = [600,6.0,40,1]

         prefnum([514,7.6,37,0.9],'125')    1-2-5, three steps per decade.
           ans = [500,10,50,1]

         prefnum([514,7.6,37,0.9],[25,75])  Custom vector, two steps per decade.
           ans = [750,7.5,25,0.75]

         prefnum([514,7.6,37,0.9],1)        Custom vector, nearest order of magnitude.
           ans = [100,10,10,1]
    """
    #oc.prefnum([514,7.6,37,0.9],'E6')
    out =  oc.prefnum(InA, PfT)[0]
    return out

