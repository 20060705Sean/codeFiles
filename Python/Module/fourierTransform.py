from math import sin, cos, pi
from random import randint
import matplotlib.pyplot as plt

from pydub import AudioSegment
import keras
import keras.models
import numpy as np
import sys
import matplotlib.pyplot as plt
import numpy as np
'''import numpy, scipy, pylab, wave, scipy.fftpack, scipy.io.wavfile as wav
xs = numpy.arange(1, 100, .01)
rate, sample = wav.read("test.mp3")
fft2 = scipy.fftpack.fft2(sample) # algo applied
bp = fft2[: ]
for i in range(len(bp)):
   if i >= 10: bp[i] = 0
ibp = scipy.fftpack.ifft2(bp) # inverse algo
print ("to check dimension")
print("sampling rate = {} Hz, length = {} samples, channels = {}".format(rate, * sample.shape))
print(sample)
'''
'''
seg = AudioSegment.from_file("test.mp3")
# Just take the first 3 seconds
hist_bins, hist_vals = seg[1:3000].fft()
hist_vals_real_normed = np.abs(hist_vals) / len(hist_vals)
plt.plot(hist_bins / 1000, hist_vals_real_normed)
plt.xlabel("kHz")
plt.ylabel("dB")
plt.show()
'''
'''
def fourierTransform(function_dots, time, frequency):
	result = complex()
	for t, d in enumerate(function_dots):
		result += d * (cos(- 2*pi*frequency*time[t]) + 1j*sin(- 2*pi*frequency*time[t]))
	return result
dots = [sin(2 * pi / 60 * i) for i in range(60)]
time = list(map(lambda x:x/10, range(0, len(dots))))
P = time[-1] - time[0]
rst = []
for i in range(1, 200):
	rst.append((i, fourierTransform(dots, time, 2 * pi / i)))
#print(list(sorted(rst, key = lambda x:abs(x[1]))))
freq, intensity = zip(*rst)
plt.plot(time, dots, color = 'red')
plt.plot(freq, intensity)
plt.show()
'''
class fourier_series(object):
	def __init__(self, x, y):
		self.x = x
		self.P = (x[0] - x[-1]) 
		self.y = y
		super(fourier_series)
	def calculate(self, sophistication = 100):
		result = []
		for i in self.x:
			result.append(self.calculateAtX(i, sophistication))
		return result
	def calculateAtX(self, x, s):
		const = self.anIntergral(0) / 2
		result = 0
		result += const
		for n in range(1, s + 1):
			result += self.anIntergral(n) * cos(2 * pi * n * x / self.P) + self.bnIntergral(n) * sin(2 * pi * n * x / self.P)
		return result
	def anIntergral(self, n):
		result = 0
		dx = self.P / len(self.x)
		q = self.x[0]
		for fx in self.y:
			result += fx * dx * cos(2 * pi * q * n / self.P)
			q += dx
		result *= 2 / self.P
		return result
	def bnIntergral(self, n):
		result = 0
		dx = self.P / len(self.x)
		q = self.x[0]
		for fx in self.y:
			result += fx * dx * sin(2 * pi * q * n / self.P)
			q += dx
		result *= 2 / self.P
		return result
resolution = 360
dr = 2 * pi / resolution
x = [dr * i for i in range(resolution + 1)]
y = list(map(lambda u:(360 * u / (2* pi)) % 180 - 90, x))
ana = fourier_series(x, y)
plt.plot(x, list(reversed(ana.calculate(1000))), color = 'blue')
plt.plot(x, y, color = 'red')
plt.show()