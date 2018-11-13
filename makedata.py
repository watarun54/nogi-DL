from PIL import Image
import os, glob
import numpy as np
import random, math
import cv2

root_dir = "./"
# categories = ["asuka_out", "ikoma_out", "ikuta_out", "maiyan_out", "nanase_out", "yasushi_out"]
categories = ["ikuta_face_image", "asuka_face_image", "maiyan_face_image", "nanase_face_image", "hashimoto_face_image"]
nb_classes = len(categories)
image_size = 64

# 画像データを読み込む
X = []  # 画像データ
Y = []  # ラベルデータ

def data_append(data, cat):
    X.append(data)
    Y.append(cat)

def add_sample(cat, fname, is_train):
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((image_size, image_size))
    data = np.asarray(img)
    X.append(data)
    Y.append(cat)
    if not is_train: return

    filter1 = np.ones((3, 3))

    flip = lambda x: cv2.flip(x, 1)
    thr = lambda x: cv2.threshold(x, 100, 255, cv2.THRESH_TOZERO)[1]
    filt = lambda x: cv2.GaussianBlur(x, (5, 5), 0)

    methods = [flip, thr, filt]

    for f in methods:
        processing_data = f(data)
        data_append(processing_data, cat)

    for f in methods[1:]:
        processing_data = flip(f(data))
        data_append(processing_data, cat)

    data_append(thr(filt(data)), cat)
    data_append(flip(thr(filt(data))), cat)


def make_sample(files, is_train):
    global X, Y
    X = []; Y = []
    for cat, fname in files:
        add_sample(cat, fname, is_train)
    return np.array(X), np.array(Y)

allfiles = []
for idx, cat in enumerate(categories):
    image_dir = root_dir + "/" + cat
    files = glob.glob(image_dir + "/*.jpg")
    for f in files:
        allfiles.append((idx, f))

random.shuffle(allfiles)
th = math.floor(len(allfiles) * 0.8)
train = allfiles[0:th]
test = allfiles[th:]
X_train, y_train = make_sample(train, True)
X_test, y_test = make_sample(test, False)
xy = (X_train, X_test, y_train, y_test)
np.save("./6obj.npy", xy)
print("ok", len(y_train))