



Starndard_Blood_Pressure_High = 120
Starndard_Blood_Pressure_Low = 80
Starndard_Heart_Rate = 72




from os import system
system("pip install matplotlib")
import matplotlib.pyplot as plt
pressure_high = []
pressure_low = []
heart_rate = []
days = []
with open("assets/bld.csv") as file:
	k = 0
	for i in file.readlines():
		days.append(k)
		k += 1
		if i.count(",") > 0:
			i = i[:-1].split(",")
		if i.count("/") > 0:
			i = i[:-1].split("/")
		if i.count("\\") > 0:
			i = i[:-1].split("\\")
		pressure_high.append(int(i[0]))
		pressure_low.append(int(i[1]))
		heart_rate.append(int(i[2]))

plt.plot([0, days[-1]], [Starndard_Blood_Pressure_High, Starndard_Blood_Pressure_High], color = '#5555AA')
plt.plot([0, days[-1]], [Starndard_Blood_Pressure_Low, Starndard_Blood_Pressure_Low], color = '#55AA55')
plt.plot([0, days[-1]], [Starndard_Heart_Rate, Starndard_Heart_Rate], color = '#AA5555')
plt.scatter(days, pressure_high, color = 'b')
plt.scatter(days, pressure_low, color = 'g')
plt.scatter(days, heart_rate, color = 'r')
plt.plot(days, pressure_high, color = 'b')
plt.plot(days, pressure_low, color = 'g')
plt.plot(days, heart_rate, color = 'r')	
plt.show()