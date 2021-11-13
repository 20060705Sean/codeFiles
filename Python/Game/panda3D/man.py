from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.ProjectileInterval import ProjectileInterval
from panda3d.core import load_prc_file
from panda3d.core import Point3, Vec3
import threading
from time import sleep
from math import sin, cos, tan, asin, acos, atan2, pi, sqrt
from p3dopenvr.p3dopenvr import *
from direct.gui.OnscreenText import OnscreenText
from numpy import array, dot
textObject = OnscreenText(text='my text string', pos=(-1.2, 0.8), scale=0.07)
load_prc_file('myConfig.prc')


class AngleTransfer():
	@staticmethod
	def RotationMatrix(Hpr):
		Y, P, R = Hpr
		return [[
			cos(P)*cos(Y), 
			sin(R)*sin(P)*cos(Y) - sin(Y)*cos(R), 
			cos(R)*sin(P)*cos(Y) + sin(Y)*sin(R)
			], [
			sin(Y)*cos(P), 
			sin(P)*sin(R)*sin(Y) + cos(R)*cos(Y), 
			cos(R)*sin(P)*sin(Y) - sin(R)*cos(Y)
			], [
			-sin(P), sin(R)*cos(P), cos(R)*cos(P)
			]
		]
	@staticmethod
	def eulerToRot(Hpr):
		RotM = AngleTransfer.RotationMatrix(Hpr)
		theta = acos(((RotM[0][0] + RotM[1][1] + RotM[2][2]) - 1) / 2)
		sin_theta = sin(theta)
		if sin_theta == 0:
			rx, ry, rz = 0, 0, 0
		else:
			multipler = 1 / (2 * sin_theta)
			rx = multipler * (RotM[2][1] - RotM[1][2]) * theta
			ry = multipler * (RotM[0][2] - RotM[2][0]) * theta
			rz = multipler * (RotM[1][0] - RotM[0][1]) * theta
		return Vec3(rx, ry, rz)
	@staticmethod
	def rotToEuler(Hpr):
		R = Hpr
		sy = sqrt(R[0][0] * R[0][0] +  R[1][0] * R[1][0])
		singular = sy < 1e-6
		if  not singular :
			x = atan2(R[2][1] , R[2][2])
			y = atan2(-R[2][0], sy)
			z = atan2(R[1][0], R[0][0])
		else :
			x = atan2(-R[1][2], R[1][1])
			y = atan2(-R[2][0], sy)
			z = 0
		return Vec3(x, y, z)
roll = pi / 3 
pitch = pi/2
yaw = 0

spinx = 0.815484
spiny = 1.41246
spinz = -0.815484
print(AngleTransfer.eulerToRot((yaw, pitch, roll)))
spin = dot(array([[spiny, 0, spiny], [0, 1, 0], [-spiny, 0, spiny]]), array([[1, 0, 0], [0, spinx, -spinx], [0, spinx, spinx]]))
spin = dot(array([[spinz, -spinz, 0], [spinz, spinz, 0], [0, 0, 1]]), spin)
print(spin)
print(AngleTransfer.rotToEuler(spin))
	
class Main(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.BonesGroup = {
			"ulna" : loader.loadModel("hand/hand.egg"), 
			"carpals" : [loader.loadModel("hand/hand.egg") for i in range(5)], 
			"metacarpals" : [loader.loadModel("hand/hand.egg") for i in range(5)], 
			"proximal phalanges" : [loader.loadModel("hand/hand.egg") for i in range(5)], 
			"intermidiate phalanges" : [loader.loadModel("hand/hand.egg") for i in range(5)], 
			"distal phalanges" : [loader.loadModel("hand/hand.egg") for i in range(5)]
		}
		bones = list(self.BonesGroup.values())
		bones[0].reparentTo(self.render)
		for i in bones[1]:
			i.reparentTo(bones[0])
		for i, b in enumerate(bones[2:]):
			for j, obj in enumerate(b):
				obj.reparentTo(bones[i + 1][j])
main = Main()
main.run()