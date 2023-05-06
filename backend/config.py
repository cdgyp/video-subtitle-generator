# -*- coding: UTF-8 -*-  
"""
@author: Fang Yao
@file  : config.py
@time  : 2022/04/27 22:55
@desc  : 配置文件
"""
import os
from pathlib import Path
from fsplit.filesplit import Filesplit
import configparser
import platform
import stat

# 将大文件切分
# fs = Filesplit()
# FFMPEG_PATH = ''
# fs.split(file=os.path.join(FFMPEG_PATH, 'ffmpeg.exe'), split_size=50000000, output_dir=FFMPEG_PATH)


# --------------------- 请你不要改 start-----------------------------
# 项目的base目录
BASE_DIR = str(Path(os.path.abspath(__file__)).parent)
# 读取settings.ini配置
settings_config = configparser.ConfigParser()
MODE_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.ini')
if not os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.ini')):
    # 如果没有配置文件，默认使用中文
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.ini'), mode='w', encoding='utf-8') as f:
        f.write('[DEFAULT]\n')
        f.write('Interface = 简体中文\n')
        f.write('Language = auto\n')
        f.write('Mode = medium')
settings_config.read(MODE_CONFIG_PATH, encoding='utf-8')

# 读取interface下的语言配置,e.g. ch.ini
interface_config = configparser.ConfigParser()
INTERFACE_KEY_NAME_MAP = {
    '简体中文': 'ch',
    '繁體中文': 'chinese_cht',
    'English': 'en'
}
interface_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'interface',
                              f"{INTERFACE_KEY_NAME_MAP[settings_config['DEFAULT']['Interface']]}.ini")
interface_config.read(interface_file, encoding='utf-8')

ASR_MODEL_BASE = os.path.join(BASE_DIR, 'models', f'{settings_config["DEFAULT"]["Mode"]}_asr')
FFMPEG_WIN_PATH = os.path.join(BASE_DIR, 'ffmpeg', 'win_x64')

# 查看该路径下是否有语音模型识别完整文件，没有的话合并小文件生成完整文件
if 'infer_model' not in (os.listdir(ASR_MODEL_BASE)):
    fs = Filesplit()
    fs.merge(input_dir=ASR_MODEL_BASE, cleanup=False)  # cleanup改成True会删除合并前的文件

if 'ffmpeg.exe' not in (os.listdir(FFMPEG_WIN_PATH)):
    fs = Filesplit()
    fs.merge(input_dir=FFMPEG_WIN_PATH, cleanup=False)  # cleanup改成True会删除合并前的文件

ASR_MODEL_PATH = os.path.join(ASR_MODEL_BASE, 'infer_model')

# 指定ffmpeg可执行程序路径
sys_str = platform.system()
if sys_str == "Windows":
    ffmpeg_bin = os.path.join('win_x64', 'ffmpeg.exe')
elif sys_str == "Linux":
    ffmpeg_bin = os.path.join('linux_x64', 'ffmpeg')
else:
    ffmpeg_bin = os.path.join('macos', 'ffmpeg')
FFMPEG_PATH = os.path.join(BASE_DIR, '', 'ffmpeg', ffmpeg_bin)
# 将ffmpeg添加可执行权限
os.chmod(FFMPEG_PATH, stat.S_IRWXU+stat.S_IRWXG+stat.S_IRWXO)
# --------------------- 请你不要改 end-----------------------------


# --------------------- 请根据自己的实际情况改 start-----------------
# 设置识别语言
REC_LANGUAGE_TYPE = settings_config["DEFAULT"]["Language"]

# 音频设置
SILENCE_THRESH = -70           # 小于 -70dBFS以下的为静默
MIN_SILENCE_LEN = 700          # 静默超过700毫秒则拆分
LENGTH_LIMIT = 60 * 1000       # 拆分后每段不得超过1分钟
ABANDON_CHUNK_LEN = 500        # 丢弃小于500毫秒的段

# 字幕设置
DEFAULT_SUBTITLE_FORMAT = 'srt'
DEFAULT_CONCURRENCY = 10

# 识别语言
LANGUAGE_LIST = (
    "auto", "en", 'zh-cn', 'zh-tw', 'zh-hk', 'zh-sg', 'zh-hans', 'zh-hant', "de", "es", "ru", "ko",
    "fr", "ja", "pt", "tr", "pl", "ca", "nl", "ar", "sv", "it", "id", "hi", "fi", "vi", "he", "uk", "el",
    "ms", "cs", "ro", "da", "hu", "ta", "no", "th", "ur", "hr", "bg", "lt", "la", "ml", "cy", "sk",
    "te", "fa", "lv", "bn", "sr", "az", "sl", "kn", "et", "mk", "br", "eu", "is", "hy", "ne", "mn", "bs",
    "kk", "sq", "sw", "gl", "mr", "pa", "si", "km", "sn", "yo", "so", "af", "oc", "ka", "be", "tg", "sd"
)

