import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras import layers, models
import asyncio
import websockets
import base64
import librosa
import numpy as np

# 定義模型
def create_model(input_shape, num_classes):
    model = models.Sequential()

    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape, strides=(2, 2), padding='same'))
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape, strides=(2, 2), padding='same'))
    model.add(layers.Conv2D(128, (3, 3), activation='relu', strides=(2, 2), padding='same'))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(num_classes, activation='softmax'))
    model.summary()
    return model

# 提取MFCC特徵
def extract_mfcc(audio_array, sample_rate=44100, n_mfcc=20):
    audio_array = audio_array.astype(np.float32)
    mfccs = librosa.feature.mfcc(y=audio_array, sr=sample_rate, n_mfcc=n_mfcc)
    return mfccs

# 進行數據歸一化
def normalize_data(data):
    mean = np.mean(data)
    std = np.std(data)
    normalized_data = (data - mean) / std
    return normalized_data

async def handle_audio(websocket, path):
    audio_data = await websocket.recv()

    # 將接收到的 base64 編碼的音頻數據解碼為二進制數據
    audio_binary = base64.b64decode(audio_data)

    # 將二進制數據轉換為NumPy數組
    audio_array = np.frombuffer(audio_binary, dtype=np.int16)

    # 提取MFCC特徵
    mfcc_features = extract_mfcc(audio_array)

    # 進行數據歸一化
    normalized_mfcc = normalize_data(mfcc_features)
    print("Normalized MFCC shape:", normalized_mfcc.shape)

    # 使用處理後的數據進行模型訓練
    num_speakers = 5
    y_labels = np.array([0])  # 請確保你的標籤數據是合適的

    input_shape = (normalized_mfcc.shape[0], normalized_mfcc.shape[1], 1)
    X_data = normalized_mfcc.reshape(1, normalized_mfcc.shape[0], normalized_mfcc.shape[1], 1)
    print("X_data shape:", X_data.shape)
    
    model = create_model(input_shape, num_speakers)

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(X_data, y_labels, epochs=10, batch_size=32)  # 使用接收到的數據進行模型訓練

    print("Received and processed audio data.")
    model.save('speaker.h5')

# 啟動 WebSocket 伺服器
start_server = websockets.serve(handle_audio, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()