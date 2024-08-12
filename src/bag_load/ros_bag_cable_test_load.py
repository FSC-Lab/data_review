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
    bagfileName = "payload_retraction_0808_trial1.bag"
    bagfileDir = os.path.dirname(os.path.abspath(sys.argv[0])) + "/../../" + "data/cable_test/"
    processed_bag = ul.ReadBag(bagfileName=bagfileName, bagfileDir=bagfileDir)

    # now set the topic you wish to covert to .csv files
    topicList = ['/encoder/position_payload',
                 '/encoder/position_raw',
                 '/encoder/velocity_payload',
                 '/encoder/velocity_raw',
                 '/mocap/T15',
                 '/mocap/pld',
                 '/stepper/serial_command',
                 '/stepper/setpoint',
                 '/stepper/test']
    ul.SaveProcessedBagToCSV(processed_bag=processed_bag, topicList=topicList)
