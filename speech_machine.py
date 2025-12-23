from manim_voiceover.services.base import SpeechService
from pathlib import Path
from pprint import pp

from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from mutagen import File
from os import getenv

import hashlib


load_dotenv()

TTS_URL = getenv("TTS_URL")
TTS_KEY = getenv("TTS_KEY")

def generate_speech(text:str,speech_file_path:Path,speaker:str):
    print("[TTS] 调用了")
    client = OpenAI(
        api_key=TTS_KEY,
        base_url=TTS_URL
    )
    print(speech_file_path)
    with client.audio.speech.with_streaming_response.create(
    model="FunAudioLLM/CosyVoice2-0.5B",
    voice=f"FunAudioLLM/CosyVoice2-0.5B:{speaker}",
    input=f"你是数学教师<|endofprompt|>{text}",
    response_format="mp3") as response:
        response.stream_to_file(speech_file_path)

get_data_hash = lambda x: hashlib.md5(x.encode(encoding='UTF-8')).hexdigest()

class CustomService(SpeechService):
    def __init__(self, voice_name="claire", **kwargs):
        # 建议设置默认缓存目录
        super().__init__(**kwargs)
        self.voice_name = voice_name

    def generate_from_text(self, text: str, cache_dir: str = None, path: str = None, **kwargs) -> dict:
        # 1. 如果没有指定路径，生成一个缓存路径
        if path is None:
            # get_data_hash 根据文本和语音配置生成唯一标识
            data_hash = get_data_hash(text)
            # 使用提供的 cache_dir 或默认的 cache_dir
            cache_dir_to_use = cache_dir if cache_dir is not None else self.cache_dir
            # 拼接成完整的缓存文件路径（假设后缀为 .mp3）
            path = Path(cache_dir_to_use) / f"{data_hash}.mp3"
        else:
            # 如果提供了 path，确保它是相对于 cache_dir 的
            cache_dir_to_use = cache_dir if cache_dir is not None else self.cache_dir

        # 确保路径是 Path 对象或字符串
        path_obj = Path(path)

        # 检查缓存是否已存在
        if path_obj.exists():
            print(f"[TTS] 缓存命中: {path}")
            audio = File(path_obj)
        else:
            print(f"[TTS] 缓存未命中，正在合成: {text}")
            generate_speech(text, speech_file_path=path_obj, speaker=self.voice_name)

            # 验证文件是否生成成功
            assert path_obj.exists()
            audio = File(path_obj)

        # 计算相对于 cache_dir 的路径
        relative_path = Path(path).relative_to(cache_dir_to_use) if Path(path).is_relative_to(cache_dir_to_use) else Path(path).name

        ret = {
            "original_text": text,
            "original_audio": str(relative_path),
            "success": True,
            "final_duration": audio.info.length,
            "path": str(relative_path)
        }

        pp(ret)
        return ret