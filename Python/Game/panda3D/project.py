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
	def RotationMatrix(Hpr):
		
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
class DistrictMap(object):
	def __init__(self, mapFileName, render, districtCode, districtName):
		self.mapDate = {"name":districtCode, "code":districtCode}
		self.mapMesh
		self.mapModel = loader.loadModel(mapFileName)
		self.mapModel.reparentTo(render)
class myProjectile(object):
	def __init__(self, b_render, cs_FileName:str):
		super(myProjectile)
		self.cs_FileName = cs_FileName
		self.m_projectile = loader.loadModel(cs_FileName)
		self.m_projectile.reparentTo(b_render)
		self.m_projectile.hide()
	def f_projection(self, p3_position:Point3, v3_velocity:Vec3, i_endZ:int, ci_gravity:int = 9.81):
		self.m_projectile.show()
		self.m_projectile.setPos(p3_position)
		ci_gravity = Vec3(0, 0, -ci_gravity)
		while self.m_projectile.getPos()[2] >= i_endZ:
			p3_position += v3_velocity * 0.1
			v3_velocity += ci_gravity * 0.1
			self.m_projectile.setPos(p3_position)
			sleep(0.01)
		self.m_projectile.hide()
		del self
class Character(object):
	def __init__(self, b_render, cs_FileName:str, v3_position:Point3 = Point3(0, 0, 0)):
		super(Character)
		self.cs_FileName = cs_FileName
		self.m_character = Actor(cs_FileName)
		self.m_character.reparentTo(b_render)
		self.m_character.setPos(v3_position)
		self.ci_movingSpeed = 0.2
		self.o_movingThread = {i:None for i in("forward", "backward", "right", "left")}
	def move(self, mode):
		t = threading.currentThread()
		while getattr(t, "loop_alive", True):
			sleep(0.01)
			nowPos = self.m_character.getPos()
			nowAng = self.m_character.getHpr()
			added = Vec3(
				sin(nowAng[2] + mode) * self.ci_movingSpeed, 
				cos(nowAng[2] + mode) * self.ci_movingSpeed, 0)
			self.m_character.setPos(nowPos + added)
	def moving_character(self, mode:str, stop):
		if not stop:
			m = str(mode)
			if mode == "forward":mode = 0
			elif mode == "backward":mode = pi
			elif mode == "right":mode = pi/2
			elif mode == "left":mode = -pi/2
			self.o_movingThread[m] = threading.Thread(target = self.move, args = (mode, ))
			self.o_movingThread[m].start()
		else:
			self.o_movingThread[mode].loop_alive = False
class Main(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.map = loader.loadModel("floor/floor.egg")
		self.map.reparentTo(self.render)
		self.character = Character(self.render, "man/man.egg")
		self.myHeadNodePath = self.character.m_character.controlJoint(None,"modelRoot","Bone.017")
		self.taskMgr.add(self.camera_positioning_task, "SpinCameraTask")
		self.accept("q", self.shoot_bullet_action)
		for i, j in [('w', 'forward'), ('s', 'backward'), ('a', 'left'), ('d', 'right')]:
			self.accept(i, self.character.moving_character, [j, False])
			self.accept(i+"-up", self.character.moving_character, [j, True])
	def camera_positioning_task(self, task):
		#self.camera.setPos(self.character.m_character.getPos())
		#self.camera.setHpr(self.character.m_character.getHpr())
		return Task.cont
	def shoot_bullet_action(self):
		arg = (self.character.m_character.getPos(), Vec3(0, 10, 10), 0)
		trident = myProjectile(self.render, "man/block.egg")
		thread = threading.Thread(target = trident.f_projection, args = (arg[0], arg[1], arg[2]))
		thread.start()
main = Main()
myvr = P3DOpenVR()
#myvr.init()
main.run()
