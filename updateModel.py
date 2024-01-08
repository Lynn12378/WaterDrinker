import asyncio
import os

import websockets
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from tensorflow.keras.models import load_model
import base64
import numpy as np
import librosa

# 載入現有模型
existing_model = load_model('speaker.h5')

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

# 獲取和處理新數據
async def handle_audio(websocket, path):
    new_audio_data = await websocket.recv()
    new_audio_binary = base64.b64decode(new_audio_data)
    new_audio_array = np.frombuffer(new_audio_binary, dtype=np.int16)
    new_mfcc_features = extract_mfcc(new_audio_array)

    # 進行數據歸一化
    new_normalized_mfcc = normalize_data(new_mfcc_features)
    X_new_data = new_normalized_mfcc.reshape(1, new_normalized_mfcc.shape[0], new_normalized_mfcc.shape[1], 1)

    # 更新模型
    num_speakers = 5  # 更新時使用的類別數，確保與原始模型一致
    y_new_labels = np.array([1])  # 根據新數據的真實類別設置標籤
    existing_model.fit(X_new_data, y_new_labels, epochs=5, batch_size=32)  # 使用新數據進行進一步訓練

    # 保存更新後的模型
    existing_model.save('speaker.h5')

# 啟動 WebSocket 伺服器
start_server = websockets.serve(handle_audio, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()