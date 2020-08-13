from keras.applications.resnet50 import ResNet50, preprocess_input
model = ResNet50(include_top=False, weights='imagenet',input_shape=(224,224,3))

#false 로 할 경우, 마지막
for layer in model.layers:
    layer.trainable = True

from keras.layers import Dense, Dropout, GlobalAveragePooling2D
x = model.output
x = GlobalAveragePooling2D()(x) #tf와 양식이 동일.
x = Dropout(0.8)(x)

from keras.models import Model
#dense : 출력 class를 줄인다!
predictions = Dense(10, activation= 'softmax')(x)
model = Model(inputs = model.input, output = predictions)
print(model.summary())

from keras.preprocessing.image import ImageDataGenerator
train_datagen = ImageDataGenerator(
    rotation_range=30,
    width_shift_range=0.15,
    height_shift_range=0.15,
    horizontal_flip=True,
    preprocessing_function=preprocess_input,
    fill_mode='constant'
)

#directory = '/Users/kimwanki/developer/testcase/data/training'
#directory 별로 만들겠다.

train_generator = train_datagen.flow_from_directory(
    directory = '/home/opensw04/training',
    target_size = (224, 224),
    batch_size = 10,
    #one hot으로 만들어줌
    class_mode = 'categorical',
    #binary - > 인풋값 그대로.
    shuffle = True
)


val_datagen = ImageDataGenerator(
    preprocessing_function = preprocess_input
)


#directory 별로 만들겠다.
val_generator = val_datagen.flow_from_directory(
    directory = '/home/opensw04/val',
    target_size = (224, 224),
    batch_size = 10,
    #one hot으로 만들어줌
    class_mode = 'categorical',
    #binary - > 인풋값 그대로.
    shuffle=False
)
import math
# import keras
# keras.losses.categorical_crossentropy()
from keras import optimizers

# TODO : 저장된 모델의 경로를 불러와서 모델을 그대로 사용가능.

model.load_weights('/home/opensw04/model_resnet.h5')
model.compile(loss="categorical_crossentropy",
              optimizer=optimizers.Adam(lr=0.0001),metrics=["accuracy"])
from keras.callbacks import ModelCheckpoint

# ckpt_filepath :
checkpoint = ModelCheckpoint('/home/opensw04/model_resnet.h5', save_best_only=True,
                             monitor='val_acc',verbose=1, save_weights_only=True, mode='auto', period = 1)

callback_list = [checkpoint]
result = model.fit_generator(train_generator, steps_per_epoch= math.ceil(150/ 10),
                             epochs=100,
                             callbacks= callback_list,
                             validation_data=val_generator,
                             validation_steps= 20,
                             shuffle=True
                             )











