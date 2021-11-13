"""
One quadrilateral ABCD has an incircle I, IA = 5, IB = 6, IC = 7, IB = 8
M is midpoint of AC, N is midpoint of BD, find MI : NI
"""
from mathSymbols import * 
from mathEquationSolver import *
'''
4^2 + 7^2 - 2*4*7cosQ = 28 ^2 t ^ 2
5^2 + 6^2 + 2*5*6cosQ = 30 ^2 t ^ 2
'''
t2 = (6 * 5 * (16 + 28) + 7 * 4 * (25 + 36)) / (6 * 5 * 28 * 28 + 7 * 4 * 30 * 30)
'''
4^2 + 5^2 - 2*4*5cosQ = 20 ^2 t ^ 2
7^2 + 6^2 + 2*7*6cosQ = 42 ^2 t ^ 2
'''
q2 = (6 * 7 * (25 + 16) + 5 * 4 * (36 + 49)) / (6 * 7 * 20 * 20 + 5 * 4 * 42 * 42)
t, q = t2 ** 0.5, q2 ** 0.5
getCosVal = lambda a, b, c:(a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
getCosAngle = lambda a, b, c:acos(getCosVal(a, b, c))

ver_to_in = {"IA" : 4, "IB" : 5, "IC" : 6, "ID" : 7}
side = {"AB" : (a := 20 * q),"BC" : (b := 30 * t),"CD" : (c := 42 * q),"DA" : (d :=28 * t)}
angles = {
	"A" : (A := getCosAngle(side["AB"], ver_to_in["IA"], ver_to_in["IB"]) + getCosAngle(side["DA"], ver_to_in["IA"], ver_to_in["ID"])), 
	"B" : (B := getCosAngle(side["AB"], ver_to_in["IB"], ver_to_in["IA"]) + getCosAngle(side["BC"], ver_to_in["IB"], ver_to_in["IC"])), 
	"C" : (C := getCosAngle(side["BC"], ver_to_in["IC"], ver_to_in["IB"]) + getCosAngle(side["CD"], ver_to_in["IC"], ver_to_in["ID"])), 
	"D" : (D := getCosAngle(side["CD"], ver_to_in["ID"], ver_to_in["IC"]) + getCosAngle(side["DA"], ver_to_in["ID"], ver_to_in["IA"])), 
}
semiperimeter = s = (a + b + c + d) / 2
area = ((s - a) * (s - b) * (s - c) * (s - d) - a * b * c * d * cos((A + C) / 2) ** 2) ** 0.5
incircleRadius = r = area / s
coordI = ((36 - r ** 2) ** 0.5, r)
coordC = (0, 0)
coordD = (c, 0)
coordB = (b * cos(C), b * sin(C))
coordA = (c - d * cos(D), d * sin(D))
coordM = ((coordA[0] + coordC[0]) / 2, (coordA[1] + coordC[1]) / 2)
coordN = ((coordB[0] + coordD[0]) / 2, (coordB[1] + coordD[1]) / 2)
Ix, Iy = coordI
Mx, My = coordM
Nx, Ny = coordN
dIM = ((Ix - Mx) ** 2 + (Iy - My) ** 2) ** 0.5 
dIN = ((Ix - Nx) ** 2 + (Iy - Ny) ** 2) ** 0.5
ratio = (dIM / dIN)
ratio_std = 35 / 48
print(abs(ratio_std - ratio) / ratio_std)