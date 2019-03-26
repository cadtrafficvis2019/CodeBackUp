import numpy as np
import pandas as pd
import os
import time,datetime
import math


def obtainFiles():
    files = []
    for i in range(24):
        if len(str(i))<2:
            i = '0' + str(i) + '.csv'
        else:
            i = str(i)+ '.csv'
        files.append(i)
    return files
    
files = obtainFiles()
print("files:", files)

dayfiles = ['/d01_w4/','/d02_w5/','/d03_w6/','/d04_w7/','/d05_w1/','/d06_w2/','/d07_w3/',
        '/d08_w4/','/d09_w5/','/d10_w6/','/d11_w7/','/d12_w1/','/d13_w2/','/d14_w3/','/d15_w4/',
        '/d16_w5/','/d17_w6/','/d18_w7/','/d19_w1/','/d20_w2/','/d21_w3/','/d22_w4/','/d23_w5/',
        '/d24_w6/','/d25_w7/','/d26_w1/','/d27_w2/','/d28_w3/','/d29_w4/','/d30_w5/']

dayf = 30
currentpath = os.getcwd()
path = currentpath + dayfiles[dayf-1]
print("path:,", path)


print("run......")
now = time.clock()

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
        print("The file exists")
    else:
        os.mkdir(save_father_path )
        print("The file is created")
    for item in big_dict.items():
        #print(type(item[0]),item[0],item[0][:-2])
        deviceId_path = save_father_path + item[0][:-2] + save_end_info
        with open(deviceId_path, "w", encoding = 'utf-8') as device_file:
            device_file.write('Longitude'+','+'Latitude'+','+'Speed'+','+'DeviceID'+','+'TimeStamp'+','+'Status'+','+'Heading'+'\n')
            for line in item[1] :
                device_file.write(line)             
print("运行完毕！耗时%f分钟。"%((time.clock()-now)/60))   