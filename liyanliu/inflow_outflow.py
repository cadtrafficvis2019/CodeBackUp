import numpy as np
import pandas as pd
import os
import time,datetime
import math
import h5py

currentpath = os.getcwd()
print("currentpath:",currentpath)
data = pd.read_csv("filesList.csv")
listName = data['filename']

num = 30
Day = listName[num-1][1:3]
print("listName[num]:", listName[num-1], "Day:", Day)

path = currentpath + '/'+ listName[num-1]+'/'
print("path:",path),print()

bottom=30.012
up=30.4439     
left=119.8691 
right=120.461
blockCount=100

wideRange=right-left
heightRange=up-bottom
wideDistance=wideRange/blockCount
heightDistance=heightRange/blockCount

def obtainFiles():
    files = []
    for i in range(24):
        if len(str(i))<2:
            i = '0' + str(i) + '.csv'
        else:
            i = str(i)+ '.csv'
        files.append(i)
    return files

def datetime_timestamp(day):
    datet0=datetime.datetime(2015,4,day,0,0,0)
    timestampt0=time.mktime(datet0.timetuple())
    
    datet1=datetime.datetime(2015,4,day,1,0,0)
    timestampt1=time.mktime(datet1.timetuple())
    
    return timestampt0,timestampt1

def timestamp_datetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt 

def splitDeviceId(files):
    for n in range(len(files)):
        big_dict = {}
        with open(path+files[n]) as f:
            print("files:", files[n])
            for line in f:
                feature_list = line.split(",")
                deviceId = feature_list[3]
                if deviceId not in big_dict:
                    big_dict[deviceId] = []
                big_dict[deviceId].append(line)
        del big_dict['DeviceID']

        save_father_path = path + '/DeviceID' + files[n][:2] +"/"
        save_end_info = ".csv"
        if os.path.isdir(save_father_path):
            print("当前文件夹存在。")
        else:
            os.mkdir(save_father_path )
            print("文件夹创建成功")
        for item in big_dict.items():
            #print(type(item[0]),item[0],item[0][:-2])
            deviceId_path = save_father_path + item[0][:-2] + save_end_info
            with open(deviceId_path, "w", encoding = 'utf-8') as device_file:
                device_file.write('Longitude'+','+'Latitude'+','+'Speed'+','+'DeviceID'+','+'TimeStamp'+','+'Status'+','+'Heading'+'\n')
                for line in item[1] :
                    device_file.write(line)
                #print("以保存分类到文件%s."%(deviceId_path))
                
def F():
    files = []
    for i in range(24):
        if i <10:
            files.append('DeviceID'+'0'+str(i))
        else:
            files.append('DeviceID'+str(i))
    return files

def obtainInflowOutflow(t0,files):
    inOutTk = np.zeros((144, 2, 100,100))
    a = t0
    b = t0+600
    for n in range(len(files)):
            deviceId_path = path+str(files[n])+'/' # 获得路径
            print(deviceId_path)
            print("input path:", deviceId_path)
            filenameList = []
            for filename in os.listdir(deviceId_path):
                filenameList.append(filename )
            print("input deviceIdList.shape:", len(filenameList))

            for ti in range(6):
                print(timestamp_datetime(a), timestamp_datetime(b))
                inRegions = np.zeros((100,100)) # 存储在某个区域的 inflow
                outRegions = np.zeros((100,100)) # 存储在某个区域的 outflow
                
                for fileN in range(len(filenameList)):
                    data = pd.read_csv(deviceId_path+filenameList[fileN])
                   # print("data.shape:",data.shape, "  fileN:", fileN, "  path:", deviceId_path+filenameList[fileN])
                    df = pd.DataFrame(data = data)
                    dfnew = data[(data.TimeStamp>=a)&(data.TimeStamp<b)]
                    #print(fileN, df.shape, dfnew.shape, timestamp_datetime(a), timestamp_datetime(b))
                    rowList = [min(math.floor(row),99) for row in (dfnew.Latitude-bottom)/heightDistance]
                    colList = [min(math.floor(col),99) for col in (dfnew.Longitude-left)/wideDistance]
                    for gi in range(len(rowList)-1):
                        if ((rowList[gi] != rowList[gi+1]) | (colList[gi] != colList[gi+1])):
                            outRegions[rowList[gi]][colList[gi]] += 1
                            inRegions[rowList[gi+1]][colList[gi+1]] += 1
                print(sum(sum(outRegions)),sum(sum(inRegions)))
                a += 600
                b += 600
                inOut= np.array([inRegions, outRegions])
                index = n*6+ti
                print("index:", index)
                inOutTk[index] = inOut
                inOutTk = np.array(inOutTk)
                print()
    return inOutTk
    
print("开始运行......")
now = time.clock()

files = obtainFiles()
print("files:", files),print()

Devicefiles = F()
print("Devicefiles:", Devicefiles),print()

day = int(Day)
t0, t1= datetime_timestamp(day)
print("start time:",t0, "  end time:", t1, "  当前日期", timestamp_datetime(t0))

# splitDeviceId(files)
# print("数据按设备ID分裂完成。")

inOutTk = obtainInflowOutflow(t0,Devicefiles)
print("数据按没10分钟计算流进流出值完成。")

f = h5py.File(currentpath+"/InOut_100X100/"+ 'HZ14_'+ Day+ '_M100x100_InOut.hdf5', "w")
print(currentpath+"/InOut_100X100/"+ 'HZ14_'+ Day+ '_M100x100_InOut.hdf5')
f['data'] = inOutTk
print("数据写入完成。")

print("运行完毕！耗时%f分钟。"%((time.clock()-now)/60))   