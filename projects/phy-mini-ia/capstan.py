import matplotlib.pyplot as plt
import matplotlib

# changing
tension_load = 0
tension_slottedMass = 0

time_x = []
tension_load_y = []
tension_slottedMass_y = []

# constants
weight = 8
release_time = 400

for ms in range(1000):
    if tension_slottedMass < weight:
        tension_slottedMass += weight / release_time
    tension_load = tension_slottedMass
    
    time_x.append(ms)
    tension_slottedMass_y.append(tension_slottedMass)

plt.plot(time_x, tension_slottedMass_y, marker='.')
plt.show()