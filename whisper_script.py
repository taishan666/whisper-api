import os

import torch
import whisper
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError



class WhisperHandler:
    def __init__(self, audio_file: str = None, model_size: str = "base", download_root: str = None,
                 language: str = "auto", task: str = "transcribe",
                 prompt: dict = None):

        if not audio_file:
            raise ValueError("[!] Audio file not provided!")
        else:
            is_valid, message = self.validate_file(audio_file)
            if not is_valid:
                raise ValueError(message)

        self.available_models = whisper.available_models()
        self.audio_file = audio_file
        self.model_size = model_size if model_size in self.available_models else "base"
        self.download_root = download_root if download_root and os.path.isdir(download_root) else None
        self.language = self.detect_language() if language == 'auto' else language
        self.task = "transcribe" if task == 'translate' and self.language in ['en', 'english'] else task
        self.prompt = self.get_valid_prompts(prompt)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(self.device)
        if self.language in ['en', 'english'] and self.model_size not in ["large", "large-v1", "large-v2", "large-3"]:
            self.model_size += '.en'
            print("[!] Using english only model.")

        self.load_model = whisper.load_model(self.model_size, device=self.device, download_root=self.download_root)
        self.result = None

    def transcribe(self):
        result = self.load_model.transcribe(self.audio_file, language=self.language, task=self.task, **self.prompt)
        self.result = result
        return result

    def detect_language(self):
        model = whisper.load_model("tiny")
        audio = whisper.load_audio(self.audio_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        _, probs = model.detect_language(mel)
        return f"{max(probs, key=probs.get)}"

    @staticmethod
    def get_valid_prompts(prompts):
        if prompts is None:
            return {}
        transcribe_params = {
            "verbose": bool,
            "temperature": float,
            "compression_ratio_threshold": float,
            "logprob_threshold": float,
            "no_speech_threshold": float,
            "condition_on_previous_text": bool,
            "initial_prompt": str,
            "word_timestamps": bool,
            "prepend_punctuations": str,
            "append_punctuations": str
        }

        valid_prompts = {}

        for prompt_name, value in prompts.items():
            if prompt_name in transcribe_params and isinstance(value, transcribe_params[prompt_name]):
                valid_prompts[prompt_name] = value

        return valid_prompts

    @staticmethod
    def validate_file(file_path: str):
        if not os.path.isfile(file_path):
            return False, "File does not exist"

        try:
            AudioSegment.from_file(file_path)

            return True, "File is a valid audio file"
        except CouldntDecodeError:
            return False, "File is not a valid audio file"
