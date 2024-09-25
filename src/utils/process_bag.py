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
import pandas as pd
from bagpy import bagreader

def ReadBag(bagfileName, bagfileDir):
    # this will display all the topics and data types
    with rosbag.Bag(bagfileDir + bagfileName, 'r') as bag_raw:
        info = bag_raw.get_type_and_topic_info()
        # topic in info 0
        topic0 = list(info[0].keys())
        topic1 = list(info[1].keys())
        print("------message types:-------")
        for x in topic0:
            print(x)
        print("------topics:-------")
        for x in topic1:
            print(x)
        rocessed_bag = bagreader(bagfileDir + bagfileName)
    return rocessed_bag

# save processed bag file from the ReadBag function to .csv files
def SaveProcessedBagToCSV(processed_bag, topicList):
    for topic in topicList:
        processed_bag.message_by_topic(topic)

def GetStartTime(bagfileName):
    with open(bagfileName, newline='') as csvfile:
        states = pd.read_csv(csvfile)

    TbaseSec = states['header.stamp.secs'][0]
    TbaseNsec = states['header.stamp.nsecs'][0]
    return TbaseSec + TbaseNsec * 10**-9

# determine the start and end index from the start and end time
def GetStartEndIdex(input, startT, endT):
    if (startT > endT):
        raise Exception("startT must be lower or equal to the endT! startT: "
                        + str(startT)
                        + "endT: "
                        + str(endT))
    startIdx = -1
    endIdx = -1
    
    if (input[-1] < startT) or (input[0] > endT):
        return startIdx, endIdx

    startIdxFound = False
    endIdxFound = False
    for i, x in enumerate(input):
        if startIdxFound and endIdxFound:
            break

        if (not startIdxFound) and (x >= startT):
            startIdx = i
            startIdxFound = True

        if (not endIdxFound) and (x > endT):
            endIdx = i - 1
            endIdxFound = True
        else:
            endIdx = i

    return startIdx, endIdx


# get data from the csv file
def ProcessRosbagDataFromCSV(bagfileName, calcTime=False):
    with open(bagfileName, newline='') as csvfile:
        states = pd.read_csv(csvfile)

    if not calcTime:
        return states

    TbaseSec = states['header.stamp.secs']
    TbaseNsec = states['header.stamp.nsecs']

    # calcualte tbase
    Tbase = list()
    Tlen = len(TbaseSec)
    for i in range(Tlen):
        Tbase.append(TbaseSec[i] + TbaseNsec[i] * 10**-9)

    # reset start time
    startT = Tbase[0]
    for i in range(Tlen):
        Tbase[i] = Tbase[i] - startT

    # append time
    states["processed_time"] = Tbase
    return states


# get data from the csv file
def ProcessRosbagDataFromCSVWithBaseTime(bagfileName,
                                         startT,
                                         endT,
                                         headerTimeStamp=False,
                                         baseTime=None):
    with open(bagfileName, newline='') as csvfile:
        states = pd.read_csv(csvfile)

    # if headerTimeStamp is True, use 'header.stamp.secs' and 'header.stamp.nsecs',
    # otherwise use 'Time'.
    # note that 'Time' is not accurate
    Tbase = list()
    if headerTimeStamp:
        TbaseSec = states['header.stamp.secs']
        TbaseNsec = states['header.stamp.nsecs']
        # calcualte tbase
        Tlen = len(TbaseSec)
        for i in range(Tlen):
            Tbase.append(TbaseSec[i] + TbaseNsec[i] * 10**-9)
    else: 
        Tlen = len(states['Time'])
        for i in range(Tlen):
            Tbase.append(states['Time'][i])

    if baseTime is None:
        # reset start time
        beginT0 = Tbase[0]
    else:
        beginT0 = baseTime

    for i in range(Tlen):
        Tbase[i] = Tbase[i] - beginT0

    startIdx, endIdx = GetStartEndIdex(Tbase, startT, endT)

    res = dict()
    for idx, (key, value) in enumerate(states.items()):
        res[key] = value.to_list()[startIdx: endIdx + 1]

    # append time
    res["processed_time"] = Tbase[startIdx:endIdx + 1]
    
    return res
