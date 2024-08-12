import rosbag
from bagpy import bagreader
import csv
from nav_msgs.msg import Odometry
import pandas as pd
import os
import sys

# get current file dir
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
print(current_dir)
# append the utils direct (if you change the appended path, you must restart the kernel!)
sys.path.append(current_dir + "/..")
# import custom package (make sure the utils is added to the path)
import utils as ul

if __name__ == "__main__":
    # set the bag name here
    bagfileName = "test_ude_vi_with_ac_0726.bag"
    bagfileDir = os.path.dirname(os.path.abspath(sys.argv[0])) + "/../../" + "data/flight_test/"
    processed_bag = ul.ReadBag(bagfileName=bagfileName, bagfileDir=bagfileDir)

    # now set the topic you wish to covert to .csv files
    topicList = ['/mavros/imu/data',
                 '/mavros/setpoint_raw/attitude',
                 '/mavros/vision_pose/pose',
                 '/mocap/UAV0',
                 '/position_controller/output_data',
                 '/position_controller/target',
                 '/state_estimator/local_position/odom/UAV0']
    ul.SaveProcessedBagToCSV(processed_bag=processed_bag, topicList=topicList)
