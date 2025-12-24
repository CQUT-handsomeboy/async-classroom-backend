from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from ex import *
from pprint import pp
from typing import List, Dict, Tuple
from textwrap import dedent
import re
import logging
import json
from pathlib import Path

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('code.py.tpl')

def escape_string(s: str) -> str:
    """转义字符串中的特殊字符，用于Python字符串字面量"""
    # 使用json.dumps来正确处理转义，然后去掉外部的引号
    escaped = json.dumps(s, ensure_ascii=False)
    # json.dumps会添加外部的双引号，我们需要去掉它们
    return escaped[1:-1]

# 全局引用存储
quote_store: Dict[str, str] = {}
# 引用对象映射：quote_name -> (line_index, element_index)
quote_object_map: Dict[str, Tuple[int, int]] = {}

def extract_and_store_quotes(text: str) -> str:
    """提取引用标签并存储内容，返回处理后的文本"""
    global quote_store

    # 匹配 <quoteX>内容</quoteX> 标签
    pattern = r'<quote(\d+)>(.*?)</quote\1>'

    def replace_quote(match):
        quote_name = f"quote{match.group(1)}"
        content = match.group(2)
        # 存储引用内容
        quote_store[quote_name] = content
        # 替换为 $$ 占位符
        return "$$"

    result = re.sub(pattern, replace_quote, text, flags=re.DOTALL)
    return result

def parse_latex_and_text(raw:str) -> List[str]:
    lines = []
    for line in raw.splitlines():
        # 跳过空行和只包含空白字符的行
        if not line.strip():
            continue
        # 先处理引用标签
        processed_line = extract_and_store_quotes(line)

        is_in_formula_mode = False
        current_text_buffer = ""
        formula_mode_flags = []
        text_segments = []
        char_index = 0
        while char_index < len(processed_line):
            current_char = processed_line[char_index]
            if current_char == "$":
                # 检查是否是 $$（引用占位符）
                if char_index + 1 < len(processed_line) and processed_line[char_index+1] == "$":
                    # 这是 $$ 占位符
                    text_segments.append(current_text_buffer)
                    formula_mode_flags.append(is_in_formula_mode)
                    text_segments.append("$$")  # 添加 $$ 作为单独的部分
                    formula_mode_flags.append(is_in_formula_mode)
                    current_text_buffer = ""
                    char_index += 2  # 跳过两个字符
                    continue
                else:
                    # 单个 $ 字符
                    text_segments.append(current_text_buffer)
                    formula_mode_flags.append(is_in_formula_mode)
                    is_in_formula_mode = not is_in_formula_mode
                    current_text_buffer = ""
            else:
                current_text_buffer += current_char
            char_index += 1
        text_segments.append(current_text_buffer)
        formula_mode_flags.append(is_in_formula_mode)
        lines.append((text_segments,formula_mode_flags))
    return lines

current_line_number = 0
def create_animation_objects_from_text(content,lines):
    global current_line_number, quote_object_map, quote_store
    texts = parse_latex_and_text(content)
    groups = []

    for text_segments,formula_mode_flags in texts:
        for segment_index,current_segment in enumerate(text_segments):
            # 检查是否是 $$ 占位符（引用）
            if current_segment == "$$" and formula_mode_flags[segment_index]:
                # 找到对应的引用名称
                # 我们需要知道这是第几个 $$ 占位符
                # 简单方法：遍历 quote_store，找到尚未分配对象的引用
                quote_assigned = False
                for quote_name in quote_store:
                    if quote_name not in quote_object_map:
                        # 使用存储的引用内容创建 MathTex
                        quote_content = quote_store[quote_name]
                        escaped_content = escape_string(quote_content)
                        code_string = f'MathTex("{escaped_content}", font_size=24)'
                        groups.append(code_string)
                        # 记录引用对象位置
                        quote_object_map[quote_name] = (current_line_number, len(groups) - 1)
                        quote_assigned = True
                        break
                if not quote_assigned:
                    # 如果没有找到未分配的引用，跳过这个占位符
                    # 不创建空的 MathTex
                    continue
            else:
                # 跳过空的或只有空格的文本
                if current_segment.strip() == "":
                    # 如果是公式部分且为空，跳过
                    if formula_mode_flags[segment_index]:
                        continue  # 跳过空的 MathTex
                    else:
                        code_string = f'Text("", font_size=24)'  # 空的 Text 是允许的
                elif (formula_mode_flags[segment_index]) :
                    escaped_segment = escape_string(current_segment)
                    code_string = f'MathTex("{escaped_segment}", font_size=24)'
                else:
                    escaped_segment = escape_string(current_segment)
                    code_string = f'Text("{escaped_segment}", font_size=24)'
                groups.append(code_string)

        joined_groups = (",".join(groups))

        result = f"line{current_line_number} = VGroup({joined_groups}).arrange(RIGHT, buff=0.2)"
        if current_line_number != 0:
            result += f".next_to(line{current_line_number-1}, DOWN, aligned_edge=LEFT)"
        else:
            result += f".arrange(RIGHT, buff=0.3).to_corner(UL)"
        lines.append(result)
        current_line_number += 1
        groups.clear()
    
def process_narrator_with_quotes(narrator_text: str):
    """处理 narrator 文本中的引用标签，返回分段文本和对应的动画"""
    # 匹配 <quoteX/> 标签
    pattern = r'<quote(\d+)/>'

    # 分割文本，保留引用标签位置
    parts = re.split(pattern, narrator_text)

    # parts 会是 [文本, 数字, 文本, 数字, ...] 的形式
    # 我们需要将文本分段，每段对应一个 voiceover 块

    segments = []  # 每个元素是 (文本, 动画代码列表)

    i = 0
    current_text = ""
    current_animations = []

    while i < len(parts):
        if i % 2 == 0:
            # 文本部分
            text_part = parts[i].strip()
            if text_part:
                # 如果有累积的动画，先添加当前段
                if current_text or current_animations:
                    segments.append((current_text, current_animations.copy()))
                    current_text = ""
                    current_animations.clear()

                # 添加纯文本段
                segments.append((text_part, []))
        else:
            # 引用标签部分
            quote_num = parts[i]
            quote_name = f"quote{quote_num}"

            # 检查是否有对应的引用对象和存储的内容
            if quote_name in quote_object_map and quote_name in quote_store:
                line_idx, elem_idx = quote_object_map[quote_name]
                quote_content = quote_store[quote_name]

                # 将引用内容转换为可读文本
                readable_content = quote_content
                # 替换常见的数学符号
                replacements = {
                    '\\cdot': '乘',
                    '\\times': '乘',
                    '\\sin': 'sin',
                    '\\cos': 'cos',
                    '\\tan': 'tan',
                    '\\log': 'log',
                    '\\ln': 'ln',
                    '\\sqrt': '根号',
                    '\\frac': '分之',
                    '\\pi': 'pi',
                    '\\theta': 'theta',
                    '\\alpha': 'alpha',
                    '\\beta': 'beta',
                    '\\gamma': 'gamma',
                    '\\Delta': 'Delta',
                    '\\sum': '求和',
                    '\\int': '积分',
                    '\\lim': '极限'
                }

                for latex, readable in replacements.items():
                    readable_content = readable_content.replace(latex, readable)

                # 移除剩余的反斜杠
                readable_content = readable_content.replace('\\', '')

                # 添加引用文本段，包含 Indicate 动画
                segments.append((readable_content.strip(), [f"self.play(Indicate(line{line_idx}[{elem_idx}]))"]))
            else:
                # 如果没有找到引用，跳过
                pass

        i += 1

    # 添加最后一段
    if current_text or current_animations:
        segments.append((current_text, current_animations.copy()))

    # 过滤空文本段
    segments = [(text, anims) for text, anims in segments if text.strip()]

    return segments

def process_simultaneous_animation(raw:str,lines:List[str]):
    top_levels = extract_top_level_tags_in_order(raw)

    # 首先处理 answer 标签，填充 quote_object_map
    start_line_number = current_line_number
    temporary_object_lines = []  # 用于创建对象的临时列表

    for top_level in top_levels:
        # 处理 answer 标签
        if top_level["tag"] == "answer":
            # 调用 create_animation_objects_from_text，但传入临时列表
            create_animation_objects_from_text(top_level["content"],temporary_object_lines)

    # 现在 quote_object_map 应该已经被填充了
    # 收集所有 narrator 分段
    all_narrator_segments = []  # 每个元素是 (文本, 动画代码列表)

    for top_level in top_levels:
        if top_level["tag"] == "narrator":
            content = top_level["content"].replace("\n", " ").replace("\r", " ")
            # 规范化空格
            content = re.sub(r'\s+', ' ', content).strip()
            # 处理引用标签，获取分段
            segments = process_narrator_with_quotes(content)
            all_narrator_segments.extend(segments)

    # 首先，在 voiceover 块之外创建对象和播放 Write 动画
    lines.extend(temporary_object_lines)

    # 生成动画播放代码（在 voiceover 块之外）
    if current_line_number > start_line_number:
        write_lines = []
        for i in range(start_line_number, current_line_number):
            write_lines.append(f"Write(line{i})")

        if write_lines:
            write_str = ",".join(write_lines)
            lines.append(f"self.play({write_str})")
            lines.append("self.wait(2)")

    # 现在为每个 narrator 分段生成 voiceover 块
    for text_segment, animations in all_narrator_segments:
        if not text_segment:
            continue

        # 开始 with self.voiceover 块
        escaped_text = escape_string(text_segment)
        lines.append(f'with self.voiceover(text="{escaped_text}"):')

        # 添加动画代码（如果有）
        for animation in animations:
            lines.append(f"    {animation}")

        # 添加 pass 语句
        lines.append("    pass")
        
def generate_code(scripts:str):
    global current_line_number, quote_store, quote_object_map
    # 重置全局变量
    current_line_number = 0
    quote_store.clear()
    quote_object_map.clear()

    lines = []
    # 统一换行符为 \n，并规范化空白行
    scripts = scripts.replace('\r\n', '\n').replace('\r', '\n')
    # 合并连续的换行符，但保留至少一个
    while '\n\n\n' in scripts:
        scripts = scripts.replace('\n\n\n', '\n\n')
    scripts = scripts.replace("\n\n","\n")
    top_levels = extract_top_level_tags_in_order(scripts)
    for top_level in top_levels:
        if top_level["tag"] == "question" or top_level["tag"] == "answer":
            create_animation_objects_from_text(top_level["content"],lines)
            write_animations = [f"Write(line{x})" for x in range(current_line_number) ]
            write_str = ",".join(write_animations)
            lines.append(
                f"self.play({write_str})"
            )
            lines.append("self.wait(2)")

        if top_level["tag"] == "narrator":
            narrator_text:str = top_level["content"]
            # 移除换行符，但保留空格
            narrator_text = narrator_text.replace("\n", " ").replace("\r", " ")
            # 规范化空格：合并多个连续空格为单个空格
            narrator_text = re.sub(r'\s+', ' ', narrator_text).strip()

            if narrator_text:
                escaped_text = escape_string(narrator_text)
                lines.append(f'with self.voiceover(text="{escaped_text}"):')
                lines.append('    pass')
        
        if top_level["tag"] == "sametime":
            process_simultaneous_animation(top_level["content"],lines)
        
    result = template.render(lines=lines,module_path=Path(__file__).parent.__str__().replace("\\","\\\\"))
    
    with open("./result.py","w",encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    with open("./foo.md","r",encoding="utf-8") as f:
        generate_code(f.read())