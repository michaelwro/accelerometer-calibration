"""

PLOT UNCALIBRTED AND CALIBRATED ACCELEROMETER MEASUREMENTS

Read data file with raw measurements and compare calibrated vs. uncalibrated
measurements.

Code By: Michael Wrona

The calibration equation is:
    h_calib = A * (h_meas - b)

h_calib: Calibrated measurements (3x1)
A: Scale factor and misalignment correction matrix (3x3, symmetric)
h_meas: Raw measurements (3x1)
b: Biases correction vector (3x1)

Calibration parametrers were determined by the Magneto calibration software (see Resources).

Resources
---------
Magneto calibration software developed by Sailboat Instruments blog
    https://sites.google.com/site/sailboatinstruments1/home

"""


import numpy as np
import matplotlib.pyplot as plt


# Define calibration parameters
A = np.array(   [[1.004332, 0.000046, 0.004896],
                [0.000046, 0.969793, 0.009452],
                [0.004896, 0.009452, 1.022384]])
b = np.array([0.027031, -0.040204, 0.046558])

# Read raw data and apply calibration
rawData = np.genfromtxt('acceldata.txt', delimiter='\t')  # Read raw measurements

N = len(rawData)
calibData = np.zeros((N, 3), dtype='float')
for i in range(N):
    currMeas = np.array([rawData[i, 0], rawData[i, 1], rawData[i, 2]])
    calibData[i, :] = A @ (currMeas - b)

# calibData *= 9.80665
# rawData *= 9.80665

# Plot XY data
plt.figure()
plt.plot(rawData[:, 0], rawData[:, 1], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 0], calibData[:, 1], 'r*', label='Calibrated Meas.')
plt.title('XY Accelerometer Data')
plt.xlabel('X [G\'s]')
plt.ylabel('Y [G\'s]')
plt.legend()
plt.grid()
plt.axis('equal')

# Plot YZ data
plt.figure()
plt.plot(rawData[:, 1], rawData[:, 2], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 1], calibData[:, 2], 'r*', label='Calibrated Meas.')
plt.title('YZ Accelerometer Data')
plt.xlabel('Y [G\'s]')
plt.ylabel('Z [G\'s]')
plt.legend()
plt.grid()
plt.axis('equal')

# Plot XZ data
plt.figure()
plt.plot(rawData[:, 0], rawData[:, 2], 'b*', label='Raw Meas.')
plt.plot(calibData[:, 0], calibData[:, 2], 'r*', label='Calibrated Meas.')
plt.title('XZ Accelerometer Data')
plt.xlabel('X [G\'s]')
plt.ylabel('Z [G\'s]')
plt.legend()
plt.grid()
plt.axis('equal')


# Plot 3D scatter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(N):
    xraw = rawData[i, 0]
    yraw = rawData[i, 1]
    zraw = rawData[i, 2]

    xcalib = calibData[i, 0]
    ycalib = calibData[i, 1]
    zcalib = calibData[i, 2]
    ax.scatter(xraw, yraw, zraw, color='r', label='Raw')
    ax.scatter(xcalib, ycalib, zcalib, color='b', label='Calibrated')

ax.set_title('3D Scatter Plot of Accelerometer Data')
ax.set_xlabel('X [G\'s]')
ax.set_ylabel('Y [G\'s]')
ax.set_zlabel('Z [G\'s]')
ax.legend(['Raw', 'Calibrated'])


plt.show()
