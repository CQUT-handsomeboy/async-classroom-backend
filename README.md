> [!NOTE]  
> 不可使用Python 3.13或更高版本，经测试会导致Manim-Voiceover依赖安装失败。
> 建议直接使用Python 3.11.9与笔者保持一致。


```powershell
# 安装依赖。
mkdir .venv && py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 运行
python meta.py
manim -pql .\result.py MainAnimation --disable_caching
```

编辑`.env`环境变量文件。
```
TTS_URL=https://api.siliconflow.cn/v1
TTS_KEY=sk-xxx # 需要硅基流动的API
```