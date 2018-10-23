from drone_simulator import DroneSimulator
import sys

WIDTH = 20
HEIGHT = 20

for arg in sys.argv:
    if arg == 'drone':
        drone_simulator = DroneSimulator()
        drone_simulator.run()




