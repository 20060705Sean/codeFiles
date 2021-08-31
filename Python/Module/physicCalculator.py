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
class NewtonObject(object):
	def __init__(self):
		super(NewtonObject, self).__init__()
		VAT_V = lambda v0, a, t:v0 + a*t
		VAS_V = lambda v0, a, s:(v0**2 + 2*a*s)**0.5
		VAT_S = lambda v0, a, t:v0*t + 0.5*a*(t**2)
		