import numpy as np
import pandas as pd
import os
import time, datetime
import math

currentpath = os.getcwd()

temp = 'd24_w6'
Day = int(temp[1:3])
path = currentpath + '/' + temp + '/'
print("当前路径：", path)

title = ["DataTime","UniqueID","DeviceType","Company","DeviceID","Flag","FilterFlag",
          "EvelationFlag","Satellite","Heading","Speed","EvalationUnit","Evalation",
          "Status","Event","Longitude","Latitude","BJ-Longitude","BJ-Latitude","TimeStamp"]

head = ['Longitude','Latitude','Speed','DeviceID','TimeStamp','Status','Heading']

bottom=30.012
up=30.4439     
left=119.8691 
right=120.461
    
def obtainFiles():
    files = []
    for i in range(24):
        if len(str(i))<2:
            i = '0' + str(i) + '.csv'
        else:
            i = str(i)+ '.csv'
        files.append(i)
    return files

# 为每个文件添加 title 行
def addTitle(files):
    for i in range(len(files)):
        data = pd.read_csv(path + files[i], header = None)
        insertRow = pd.DataFrame([title])
        data = insertRow.append(data, ignore_index = True)
        data.to_csv(path+files[i],header = None, index = None)
        print(path+files[i])

#删除 long 和 lat 不在指定范围内的数据；
# 删除 speed 不在指定范围内的数据
# 删除任何含有NaN的行
def removeLongLatSpeed(files):
    for n in range(len(files)):
        data = pd.read_csv(path + files[n])
        print("files[n]:", files[n], "data.shape:", data.shape)
        df = pd.DataFrame(data = data,columns = head)
        df['Longitude'] = data['Longitude']/10000000
        df['Latitude'] =  data['Latitude']/10000000
        df = df[(df['Longitude'] <= right) & (df['Longitude'] >= left)]
        df = df[(df['Latitude'] <= up) & (df['Latitude'] >= bottom)]
        df = df[(df['Speed']>=0) & (df['Speed']<=150)]
        df = df.dropna(axis = 0, how = 'any') # 删除表中任何含有NaN的行
        print("df.shape:", df.shape)
        df.to_csv(path + files[n][:2]+'.csv',index = False, header = head)
        
def datetime_timestamp(day):
    datet0=datetime.datetime(2015,4,day,0,0,0)
    timestampt0=time.mktime(datet0.timetuple())
    
    datet1=datetime.datetime(2015,4,day,1,0,0)
    timestampt1=time.mktime(datet1.timetuple())
    
    return timestampt0,timestampt1

def splitTime1(a0, b1):
    a = a0
    b = b1
    otherList = []
    for n in range(len(files)):
    #for n in range(2):
        data = pd.read_csv(path + files[n])
        print('files:',files[n], ",  data.shape:", data.shape, ",  a and b:", a,b)
        df = pd.DataFrame(data = data)
        df_in_ab = df[(df.TimeStamp>=a) & (df.TimeStamp <b)] # 获取时间在 [a,b)
        print("df_in_ab:",df_in_ab.shape)
        df_in_ab.to_csv(path+files[n][:2]+'.csv', index = None, header = head)
        df_notin_ab = df[(df.TimeStamp<a)|(df.TimeStamp >=b)]
        print("df_notin_ab:", df_notin_ab.shape)
        otherList.append(df_notin_ab)
        a += 3600
        b += 3600    
        print()
    otherTime = otherList[0].append(otherList[1:])
    print(otherTime.shape)

    dftomorrow = otherTime[(otherTime.TimeStamp >= a)]
    dfyesterday = otherTime[(otherTime.TimeStamp < a0)]
    dfcurrent = otherTime[(otherTime.TimeStamp>= a0) & (otherTime.TimeStamp < a)]

    dftomorrow.to_csv(path+'dftomorrow.csv', index = None, header = head )
    dfyesterday.to_csv(path+'dfyesterday.csv', index = None, header = head)
    dfcurrent.to_csv(path+'dfcurrent.csv', index = None, header = head)

print("开始运行......")
now = time.clock()

files = obtainFiles()  
print("files:", files)

addTitle(files)
print("添加header完成。")

removeLongLatSpeed(files)
print("移除经度，维度，速度不在给定区域的数据完成。")

t0, t1= datetime_timestamp(Day)
print("start time:",t0, "end time:", t1)

splitTime1(t0, t1)
print("时间按小时分裂第一轮完成。")

print("当前路径：", path)

print("运行完毕！耗时%f分钟。"%((time.clock()-now)/60))   








# import numpy as np
# import pandas as pd
# import os
# import time, datetime
# import math

# currentpath = os.getcwd()

# temp = 'd07_w3'
# path = currentpath + '/' + temp + '/'

# title = ["DataTime","UniqueID","DeviceType","Company","DeviceID","Flag","FilterFlag",
#           "EvelationFlag","Satellite","Heading","Speed","EvalationUnit","Evalation",
#           "Status","Event","Longitude","Latitude","BJ-Longitude","BJ-Latitude","TimeStamp"]

# head = ['Longitude','Latitude','Speed','DeviceID','TimeStamp','Status','Heading']

# bottom=30.012
# up=30.4439     
# left=119.8691 
# right=120.461
    
# def obtainFiles():
#     files = []
#     for i in range(24):
#         if len(str(i))<2:
#             i = '0' + str(i) + '.csv'
#         else:
#             i = str(i)+ '.csv'
#         files.append(i)
#     return files

# # 为每个文件添加 title 行
# def addTitle(files):
#     for i in range(len(files)):
#         data = pd.read_csv(path + files[i], header = None)
#         insertRow = pd.DataFrame([title])
#         data = insertRow.append(data, ignore_index = True)
#         data.to_csv(path+files[i],header = None, index = None)
#         print(path+files[i])
 
# # 删除 long 和 lat 不在指定范围内的数据；
# # 删除 speed 不在指定范围内的数据
# # 删除任何含有NaN的行
# def removeLongLatSpeed(files):
#     for n in range(len(files)):
#         data = pd.read_csv(path + files[n])
#         print("files[n]:", files[n], "data.shape:", data.shape)
#         df = pd.DataFrame(data = data,columns = head)
#         df['Longitude'] = data['Longitude']/10000000
#         df['Latitude'] =  data['Latitude']/10000000
#         df = df[(df['Longitude'] <= right) & (df['Longitude'] >= left)]
#         df = df[(df['Latitude'] <= up) & (df['Latitude'] >= bottom)]
#         df = df[(df['Speed']>=0) & (df['Speed']<=150)]
#         df = df.dropna(axis = 0, how = 'any') # 删除表中任何含有NaN的行
#         print("df.shape:", df.shape)
#         df.to_csv(path + files[n][:2]+'.csv',index = False, header = head)

# print("开始运行......")
# now = time.clock()

# files = obtainFiles()  
# print("files:", files)
# addTitle(files)
# removeLongLatSpeed(files)

# print("运行完毕！耗时%f分钟。"%((time.clock()-now)/60))   