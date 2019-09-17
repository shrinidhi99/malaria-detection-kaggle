from glob import glob

import matplotlib.pyplot as plt
from keras.applications.vgg19 import VGG19
from keras.layers import Dense, Flatten
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator

IMAGE_SIZE = [224, 224]

train_path = 'cell_images/Train'
valid_path = 'cell_images/Test'

vgg = VGG19(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)
for layer in vgg.layers:
    layer.trainable = False
folders = glob('cell_images/Train/*')

x = Flatten()(vgg.output)

prediction = Dense(len(folders), activation='softmax')(x)

model = Model(inputs=vgg.input, outputs=prediction)

model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# use the image data generator to import the images from the dataset
train_datagen = ImageDataGenerator(rescale=1. / 255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1. / 255)
training_set = train_datagen.flow_from_directory('cell_images/Train', target_size=(224, 224), batch_size=32,
                                                 class_mode='categorical')
test_set = test_datagen.flow_from_directory('cell_images/Test', target_size=(224, 224), batch_size=32,
                                            class_mode='categorical')

# fit the model
r = model.fit_generator(training_set, validation_data=test_set, epochs=5, steps_per_epoch=len(training_set),
                        validation_steps=len(test_set))
# loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('lossVal_loss')

# accuracies
plt.plot(r.history['acc'], label='train_acc')
plt.plot(r.history['val_acc'], label='val_acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')

model.save('model_vgg19.h5')
