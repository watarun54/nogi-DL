import numpy as np
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import glob
import os
import random
 
#元画像を取り出して顔部分を正方形で囲み、64×64pにリサイズ、別のファイルにどんどん入れてく
in_dir = "./nanase/*"
out_dir = "./nanase_face_image"
in_jpg=glob.glob(in_dir)
in_fileName=os.listdir("./nanase/")
# print(in_jpg)
# print(in_fileName)
print(len(in_jpg))
for num in range(len(in_jpg)):
    image=cv2.imread(str(in_jpg[num]))
    if image is None:
        print("Not open:",line)
        continue
    
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier("./haarcascade_frontalface_alt.xml")
    # 顔認識の実行
    face_list=cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=2,minSize=(64,64))
    #顔が１つ以上検出された時
    if len(face_list) > 0:
        for rect in face_list:
            x,y,width,height=rect
            image = image[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
            if image.shape[0]<64:
                continue
            image = cv2.resize(image,(64,64))
    #顔が検出されなかった時
    else:
        print("no face")
        continue
    print(image.shape)
    #保存
    fileName=os.path.join(out_dir,str(in_fileName[num])+".jpg")
    cv2.imwrite(str(fileName),image)

in_dir = "./nanase_face_image/*"
in_jpg=glob.glob(in_dir)
img_file_name_list=os.listdir("./nanase_face_image/")
#img_file_name_listをシャッフル、そのうち2割をtest_imageディテクトリに入れる
random.shuffle(in_jpg)
import shutil
for i in range(len(in_jpg)//5):
    shutil.move(str(in_jpg[i]), "./nanase_test_image")