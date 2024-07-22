import os
import tempfile
import time

import uvicorn
from fastapi import FastAPI, UploadFile, File, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from whisper_script import WhisperHandler

app = FastAPI()
security = HTTPBearer()
env_bearer_token = os.getenv("ACCESS_TOKEN", 'sk-tarzan')
model_size = os.getenv("MODEL_SIZE", "base")
language = os.getenv("LANGUAGE", "Chinese")
whisper_handler = WhisperHandler(model_size=model_size, download_root=os.path.dirname(__file__))


def cleanup_temp_file(path):
    if os.path.exists(path):
        os.remove(path)


# 语音识别
@app.post("/v1/audio/transcriptions")
async def transcribe(file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Security(security)):
    if env_bearer_token is not None and credentials.credentials != env_bearer_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"text": audio_to_text(file, 'transcribe')}


# 语音翻译
@app.post("/v1/audio/translations")
async def translate(file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Security(security)):
    if env_bearer_token is not None and credentials.credentials != env_bearer_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"text": audio_to_text(file, 'translate')}


def audio_to_text(file, task):
    start_time = time.time()
    max_file_size = 500 * 1024 * 1024
    if file.size > max_file_size:
        raise HTTPException(status_code=400, detail="File is too large")
    try:
        temp_path = os.path.join(tempfile.gettempdir(), file.filename)
        # 检查文件是否存在
        if not os.path.exists(temp_path):
            print(f"文件 {temp_path} 不存在.")
        result = whisper_handler.transcribe(temp_path, language=language, task=task)
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail=str(ex))
    end_time = time.time()
    print(f"audio to text took {end_time - start_time:.2f} seconds")
    return result['text']


if __name__ == "__main__":
    try:
        uvicorn.run("main:app", reload=True, host="0.0.0.0", port=3003)
    except Exception as e:
        print(f"API启动失败！\n报错：\n{e}")
