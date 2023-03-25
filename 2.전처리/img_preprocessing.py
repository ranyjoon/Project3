# -*- coding: utf-8 -*-
"""img_preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/141ryyxyFSOhUo15Rpyt3YTjGT_qfVjdu
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob
import math

from sklearn.linear_model import LinearRegression
from google.colab.patches import cv2_imshow as imshow

class img_preprocessing() :
  def __init__(self, img) :
    self.self = self
    self.img = img
  
  # contrast 함수
  def contrast_roi(img, low, high):
    h, w = img.shape
    img_ = np.zeros(img.shape, dtype=np.uint8)
    for y in range(h):
      for x in range(w):
        temp = int((255 / (high - low)) * (img[y][x] - low))
        if temp > 255:
          img_[y][x] = 255
        elif temp < 0:
          img_[y][x] = 0
        else:
          img_[y][x] = temp
    return img_

  # 밝기 조정
  def bright_ness(img):
    cols, rows = img.shape[:2]
    brightness = np.sum(img) / (255 * cols * rows)
    return brightness

  # 마스크 생성
  def make_mask(img):
      img1 = img.copy()
      out1 = img1.copy()

      img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
      img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2Lab)
      out2 = img1.copy()

      blur_k = int((img1.mean()*0.5)//2)*2+1
      img1 = cv2.medianBlur(img1, blur_k)

      img1 = cv2.cvtColor(img1, cv2.COLOR_Lab2BGR)
      img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

      if img1.mean() > 100 : 
        th = img1.mean()*0.94
      else : 
        th = img1.mean()

      ret, img1 = cv2.threshold(img1, th, 255, cv2.THRESH_BINARY)

      contours, hierarchy = cv2.findContours(img1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
      max_cnt = max(contours, key=cv2.contourArea)
      mask = np.zeros(img1.shape, dtype=np.uint8)

      cv2.drawContours(mask, [max_cnt], -1, (255,255,255), -1)
      
      k = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
      mask = cv2.dilate(mask,k)


      return mask

  # 마스크 기준으로 자르기
  def cut_mask(img, mask):
      img2 = img.copy()
      height, width = img2.shape[:2]
      mask_list = mask.tolist()
      
      for y in range(int(height*0.05),height):
          if max(mask[y,int(width*0.3):int(width*0.7)]) > 0:
              start_y = y-int(height*0.05)
              break
              
      for x in range(int(width*0.05),width):
          if max(mask[int(height*0.3):int(height*0.7),x]) > 0:
              start_x = x-int(width*0.05)
              break
              
      for x in range(int(width*0.95),-1,-1):
          if max(mask[int(height*0.3):int(height*0.7),x]) > 0:
              end_x = x+int(width*0.05)
              break
              
      cut_index = 0
      if mask_list[height-1][-1] == 255 or mask_list[height-1][0] == 255:
          for n in reversed(range(height)):
              if mask_list[n][0] == 0 or mask_list[n][-1] == 0:
                  cut_index = n
                  break
                  
      if cut_index == 0:
          cut_index = height

      img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY) 

      img2 = img2[start_y:(cut_index-1),start_x:end_x]
      mask = mask[start_y:(cut_index-1),start_x:end_x]

      masked = cv2.bitwise_and(img2, mask)

      return masked

  def masked_ro(img):
      img3 = img.copy()
      h, w = img3.shape[:2]
      img3 = cv2.cvtColor(img3, cv2.COLOR_RGB2BGR)
      gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

      ret, th = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
      th_li = th.tolist()

      for i in reversed(range(h)):
        if th_li[i][0] == 0 and th_li[i][-1] == 0:
          lower = i
          break

      if lower == h - 1:
        lower = int(h*0.9)

      slice5 = int(len(th)*0.05)
      upper = lower - slice5

      x,y = [],[]

      for i in range(slice5):
        cnt = th_li[i + upper].count(255)
        index = th_li[i + upper].index(255)

        x.append([i+upper])
        y.append([int((index*2 + cnt - 1)/2)])

      model = LinearRegression()
      model.fit(X=x,y=y)

      # -----------------------------------------------------------------------------------
      angle = math.atan2(h - 0, int(model.predict([[h]])) - int(model.predict([[0]])))*180/math.pi

      M = cv2.getRotationMatrix2D((w/2,h/2), angle-90, 1)
      rotate = cv2.warpAffine(img3, M, (w, h))

      for i in range(len(th[-1])):
          if th[-1][i] == 255:
              start_x = i
              break

      for i in range(len(th[-1])):
          if th[-1][i] == 255:
              end_x = i

      s_point = h - int((int(model.predict([[h]])-start_x)) * math.tan(math.pi*((90-angle)/180)))
      e_point = h - int((end_x - int(model.predict([[h]]))) * math.tan(math.pi*((angle-90)/180)))

      point = max(s_point, e_point)
      img_ro = rotate[:point]

      return img_ro

  def bone_extraction(img,a,b,d,e):
    img1 = img
    if img_preprocessing.bright_ness(img1) > 0.8:
      img1 = np.clip(img1 - 80., 0, 255).astype(np.uint8)
    elif img_preprocessing.bright_ness(img1) > 0.75:
      img1 = np.clip(img1 - 50., 0, 255).astype(np.uint8)
    elif img_preprocessing.bright_ness(img1) > 0.65:
      img1 = np.clip(img1 - 30., 0, 255).astype(np.uint8)
    else: img1 = np.clip(img1 - 10., 0, 255).astype(np.uint8)

    img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2BGR)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2Lab)
    out1 = img1.copy()

    k = cv2.getStructuringElement(cv2.MORPH_CROSS, (a, a))
    img1 = cv2.morphologyEx(img1, cv2.MORPH_TOPHAT, k)

    img1 = cv2.bilateralFilter(img1,-1, d, e)

    img1 = cv2.cvtColor(img1, cv2.COLOR_Lab2BGR)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    out1 = img1.copy()

    img1 = cv2.normalize(img1, None, 0, 255, cv2.NORM_MINMAX)
    img1 = cv2.equalizeHist(img1)
    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(3,3))
    img1 = clahe.apply(img1)

    ret, mask = cv2.threshold(img1, np.mean(img1), 255, cv2.THRESH_BINARY)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(mask, contours, -1, (255,255,255), -1)


    #### 강 조
    img2 = img.copy()
    if img_preprocessing.bright_ness(img2) > 0.8:
      img2 = np.clip(img2 - 80., 0, 255).astype(np.uint8)
    elif img_preprocessing.bright_ness(img2) > 0.75:
      img2 = np.clip(img2 - 50., 0, 255).astype(np.uint8)
    elif img_preprocessing.bright_ness(img2) > 0.65:
      img2 = np.clip(img2 - 30., 0, 255).astype(np.uint8)
    else: img2 = np.clip(img2 - 10., 0, 255).astype(np.uint8)

    # 모폴로지
    k2 = cv2.getStructuringElement(cv2.MORPH_CROSS,(b,b))
    img2 = cv2.morphologyEx(img2, cv2.MORPH_TOPHAT, k2)

    # contrast
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    if img2.mean() <= 15:
        low = img2.mean() * 3.2
        high = img2.mean() * 3.6
    elif img2.mean() <= 20:
        low = img2.mean() * 3
        high = img2.mean() * 3.6
    else:
        low = img2.mean() * 3
        high = img2.mean() * 3.7

    img2 = cv2.blur(img2,(2,2))
    img2 = img_preprocessing.contrast_roi(img2, low, high)

    # 컨투어
    contours, hierarchy = cv2.findContours(img2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img2, contours, -1, (255, 255, 255), -1)

    img2 = cv2.bitwise_and(img2, mask) 
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    img2 = cv2.blur(img2,(2,2))
    img2 = cv2.resize(img2, (600, 800))

    return img2

  def preprocession(img):
    mask = img_preprocessing.make_mask(img)
    masked = img_preprocessing.cut_mask(img, mask)
    img_ro = img_preprocessing.masked_ro(masked)
    img = img_preprocessing.bone_extraction(img_ro, 60,55,50,25)
    
    return img

from tqdm import tqdm

def save(img_path, save_path) :
  gender_li = ["Female", "Male"]
  img_path = img_path

  for g in gender_li :
    start, end = 0, 0
    if g == "Female" :
      start, end = 1, 573
    elif g == "Male" :
      start, end = 1, 666

    for i in tqdm(range(start, end)) :
      try :
        img = cv2.imread(img_path+f"{g}/{i}_{g[0]}.jpg", cv2.IMREAD_COLOR)
        img = img_preprocessing.preprocession(img)
        #imshow(img)  
        cv2.imwrite(f'{save_path}{g}/{i}_{g[0]}.jpg',img )
      except :
        print(f"오류 > {i}_{g[0]}.jpg")
        continue

