"""

PLOT UNCALIBRATED AND CALIBRATED ACCELEROMETER MEASUREMENTS

Read data file with raw measurements and compare calibrated vs. uncalibrated
measurements.

Code By: Michael Wrona

The calibration equation is:
    h_calib = A * (h_meas - b)

h_calib: Calibrated measurements (3x1)
A: Scale factor and misalignment correction matrix (3x3, symmetric)
h_meas: Raw measurements (3x1)
b: Biases correction vector (3x1)

Calibration parameters were determined by the Magneto calibration software (see Resources).

Resources
---------
Magneto calibration software developed by Sailboat Instruments blog
    https://sites.google.com/site/sailboatinstruments1/home

"""


import os
import sys
import numpy as np
import matplotlib.pyplot as plt


# Define calibration parameters
A = np.array([[1.004332, 0.000046, 0.004896],  # 'A^-1' matrix from Magneto
              [0.000046, 0.969793, 0.009452],
              [0.004896, 0.009452, 1.022384]])
# 'Combined bias (b)' vector from Magneto
b = np.array([0.027031, -0.040204, 0.046558])

# Resolve default data file path safely relative to this script
scriptDir = os.path.dirname(os.path.abspath(__file__))
defaultDataFile = os.path.join(scriptDir, 'examples', 'acceldata-example.txt')

# Read raw data and apply calibration
dataFile = sys.argv[1] if len(sys.argv) > 1 else defaultDataFile

rawData = np.genfromtxt(dataFile, delimiter='\t')  # raw measurement file
units = 'G\'s'  # units of accelerometer measurements (used for axis labels)

N = len(rawData)
# Vectorized calibration: h_calib = A * (h_meas - b)
calibData = (rawData[:, :3] - b) @ A.T

# Calculate and print metrics summary
rawNorms = np.linalg.norm(rawData[:, :3], axis=1)
calibNorms = np.linalg.norm(calibData, axis=1)

# Plot XY data
plt.figure()
plt.plot(rawData[:, 0], rawData[:, 1], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 0], calibData[:, 1], 'r*', label='Calibrated Meas.')
plt.title('XY Accelerometer Data')
plt.xlabel('X [{}]'.format(units))
plt.ylabel('Y [{}]'.format(units))
plt.legend()
plt.grid()
plt.axis('equal')

# Plot YZ data
plt.figure()
plt.plot(rawData[:, 1], rawData[:, 2], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 1], calibData[:, 2], 'r*', label='Calibrated Meas.')
plt.title('YZ Accelerometer Data')
plt.xlabel('Y [{}]'.format(units))
plt.ylabel('Z [{}]'.format(units))
plt.legend()
plt.grid()
plt.axis('equal')

# Plot XZ data
plt.figure()
plt.plot(rawData[:, 0], rawData[:, 2], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 0], calibData[:, 2], 'r*', label='Calibrated Meas.')
plt.title('XZ Accelerometer Data')
plt.xlabel('X [{}]'.format(units))
plt.ylabel('Z [{}]'.format(units))
plt.legend()
plt.grid()
plt.axis('equal')


# Plot 3D scatter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(rawData[:, 0], rawData[:, 1], rawData[:, 2], color='r', label='Raw')
ax.scatter(calibData[:, 0], calibData[:, 1], calibData[:, 2], color='b', label='Calibrated')

ax.set_title('3D Scatter Plot of Accelerometer Data')
ax.set_xlabel('X [{}]'.format(units))
ax.set_ylabel('Y [{}]'.format(units))
ax.set_zlabel('Z [{}]'.format(units))
ax.legend()
('Y [{}]'.format(units))
ax.set_zlabel('Z [{}]'.format(units))
ax.legend(['Raw', 'Calibrated'])
('Y [{}]'.format(units))
ax.set_zlabel('Z [{}]'.format(units))
ax.legend(['Raw', 'Calibrated'])

plt.show()
