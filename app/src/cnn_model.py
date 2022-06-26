import os
import json
import librosa
import numpy as np
import sounddevice as sd
import soundfile as sf
from sklearn.model_selection import train_test_split
from common import *
from controller import *
import time

PATH_DATA = os.path.join('model', 'data1.json')
NUM_MFCC = 13
SAMPLE_RATE = 22050
DURATION = 1 / 5
SAMPLES_PER_TRACK = SAMPLE_RATE * DURATION

def load_data(path):
  with open(path, "r") as fp:
    data = json.load(fp)
  
  X = np.array(data["mfcc"])
  y = np.array(data["labels"])
  return X, y

def prepare_dataset(test_size, validation_size):
  # load data
  X, y = load_data(PATH_DATA)

  # create train / test split
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size)

  # create train / validation split
  X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size = validation_size)

  # 3D array (130, 13, 1)
  X_train = X_train[..., np.newaxis]  # 4D array (num_samples, 130, 13, 1)
  X_validation = X_validation [..., np.newaxis]
  X_test = X_test[..., np.newaxis]
  print('len x s:', X_test.shape)
  print('len y s:', y_test.shape)
  return X_train, X_validation, X_test, y_train, y_validation, y_test

def predict(model, X, y):
  X = X[np.newaxis, ...]
  prediction = model.predict(X) # prediction = [[0.1, 0.2, ...]]

  # extract index with max value
  predicted_index = np.argmax(prediction, axis = 1)
  print("Expected index: {}, Predicted index: {}".format(y, predicted_index[0]))
  return y == predicted_index[0]

def predict_speech(model, X):
  X = X[np.newaxis, ...]
  prediction = model.predict(X)
  predicted_index = np.argmax(prediction, axis = 1)
  if predicted_index == 0:
    print('prediction: nasal')
    return 0
  if predicted_index == 1:
    print('prediction: normal')
    return 1
  #X = X_test[i]
  #y = y_test[i]
  #predict(model, X, y)

# open microphone
# get raw audio
# extract mfcc of audio
# return mfcc array
def get_live_mfcc():
  
  silence_threshold = 0.0029

  recording = sd.rec(int(0.9 * SAMPLE_RATE), samplerate = SAMPLE_RATE, channels = 1, blocking = False)
  sd.wait()
  recravel = recording.ravel()

  #print(np.max(recravel))
  if np.max(recravel) < silence_threshold:
    return []
  #signal, sr = librosa.load(file_path, sr = SAMPLE_RATE)
  mfcc = librosa.feature.mfcc(y = recravel[0:19500],
                              sr = SAMPLE_RATE,
                              n_mfcc = NUM_MFCC,
                              n_fft = 2048,
                              hop_length = 512)
  #mfcc = librosa.feature.mfcc(signal[start_sample:finish_sample], 
  #                                    sr = sr, 
  #                                    n_fft = num_fft, 
  #                                    n_mfcc = NUM_MFCC,
  #                                    hop_length = hop_length)
  #        mfcc = mfcc.T
  mfcc = mfcc.T
  return mfcc

def get_live_mfcc2():
  duration = 1
  with sd.Stream(channels = 1, callback = sd_callback):
    sd.sleep(int(duration * 1000))

def detect_nasality(model):
  while not ctrl.THREAD_QUIT:
    #start_time = pygame.time.get_ticks()
    if (ctrl.talk_with_space is True and ctrl.space is True) or ctrl.talk_with_space is False:
      live_mfcc = get_live_mfcc()
      if len(live_mfcc) == 0:
        ctrl.a_key = False
        ctrl.d_key = False
      else:
        X = np.array(live_mfcc);
        nasal_normal = predict_speech(model, X)
        if nasal_normal == 0:
          if (ctrl.talk_with_space is True and ctrl.space is True) or ctrl.talk_with_space is False:
            ctrl.a_key = True
            ctrl.d_key = False
          else:
            ctrl.a_key = False
            ctrl.d_key = False
        if nasal_normal == 1:
          if (ctrl.talk_with_space is True and ctrl.space is True) or ctrl.talk_with_space is False:
            ctrl.d_key = True
            ctrl.a_key = False
          else:
            ctrl.a_key = False
            ctrl.d_key = False
    time.sleep(0.0001)
    #print('prediction elapsed time: ', pygame.time.get_ticks() - start_time)

def test_accuracy(model, file_path, label = 0):
  # get voice input as file
  # convert file to array
  # get mfcc from array
  # model.evaluate
  
  #prepare_dataset(0.20, 0.2)

  data, fs = sf.read(file_path, dtype='float32')
  
  mfcc = librosa.feature.mfcc(y = data[0:19500],
                              sr = SAMPLE_RATE,
                              n_mfcc = NUM_MFCC,
                              n_fft = 2048,
                              hop_length = 512)
  mfcc = mfcc.T

  X_test = np.array(mfcc)
  X_test = X_test[np.newaxis, ...]

  y_test = [label] * X_test.shape[0]
  print('ytest1 of len:', len(y_test), y_test)
  print('xtest1 of len:', len(X_test), X_test)
  y_test = np.array(y_test)
  print('ytest2 of len:', len(y_test), y_test)

  test_error, test_accuracy = model.evaluate(X_test, y_test, verbose = 1)
  print("Accuracy on test set is: {}".format(test_accuracy))
