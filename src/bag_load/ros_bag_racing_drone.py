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
    bagfileName = "0912_no_gate.bag"
    bagfileDir = os.path.dirname(os.path.abspath(sys.argv[0])) + "/../../" + "data/racing_drone/"
    processed_bag = ul.ReadBag(bagfileName=bagfileName, bagfileDir=bagfileDir)

    # now set the topic you wish to covert to .csv files
    topicList = ['/orin16/vicon/adr_drone_2/adr_drone_2',
                 '/orin16/bf/rpm',
                 '/orin16/bf/imu']
    ul.SaveProcessedBagToCSV(processed_bag=processed_bag, topicList=topicList)
