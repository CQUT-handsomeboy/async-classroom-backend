from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from ex import *
from pprint import pp
from typing import List
from textwrap import dedent

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('code.py.tpl')

def ex_latex_and_text(raw:str) -> List[str]:
    lines = []
    for line in raw.split("\n"):
        if line == "": continue
        formula_sign = False
        res = ""
        formula_mask = []
        texts = []
        for i,c in enumerate(line):
            if "$" == c: 
                texts.append(res)
                formula_mask.append(formula_sign)
                formula_sign = not formula_sign
                res = ""
                continue
            res += c
        texts.append(res)
        formula_mask.append(formula_sign)
        lines.append((texts,formula_mask))
    return lines

line_count = 0
def ex_latex_and_text_to_add(content,lines):
    global line_count
    texts = ex_latex_and_text(content)
    groups = []
    for line,formula_mask in texts:
        for i,c in enumerate(line):
            if (formula_mask[i]) :
                cc = f'MathTex("{c}", font_size=24)'
            else:
                cc = f'Text("{c}", font_size=24)'
            cc = cc.replace('\\', '\\\\')
            groups.append(cc)
        l = (",".join(groups))
        
        result = f"line{line_count} = VGroup({l}).arrange(RIGHT, buff=0.2)"
        if line_count != 0:
            result += f".next_to(line{line_count-1}, DOWN, aligned_edge=LEFT)"
        else:
            result += f".arrange(RIGHT, buff=0.3).to_corner(UL)"
        lines.append(result)
        line_count += 1
        groups.clear()
    
def ex_sametime_to_add(raw:str,lines:List[str]):
    top_levels = extract_top_level_tags_in_order(raw)

    # 收集所有 narrator 文本
    narrator_texts = []
    for top_level in top_levels:
        if top_level["tag"] == "narrator":
            content = top_level["content"].replace("\n", " ")
            narrator_texts.append(content)

    # 合并 narrator 文本
    combined_narrator = " ".join(narrator_texts)

    # 开始 with self.voiceover 块
    lines.append(f'with self.voiceover(text="{combined_narrator}"):')

    # 记录当前行数，用于后续动画
    start_line_count = line_count

    # 创建一个临时列表来存储 with 块内部的代码
    inner_lines = []

    for top_level in top_levels:
        # 处理 answer 标签
        if top_level["tag"] == "answer":
            # 调用 ex_latex_and_text_to_add，但传入临时列表
            ex_latex_and_text_to_add(top_level["content"],inner_lines)

    # 生成动画播放代码
    if line_count > start_line_count:
        write_lines = []
        for i in range(start_line_count, line_count):
            write_lines.append(f"Write(line{i})")

        if write_lines:
            write_str = ",".join(write_lines)
            # 添加动画播放代码到临时列表
            inner_lines.append(f"self.play({write_str})")
            inner_lines.append("self.wait(2)")

    # 添加一个缩进的 pass 语句作为 with 块的结束
    inner_lines.append("pass")

    # 将临时列表中的代码添加到主列表，每行添加4个空格的缩进
    for line in inner_lines:
        lines.append(f"    {line}")
        
def generate_code(scripts:str):
    global line_count
    lines = []
    top_levels = extract_top_level_tags_in_order(scripts)
    for top_level in top_levels:
        if top_level["tag"] == "question" or top_level["tag"] == "answer":
            ex_latex_and_text_to_add(top_level["content"],lines)
            write_ = [f"Write(line{x})" for x in range(line_count) ]
            write_str = ",".join(write_)
            lines.append(
                f"self.play({write_str})"
            )
            lines.append("self.wait(2)")

        if top_level["tag"] == "narrator":
            x:str = top_level["content"]
            x = x.replace("\n","")
            cc = f"""
            with self.voiceover(text="{x}"):
            pass
            """.strip()
            lines.append(cc)
        
        if top_level["tag"] == "sametime":
            ex_sametime_to_add(top_level["content"],lines)
        
    result = template.render(lines=lines)
    
    with open("./result.py","w",encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    with open("./foo.md","r",encoding="utf-8") as f:
        generate_code(f.read())