from speech_machine import CustomService
from pathlib import Path

# 测试 CustomService
service = CustomService()

print("=== 测试1: 使用 cache_dir 参数 ===")
# 模拟生成语音
test_text = "这是一个测试文本"
result = service.generate_from_text(test_text, cache_dir="media/voiceovers")

print("结果:", result)
print("original_audio 路径:", result["original_audio"])

# 检查路径是否重复
if "media" in result["original_audio"] and result["original_audio"].count("media") > 1:
    print("错误: 路径仍然重复!")
else:
    print("成功: 路径没有重复")

print("\n=== 测试2: 使用 path 参数 ===")
# 测试提供 path 参数
test_text2 = "这是另一个测试文本"
result2 = service.generate_from_text(test_text2, cache_dir="media/voiceovers", path="media/voiceovers/test_custom.mp3")

print("结果:", result2)
print("original_audio 路径:", result2["original_audio"])

print("\n=== 测试3: 使用默认 cache_dir ===")
# 测试使用默认 cache_dir
service2 = CustomService()
result3 = service2.generate_from_text("测试默认缓存目录")

print("结果:", result3)
print("original_audio 路径:", result3["original_audio"])