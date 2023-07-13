import os
import matplotlib.pyplot as plt
from skimage.transform import resize
from skimage.io import imread
import numpy as np
from sklearn.model_selection import train_test_split
import random
from keras.utils import np_utils
import tensorflow as tf
import cv2

dir = 'C:\\Users\\kamil\\someThings\\python\\artificial_neural_networks\\images'
categories=['paper', 'rock', 'scissors']
loss=[]
acc=[]
for i in range(10):
    data=[]
    for category in categories:
        path = os.path.join(dir, category)
        label=categories.index(category)

        for imgs in os.listdir(path):
            imgpath = os.path.join(path, imgs)
            img=cv2.imread(imgpath, 0)
            try:
                img = cv2.resize(img, (60,40))
                data.append([img, label])
            except exception as e:
                pass

    random.shuffle(data)
    x=[]
    y=[]
    for feature, label in data:
        x.append(feature)
        y.append(label)
    x = np.array(x).reshape(-1, 60,40)
    x = x.astype('float32')
    x /= 255.0
    y = np_utils.to_categorical(y, 3)

    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=77,stratify=y)

    ann = tf.keras.models.Sequential()
    ann.add(tf.keras.layers.Flatten())
    ann.add(tf.keras.layers.Dense(units=2400,activation="relu"))
    ann.add(tf.keras.layers.Dense(units=600,activation="relu"))
    ann.add(tf.keras.layers.Dense(units=150,activation="relu"))
    ann.add(tf.keras.layers.Dense(units=30,activation="relu"))
    ann.add(tf.keras.layers.Dense(units=3,activation="sigmoid"))
    ann.compile(optimizer="adamax",loss="categorical_crossentropy",metrics=['accuracy'])
    history = ann.fit(x_train,y_train,batch_size=100,epochs = 180, validation_data = (x_test, y_test))

    score = ann.evaluate(x_test, y_test, verbose = 0 )
    print("Test loss: ", score[0])
    print("Test accuracy: ", score[1])

    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.show()

    plt.plot(history.history['loss']) 
    plt.plot(history.history['val_loss']) 
    plt.title('Model loss') 
    plt.ylabel('Loss') 
    plt.xlabel('Epoch') 
    plt.legend(['Train', 'Test'], loc='upper left') 
    plt.show()

    loss.append(score[0])
    acc.append(score[1])   

print("Test loss: ", sum(loss)/len(loss))
print("Test accuracy: ", sum(acc)/len(acc))

url=input('Enter URL of Image')
img=cv2.imread(url, 0)
cv2.imshow('image window', img)
cv2.waitKey(0)
img = cv2.resize(img, (60,40))
img = np.array(img).reshape(-1, 60,40)
img = img.astype('float32')
img /= 255.0

probability=ann.predict(img)
dic={}
for ind,val in enumerate(categories):
    dic[val] = probability[0][ind]
print("The predicted image is : " + max(dic, key=dic.get))

