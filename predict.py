import asyncio
import base64
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import librosa
import numpy as np
from tensorflow.keras.models import load_model
import websockets


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
    # 載入模型
    model = load_model('speaker.h5')

    audio_data = await websocket.recv()
    audio_binary = base64.b64decode(audio_data)
    audio_array = np.frombuffer(audio_binary, dtype=np.int16)
    mfcc_features = extract_mfcc(audio_array)

    # 進行數據歸一化
    normalized_mfcc = normalize_data(mfcc_features)
    data = normalized_mfcc.reshape(1, normalized_mfcc.shape[0], normalized_mfcc.shape[1], 1)

    # 進行預測
    prediction = model.predict(data)

    # 取得預測的說話者編號（假設是多類別分類）
    await websocket.send(str(np.argmax(prediction)))


# 啟動 WebSocket 伺服器
start_server = websockets.serve(handle_audio, "localhost", 8766)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()