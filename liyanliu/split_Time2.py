import pandas as pd
import numpy as np
import time, datetime
import os

currentpath = os.getcwd()

data = pd.read_csv("filesList.csv")
listName = data['filename']

num = 10
Day = int(listName[num][1:3])
print("listName[num]:", listName[num], "Day:", Day)

pathback = currentpath + '/'+ listName[num-1] +'/'
pathcurrent = currentpath + '/'+ listName[num] +'/'
pathforth = currentpath + '/'+ listName[num+1] +'/'
print("pathback:", pathback, ",   pathcurrent:", pathcurrent, ",  pathforth:", pathforth),print()

def obtainFiles():
    files = []
    for i in range(24):
        if len(str(i))<2:
            i = '0' + str(i) + '.csv'
        else:
            i = str(i)+ '.csv'
        files.append(i)
    return files

def timestamp_datetime(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt 

def datetime_timestamp(day):
    datet0=datetime.datetime(2015,4,day,0,0,0)
    timestampt0=time.mktime(datet0.timetuple())
    
    datet1=datetime.datetime(2015,4,day,1,0,0)
    timestampt1=time.mktime(datet1.timetuple())
    
    return timestampt0,timestampt1

def data_back_current_forth():
    databack = pd.read_csv(pathback + 'dftomorrow.csv')
    print("databack.shape:", databack.shape)
    dfback = pd.DataFrame(data = databack)

    datacurrent = pd.read_csv(pathcurrent + "dfcurrent.csv")
    print("datacurrent.shape:", datacurrent.shape)
    dfcurrent = pd.DataFrame(data = datacurrent)

    dataforth = pd.read_csv(pathforth + "dfyesterday.csv")
    print("dataforth.shape:", dataforth.shape)
    dfforth = pd.DataFrame(data = dataforth)

    dfother = dfcurrent.append([dfback, dfforth])
    print("df.shape:", dfother.shape)

    return dfother

def classify(a0,b1,files):
    a = a0
    b = b1
    for n in range(len(files)):
    #for n in range(2):
        data = pd.read_csv(pathcurrent + files[n])
        print('files:',files[n], ",  data.shape:", data.shape, ",  a and b:", a,b)
        df = pd.DataFrame(data = data)
        dfnew = dfother[(dfother.TimeStamp>=a) & (dfother.TimeStamp <b)]
        print("dfnew.shape:", dfnew.shape)
        dfnew = df.append(dfnew)
        print("dfnew.shape:", dfnew.shape)
        dfnew = dfnew.drop_duplicates(['Longitude','Latitude','Speed','DeviceID','TimeStamp']) # 去除重复值
        dfnew = dfnew.sort_values('TimeStamp',ascending=True) # 按时间升序排列
        print("dfnew.shape:", dfnew.shape)
        dfnew.to_csv(pathcurrent + files[n][:2]+'.csv',index = False, header = ['Longitude','Latitude','Speed','DeviceID','TimeStamp','Status','Heading'])
        a += 3600
        b += 3600



def timePercentage(a0,files):
    a = a0
    b = a0+600
    dt = timestamp_datetime(b)
    print(dt)

    bigList = []
    for n in range(len(files)):
    #for n in range(2):
        data = pd.read_csv(pathcurrent +files[n])
        dftest = pd.DataFrame(data = data)
        print("files:", files[n], "dftest.shape:",dftest.shape)
        countList = []
        for i in range(6):
            count = dftest[(dftest.TimeStamp>=a) & (dftest.TimeStamp <b)].shape[0]
            countList.append(count)
            #print("count:", count, "a and b:",a,b,  timestamp_datetime(a), timestamp_datetime(b))
            a = a+600
            b = b+ 600
        percentage = []
        for count in countList:
            percentage.append(count/sum(countList)*100)
        #print(percentage)
        bigList.append(percentage)
    print(len(bigList))

    with open(pathcurrent + "timePercentage.csv", 'w') as f:
        f.write("time,0-10, 10-20, 20-30, 30-40, 40-50,50-60"+'\n')
        for i in range(len(bigList)):
            f.write(str(i) +",  "+str(round(bigList[i][0], 2)) +',  '+ \
                    str(round(bigList[i][1],2)) + ',  '+str(round(bigList[i][2],2))+',  '\
                    + str(round(bigList[i][3],2))+ ',  '+str(round(bigList[i][4],2))+',  '\
                    + str(round(bigList[i][5],2))+'\n')
            
            
print("开始运行......")
now = time.clock()

files = obtainFiles()
print("files:", files)

t0, t1= datetime_timestamp(Day)
print("start time:",t0, "end time:", t1)

dfother = data_back_current_forth()

classify(t0, t1,files)
print("时间分类并按升序排列完成。")

timePercentage(t0,files)
print("计算每个小时，在对应小时的每十分钟上的比例完成。")

print("listName[num]:", listName[num], "Day:", Day)

print("运行完毕！耗时%f分钟。"%((time.clock()-now)/60)) 