#!/usr/bin/env python
# coding: utf-8

# In[9]:


import cv2
import numpy as np
import pandas as pd

#shape is like[a,b] which stands for height,width
#Filter[a:b,c:d] means: call out the (a to b row) of Filter (c to d column) of Filter
#手輸Data(Banner大小, 基準rows, 基準Percentage)

#Hue = 色相(red green blue), Saturation = 飽和度, Lightness = 亮度

class barchart():
    def __init__(self, filename, color, row_number, max_value):
        self.photo = cv2.imread(filename)
        self.row_number = row_number
        self.max_value = max_value
        if color == 'black':
            self.Hue=[0,180]
            self.Saturation=[0,255]
            self.Value=[0,46]
        elif color == 'gray':
            self.Hue=[0,180]
            self.Saturation=[0,43]
            self.Value=[46,220]
        elif color == 'white':
            self.Hue=[0,180]
            self.Saturation=[0,30]
            self.Value=[221,255]
        elif color == 'red':
            self.Hue=[0,10]
            self.Saturation=[43,255]
            self.Value=[46,255]
        elif color == 'orange':
            self.Hue=[11,25]
            self.Saturation=[43,255]
            self.Value=[46,255]
        elif color == 'yellow':
            self.Hue=[26,34]
            self.Saturation=[43,255]
            self.Value=[46,255]
        elif color == 'green':
            self.Hue=[35,77]
            self.Saturation=[43,255]
            self.Value=[46,255]
        elif color == 'blue':
            self.Hue=[100,124]
            self.Saturation=[43,255]
            self.Value=[46,255]
        elif color == 'purple':
            self.Hue=[125,155]
            self.Saturation=[43,255]
            self.Value=[46,255]
        elif color == 'cyanblue':
            self.Hue=[78,99]
            self.Saturation=[43,255]
            self.Value=[46,255]
        else:
            print('error color')
        
        
    def historecognized(self):
        HSV=cv2.cvtColor(self.photo,cv2.COLOR_BGR2HSV)
        LowerBound=np.array([self.Hue[0],self.Saturation[0],self.Value[0]])
        UpperBound=np.array([self.Hue[1],self.Saturation[1],self.Value[1]])
        
        mask=cv2.inRange(HSV,LowerBound,UpperBound)

        histo=cv2.bitwise_and(self.photo,self.photo,mask=mask)

        histo=cv2.cvtColor(histo,cv2.COLOR_BGR2GRAY)
        histo=np.piecewise(histo,[histo<=0,histo>0],[0,255]) #0是黑色，255是白色，依條件assign值
        histo = histo.astype('uint8')#以int的法是呈現
        self.photo = histo

    def LockHisto(self):
        Location=np.where(self.photo == 255)#找出Image裡elements是255的位置
        self.photo = self.photo[
                min(Location[0])-2:max(Location[0])+2,
                min(Location[1])-2:max(Location[1])+2
            ]
    
    def producedata(self):
        rows,cols = self.photo.shape
        datalist =[]
        right_point = []
        result = []
        for j in range(cols):
            for i in range(rows-1):
                if  self.photo[i+1][j] == 255 and  self.photo[i][j] == 0 and  self.photo[i+1][j+1] == 0:
                    right_point.append([i+1,j])
        for i in range(len(right_point)):
            bottom_up_basic_row = self.photo.shape[0] - self.row_number
            bottom_up_finding_row = self.photo.shape[0] - right_point[i][0]
            finding_percentage = self.row_number * bottom_up_finding_row / bottom_up_basic_row
            datalist.append(finding_percentage)
        for i in datalist:
            result.append(i*10)
        return result

# bar = barchart("C:\\Users\\TsaiYiChen\\Desktop\\bar.png",'blue',4,0.41)
# bar.historecognized()
# bar.LockHisto()
# result = bar.producedata()

