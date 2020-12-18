#載入套件
import cv2
import numpy as np
import pandas as pd
import datetime 

#寫__私人程式判定 加入__init__中

class linechart():
    def __init__(self, filename, color, Yrange, Xrange, datatype):
        self.photo = cv2.imread(filename)
        #先不處理灰階
        self.GrayFlag = 0
        #處理時間資料
        # datatype = 1 表示日期資料
        if datatype == 1:
            Start=str(Xrange[0])
            Start=f"{Start[:4]}-{Start[4:6]}-{Start[6:8]}"
            End=str(Xrange[1])
            End=f"{End[:4]}-{End[4:6]}-{End[6:8]}"
            DateSeries=[]
            for entry in pd.date_range(Start,End):
                DateSeries.append(entry.strftime("%Y%m%d"))
            self.Xrange = DateSeries
        else:
            #由小到大
            Xrange.sort()
            self.Xrange = [int(i) for i in range(int(Xrange[0]),int(Xrange[1]))]
        #由小到大
        Yrange.sort()
        self.Yrange = Yrange
        #定義顏色上下界：黑、灰、白、紅、橙、黃、綠、藍、青、紫
        #在前端貼色階圖給使用者選擇顏色區塊
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
        
    #折線圖辨識
    def CurveRecognize(self):
        HSV=cv2.cvtColor(self.photo,cv2.COLOR_BGR2HSV)
        LowerBound=np.array([self.Hue[0],self.Saturation[0],self.Value[0]])
        UpperBound=np.array([self.Hue[1],self.Saturation[1],self.Value[1]])
        mask=cv2.inRange(HSV,LowerBound,UpperBound)
        Curve=cv2.bitwise_and(self.photo,self.photo,mask=mask)
        
        if self.GrayFlag == 1:
            Curve=cv2.cvtColor(Curve,cv2.COLOR_BGR2GRAY)
            Curve=np.piecewise(Curve,[Curve<=0,Curve>0],[0,255])
            Curve=Curve.astype('uint8')
            self.photo = Curve
        else:
            self.photo = mask
        
    #找出上下界
    def LockCurve(self):
        Location=np.where(self.photo==255)
        self.photo = self.photo[
                min(Location[0]):max(Location[0])+1,
                min(Location[1]):max(Location[1])+1
            ]
        
    def smooth(self):
        kernel = 9
        times = 3
        if times > kernel:
            times = kernel
        temp = cv2.dilate(self.photo, np.ones((kernel,kernel), np.uint8), iterations = 1)
        for i in range(times):
            temp = cv2.erode(temp, np.ones((int(kernel/times),int(kernel/times)), np.uint8), iterations = 1)
        self.photo = temp
    
    def output(self):
        grid = int(self.photo.shape[1]/len(self.Xrange))
        output_y = []
        ya = self.Yrange[0]
        yb = self.Yrange[1]
        xa = 0
        xb = self.photo.shape[0]
        for i in range(len(self.Xrange)):
            result = []
            for j in range(self.photo.shape[0]):
                if self.photo[j,i*grid] == 255:
                    result.append(self.photo.shape[0] - j)
            output_y.append(ya + (yb - ya)*(np.array(result).mean() - xa)/(xb - xa))
            
        return pd.DataFrame({'X':self.Xrange,'Y':output_y})
