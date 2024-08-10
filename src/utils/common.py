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

def QuaT2RotationMatrix(imuLogging):
    

# used for testing r.as_matrix
def QuaT2RotationMatrix(w, x, y, z):
""""
    L = [-q1 q0 q3 -q2;
         -q2 -q3 q0 q1;
         -q3 q2 -q1 q0]
    R = [-q1 q0 -q3 q2;
         -q2 q3 q0 -q1;
         -q3 -q2 q1 q0]
    R_IB = RL^T

    pose[1].L(0,0) = - pose[1].q1;
    pose[1].L(1,0) = - pose[1].q2;
    pose[1].L(2,0) = - pose[1].q3;

    pose[1].L(0,1) = pose[1].q0;
    pose[1].L(1,2) = pose[1].q0;
    pose[1].L(2,3) = pose[1].q0;

    pose[1].L(0,2) = pose[1].q3;
    pose[1].L(0,3) = - pose[1].q2;
    pose[1].L(1,1) = - pose[1].q3;
    pose[1].L(1,3) = pose[1].q1;
    pose[1].L(2,1) = pose[1].q2;
    pose[1].L(2,2) = - pose[1].q1;

    pose[1].R(0,0) = - pose[1].q1;
    pose[1].R(1,0) = - pose[1].q2;
    pose[1].R(2,0) = - pose[1].q3;

    pose[1].R(0,1) = pose[1].q0;
    pose[1].R(1,2) = pose[1].q0;
    pose[1].R(2,3) = pose[1].q0;

    pose[1].R(0,2) = -pose[1].q3;
    pose[1].R(0,3) =  pose[1].q2;
    pose[1].R(1,1) =  pose[1].q3;
    pose[1].R(1,3) = -pose[1].q1;
    pose[1].R(2,1) = -pose[1].q2;
    pose[1].R(2,2) =  pose[1].q1; 

    pose[1].R_IB = pose[1].R * pose[1].L.transpose();
    pose[1].R_BI = pose[1].R_IB.transpose();
    // position is straight forward
    pose[1].Position(0) =  OptiTrackdata.pose.position.x;
    pose[1].Position(1) =  OptiTrackdata.pose.position.y;
    pose[1].Position(2) =  OptiTrackdata.pose.position.z;

"""
    L = np.zeros((3, 4))
    R = np.zeros((3, 4))
    
    pass


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