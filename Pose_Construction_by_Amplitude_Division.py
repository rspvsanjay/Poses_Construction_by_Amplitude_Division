import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# def vec(framesNumber):
#   frame_x = []
#   for number3 in range(0,framesNumber):
#     frame_x.append(number3)
#   return frame_x

def smooth(vector1,framesNumber):
  vector2 = []
  #frame_x = []
  for number3 in range(0,framesNumber):
   # frame_x.append(number3)
    if number3 == 0:
      vector2.append(vector1[0])
    if number3 == 1:
      vector2.append(((vector1[0]+vector1[1])/2))
    if number3 == 2:
      vector2.append(((vector1[0]+vector1[1]+vector1[2])/3))
    if number3 == 3:
      vector2.append(((vector1[0]+vector1[1]+vector1[2]+vector1[3])/4))
    if number3 == 4:
      vector2.append(((vector1[0]+vector1[1]+vector1[2]+vector1[3]+vector1[4])/5))
    if number3>4:
      vector2.append(((vector1[number3-4]+vector1[number3-3]+vector1[number3-2]+vector1[number3-1]+vector1[number3])/5))
  return vector2

path1 = '/content/drive/MyDrive/CASIA_B036degree_Centered_Alinged/'
save_path = '/content/drive/MyDrive/CASIA_B036degree_Centered_Alinged_PEI/'
#print(path1)
subjects = os.listdir(path1)
subjectsNumber = len(subjects)
#print(subjectsNumber)
for number1 in range(0,subjectsNumber):#subjectsNumber
  path2 = path1+subjects[number1]+'/'
  sequences = os.listdir(path2)
  sequencesNumber = len(sequences)
  #print(sequencesNumber)
  
  for number2 in range(0,sequencesNumber):#sequencesNumber
    path3 = path2+sequences[number2]+'/'
    frames = os.listdir(path3)
    framesNumber = len(frames)
    print(framesNumber)
    path11 = save_path+subjects[number1]+'/'+sequences[number2]+'/'
    try:
      os.makedirs(path11)
    except OSError:
      print("Creation of the directory %s failed" % path11)
    else:
      print("Successfully created the directory %s " % path11)
    vector1 = []
    for number3 in range(0,framesNumber):
      path4 = path3+frames[number3]
      img = cv2.imread(path4)
      numberOfNonZeros = np.count_nonzero(img)
      vector1.append(numberOfNonZeros)
    print(vector1)
    vector2 = smooth(vector1,framesNumber)
    frame_x = vec(framesNumber)
    max1 = max(vector2)
    min1 = min(vector2)
    diff = max1-min1
    ap_div = diff/7
    pre_val = min1
    for_val = 0.0
    for num1 in range(0,7):
      for_val = min1 + (num1+1)*ap_div
      pose01 = np.zeros((256, 256, 3), dtype=float)
      count1 = 0
      for number3 in range(0,framesNumber):
        if (vector2[number3]>=pre_val) and (vector2[number3]<for_val):
          path4 = path3+frames[number3]
          img = cv2.imread(path4)
          pose01 = pose01+img
          count1 = count1+1
      pre_val = for_val
      pose01 = pose01/count1
      
      path2save = path11 + 'pose0'+str(num1+1)+'.png'
      print(path2save)
      cv2.imwrite(path2save, pose01)
    # plt.plot(frame_x,vector1)
    # plt.plot(frame_x,vector2, color='red')
    # plt.show()
