import atexit
import json
import os
import tempfile
import time

import uvicorn
from fastapi import FastAPI, UploadFile, File, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from whisper_script import WhisperHandler

app = FastAPI()
security = HTTPBearer()
env_bearer_token = 'sk-tarzan'


def cleanup_temp_file(path):
    if os.path.exists(path):
        os.remove(path)


with open('options.json', 'r') as options:
    # 使用json.load()函数读取并解析文件内容
    load_options = json.load(options)


# 语音识别
@app.post("/v1/audio/transcriptions")
async def transcribe(file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Security(security)):
    if env_bearer_token is not None and credentials.credentials != env_bearer_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    file_bytes = await file.read()
    return {"text": audio_to_text(file_bytes, 'transcribe')}


# 语音翻译
@app.post("/v1/audio/translations")
async def translate(file: UploadFile = File(...), credentials: HTTPAuthorizationCredentials = Security(security)):
    if env_bearer_token is not None and credentials.credentials != env_bearer_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    file_bytes = await file.read()
    return {"text": audio_to_text(file_bytes, 'translate')}


def audio_to_text(file_bytes, task):
    start_time = time.time()
    max_file_size = 500 * 1024 * 1024
    if len(file_bytes) > max_file_size:
        raise HTTPException(status_code=400, detail="File is too large")
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(file_bytes)
            temp_path = temp_audio.name
        model_size = load_options.get("model_size")
        language = load_options.get("language")
        prompts = {
            "verbose": load_options.get("verbose"),
            "temperature": load_options.get("temperature"),
            "compression_ratio_threshold": load_options.get("compression_ratio_threshold"),
            "logprob_threshold": load_options.get("logprob_threshold"),
            "no_speech_threshold": load_options.get("no_speech_threshold"),
            "condition_on_previous_text": load_options.get("condition_on_previous_text"),
            "initial_prompt": load_options.get("initial_prompt"),
            "word_timestamps": load_options.get("word_timestamps"),
            "prepend_punctuations": load_options.get("prepend_punctuations"),
            "append_punctuations": load_options.get("append_punctuations")
        }
        print('temp_path', temp_path)
        handler = WhisperHandler(temp_path, model_size=model_size, language=language, task=task, prompt=prompts)
        result = handler.transcribe()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        atexit.register(cleanup_temp_file, temp_path)
    end_time = time.time()
    print(f"audio to text took {end_time - start_time:.2f} seconds")
    return result['text']


if __name__ == "__main__":
    token = os.getenv("ACCESS_TOKEN")
    if token is not None:
        env_bearer_token = token
    try:
        uvicorn.run("main:app", reload=True, host="0.0.0.0", port=3003)
    except Exception as e:
        print(f"API启动失败！\n报错：\n{e}")
