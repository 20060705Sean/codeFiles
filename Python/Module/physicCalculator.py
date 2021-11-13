'''
1. An Newton Object
@can output or receive these datas:

-> F
--> external force(receive only)
--> summary force(output only)

-> mass

-> momentum

-> x
--> position
--> delta position in time

-> v
--> average velocity
--> instantaneous velocity
--> delta velocity in time

-> a
--> acceleration
--> delta acceleration in time


@can do these jobs:
-> calculate status after n sec
-> two objects can collide

2. Feild Object
@can output or receive these datas:
-> Feild velocity
-> coefficent of friciton
-> Feild force

'''
import matplotlib.pyplot as plt
from math import atan, pi
const = {
	"G" : 6.67408 * (10 ** (-11)), 
	"density" : 5510
}

class Vector(object):
	def __init__(self, *values):
		self.values = values[0] if isinstance(values[0], tuple) else values
	def __abs__(self):
		return sum([v ** 2 for v in self.values]) ** 0.5
	def __add__(self, other):
		return Vector(tuple([v1 + v2 for v1, v2 in zip(self.values, other.values)]))
	def __iadd__(self, other):
		return self + other
	def __sub__(self, other):
		return self + (-1) * other
	def __mul__(self, other):
		return Vector(tuple([v * other for v in self.values]))
	def __rmul__(self, other):
		return self * other
	def __truediv__(self, other):
		return self * (1 / other)
	def __str__(self):
		return str(self.values)
	def __round__(self, k):
		return Vector(tuple([round(v, k) for v in self.values]))
class SpaceContainer(object):
	def __init__(self, delta_time, *objects):
		super(SpaceContainer, self).__init__()
		self.delta_time = delta_time
		self.objects = objects
		self.dimention = 3
	def start_simulation(self, end):
		t = 0
		logs = {}
		logs[0] = ["initial"]
		while t < end:
			t += self.delta_time
			logs[t] = []
			for planet in self.objects:
				sigma_force = Vector(0, 0, 0) if self.dimention == 3 else Vector(0, 0)
				for other_planet in self.objects:
					if other_planet == planet:
						continue
					distance = abs(other_planet.position - planet.position)
					if planet.radius + other_planet.radius >= distance:
						planet.velocity, other_planet.velocity = - other_planet.velocity * other_planet.mass / planet.mass, - planet.velocity  * planet.mass / other_planet.mass
					unit_vector = (other_planet.position - planet.position) / distance
					G = const["G"]
					sigma_force += G * planet.mass * other_planet.mass / distance ** 2 * unit_vector
				acceleration = sigma_force / planet.mass
				planet.velocity += acceleration * self.delta_time
				planet.position += planet.velocity * self.delta_time
				pos = planet.position.values
				plt.scatter(pos[0], pos[1])
				logs[t].append((planet.velocity.values, planet.position.values))
				pos = planet.position.values
		return logs
class NewtonObject(object):
	def __init__(self, mass, position, initial_velocity):
		super(NewtonObject, self).__init__()
		self.mass = mass
		self.radius = mass
		self.position = position
		self.velocity = initial_velocity

class PlanetLikeObject(NewtonObject):
	def __new__(cls, mass, position, initial_velocity):
		return super(PlanetLikeObject, cls).__new__(cls)
	def __init__(self, mass, position, initial_velocity):
		super().__init__(mass, position, initial_velocity)
		self.radius = (self.radius * 3 / 4 / pi / const["density"]) ** (1 / 3)

Earth = PlanetLikeObject(5.97237 * 10 ** 24, Vector(0, 0), Vector(0, 0))
Moon = PlanetLikeObject(7.3477 * 10 ** 22, Vector(384401000, 0), Vector(0, 1023.1))
Sun = PlanetLikeObject(1.98892 * 10 ** 30, Vector(149597871000, 0), Vector(0, 0))
space1 = SpaceContainer(8640, Earth, Moon, Sun)
space1.start_simulation(2592000)
plt.show()