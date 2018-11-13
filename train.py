import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

#分類対象のカテゴリーを選ぶ
categories = ["asuka", "ikoma", "ikuta", "maiyan", "nanase", "yasushi"]

nb_classes = len(categories)

#画像データを読み込み

X_train, X_test, y_train, y_test = np.load("./6obj.npy")

X_train = X_train.astype("float") / 256
X_test = X_test.astype("float") / 256
y_train = np_utils.to_categorical(y_train, nb_classes)
y_test = np_utils.to_categorical(y_test, nb_classes)

# モデルの定義
model = Sequential()
model.add(Conv2D(input_shape=(64, 64, 3), filters=32,kernel_size=(2, 2), strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(filters=32, kernel_size=(2, 2), strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=32, kernel_size=(2, 2), strides=(1, 1), padding="same"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(256))
model.add(Activation("sigmoid"))
model.add(Dense(128))
model.add(Activation('sigmoid'))
model.add(Dropout(0.5))
model.add(Dense(6))
model.add(Activation('softmax'))

model.compile(loss='binary_crossentropy',
    optimizer=Adam(lr=1e-5),
    metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', patience=15, verbose=0)

model.fit(X_train, y_train, batch_size=64, epochs=500, validation_split=0.1, callbacks=[early_stopping])

score = model.evaluate(X_test, y_test)
print('loss=', score[0])
print('accuracy=', score[1])


#モデルを保存
model.save("my_model.h5")