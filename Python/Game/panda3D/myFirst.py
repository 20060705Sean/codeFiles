from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import WindowProperties
from panda3d.core import load_prc_file

import simplepbr

from math import pi, sin, cos

load_prc_file('myConfig.prc')

class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		#simplepbr.init()
		'''
		self.kirito = self.loader.loadModel("kirito/scene.gltf")
		self.kirito.reparentTo(self.render)
		self.kirito.setPos(0, 0, 0)
		self.kirito.setScale(1, 1, 1)
		self.kirito.setHpr(0, 0, 0)
		'''
		'''
		self.elucidator = self.loader.loadModel("elucidator/scene.gltf")
		self.elucidator.reparentTo(self.render)
		self.elucidator.setPos(0, 0, -1)
		self.elucidator.setScale(0.05, 0.05, 0.05)
		self.elucidator.setHpr(0, 60, 0)
		'''
		self.mySword = Actor("MySword/mysword.egg.pz", {
			"attack" : "MySword/mysword-attack.egg.pz", 
			"idle" : "MySword/mysword-idle.egg.pz", 
			"poke" : "MySword/mysword-poke.egg.pz"
			}
		)
		self.mySword.reparentTo(self.render)
		self.mySword.setPos(0, 0, 0)
		self.mySword.setScale(1, 1, 1)
		self.ataack = self.mySword.getAnimControl('attack')
		self.startAttack = lambda:"denied" if self.ataack.isPlaying() else self.ataack.play()
		self.accept('space', self.startAttack)
		self.poke = self.mySword.getAnimControl("poke")
		self.accept("p", lambda:"denied" if self.poke.isPlaying() else self.poke.play())
		'''
		# add the spinCameraTask to the task manager
		self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
		'''
		# load and transform the panda actor
		'''
		self.pandaActor = Actor("models/panda-model", 
			{"walk" : "models/panda-walk4"})
		self.pandaActor.setScale(0.005, 0.005, 0.005)
		self.pandaActor.reparentTo(self.render)
		self.pandaActor.loop("walk")

		posInterval1 = self.pandaActor.posInterval(13, 
			Point3(0, -10, 0), 
			startPos=Point3(0, 10, 0))
		posInterval2 = self.pandaActor.posInterval(13, 
			Point3(0, 10, 0), 
			startPos=Point3(0, -10, 0))
		hprInterval1 = self.pandaActor.hprInterval(3, 
			Point3(180, 0, 0), 
			startHpr=Point3(0, 0, 0))
		hprInterval2 = self.pandaActor.hprInterval(3, 
			Point3(0, 0, 0), 
			startHpr=Point3(180, 0, 0))
		
		self.pandaPace = Sequence(posInterval1, hprInterval1, 
			posInterval2, hprInterval2, 
			name = "pandaPace")
		self.pandaPace.loop()
	def spinCameraTask(self, task):
		angleDegrees = task.time * 6.0
		angleRadians = angleDegrees * (pi / 180.0)
		self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
		self.camera.setHpr(angleDegrees, 0, 0)
		return Task.cont
		'''
		
app = MyApp()
app.run()