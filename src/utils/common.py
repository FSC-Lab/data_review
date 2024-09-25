'''
MIT License

Copyright (c) 2024 FSC Lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''
import numpy as np
from scipy.spatial.transform import Rotation

def QuaT2EulerAngles(imuLogging):
    n = len(imuLogging["orientation.x"])
    
    roll = np.zeros((n,))
    pitch = np.zeros((n,))
    yaw = np.zeros((n,))

    for i in range(n):
        r = Rotation.from_quat([imuLogging["orientation.x"][i],
                                imuLogging["orientation.y"][i],
                                imuLogging["orientation.z"][i],
                                imuLogging["orientation.w"][i]])
        euler = r.as_euler('xyz', degrees=True)
        roll[i] = euler[0]
        pitch[i] = euler[1]
        yaw[i] = euler[2]
    return roll, pitch, yaw


# quad 2 rotation matrix R_IB
def QuaT2RotationMatrix(w, x, y, z):
    '''
        L = [-q1 q0 q3 -q2;
            -q2 -q3 q0 q1;
            -q3 q2 -q1 q0]
    '''
    L = np.array([[-x, w, z, -y],
                  [-y, -z, w, x],
                  [-z, y -x, w]])
    '''
    R = [-q1 q0 -q3 q2;
         -q2 q3 q0 -q1;
         -q3 -q2 q1 q0]
    '''
    R = np.array([[-x, w, -z, y],
                  [-y, z, w, -x],
                  [-z, -y, x, w]])
    # R_IB = RL^T
    return R @ L.transpose()

# linear interpolation
# determine whether there are entries lie in the given interval
def FindElementFromInterval(data, start, end):
    startIdx = -1
    numOfPoints = 0
    
    return startIdx, numOfPoints


def MovingWindowAverage(data, windowLen=5):
    res = np.zeros_like(data)
    for i, x in enumerate(data):
        total = 0
        numOfpoints = 0
        for j in range(windowLen):
            currIdx = i - j
            if currIdx >= 0:
                total = total + data[currIdx]
                numOfpoints = numOfpoints + 1
        
        if numOfpoints > 0:
            res[i] = total / numOfpoints
    return res