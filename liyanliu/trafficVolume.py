import numpy as np
import pandas as pd
import os
import math
import time
import h5py

current_path = os.getcwd()
print("current_path:", current_path)

bottom=30.012
up=30.4439     
left=119.8691 
right=120.461
blockCount=50

wideRange=right-left
heightRange=up-bottom
wideDistance=wideRange/blockCount
heightDistance=heightRange/blockCount

data = pd.read_csv("filesList.csv")
listName = data['filename']
print("listName[0]:", listName[0]),print()

def deviceFile():
    fileList = []
    for i in range(24):
        if len(str(i))<2:
            fileList.append('DeviceID'+'0'+str(i))
        else:
            fileList.append('DeviceID'+str(i))
    return fileList

fileList = deviceFile()
print("fileList:", fileList),print()

# m表示表示选取的天数，m=0,表示选取d01_w4
# n表示选取第几个DeviceID, n=0,表示选取DeviceID00
# 获取不同day下的DeviceID文件的路径，以及路径下文件列表
def deviceId(m,n): 
    deviceList = []
    path = current_path + '/'+listName[m]+'/'+fileList[n]+'/'
    for file in os.listdir(path):
        deviceList.append(file)
    return deviceList,path

deviceList,path = deviceId(0,1) 
print("len(deviceList):", len(deviceList))
# print("path:", path)

print("runing......")
now = time.clock()

# 获取每个网格中出租车的数量
def trafficVolum(m):
    TV = np.zeros((24,100,100))
    for n in range(24):
#     for n in range(0,2):
        deviceList,path = deviceId(m,n) 
        print("len(deviceList):", len(deviceList))
        print('path:',path)
        trafficVolume = np.zeros((100,100))
        for i in range(len(deviceList)):
        # for i in range(0,3):
            data = pd.read_csv(path+deviceList[i])
    #         print("deviceList[i]:", deviceList[i])
            df = pd.DataFrame(data = data)
            rowList = [int(min(math.floor(row),99)) for row in (df.Latitude-bottom)/heightDistance]
            colList = [int(min(math.floor(col),99)) for col in (df.Longitude-left)/wideDistance]
            grid = list(set((str(rowList[i])+','+str(colList[i])) for i in range(len(rowList))))
    #         print(len(grid))
            for j in range(len(grid)):
                row = int(grid[j].split(',')[0])
                col = int(grid[j].split(',')[1])
                trafficVolume[row][col] +=1
    #     trafficVoume = np.array(trafficVolume)
        print(sum(sum(trafficVolume)))
        TV[n]=np.array(trafficVolume)

    f = h5py.File(current_path + '/trafficVolume_100X100/'+ listName[m]+'_M100x100_trafficVolume.hdf5', "w")
    print(current_path + '/trafficVolume_100X100/'+ listName[m]+'_M100x100_trafficVolume.hdf5')
    f['data'] = TV

day = 20
trafficVolum(day-1)    
    
print("运行完毕！耗时%f分钟。"%((time.clock()-now)/60))  