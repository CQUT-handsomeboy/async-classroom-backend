from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from ex import *
from pprint import pp
from typing import List
from textwrap import dedent

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('code.py.tpl')

def ex_question(raw:str) -> List[str]:
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
def generate_code(scripts:str):
    global line_count
    lines = []
    top_levels = extract_top_level_tags_in_order(scripts)
    for top_level in top_levels:
        if top_level["tag"] == "question":
            texts = ex_question(top_level["content"])
            groups = []
            for line,formula_mask in texts:
                for i,c in enumerate(line):
                    if (formula_mask[i]) :
                        cc = f'MathTex("{c}", font_size=24)'
                        groups.append(cc)
                    else:
                        cc = f'Text("{c}", font_size=24)'
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
            print(lines)
        
    result = template.render(lines=lines)
    
    with open("./result.py","w",encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    with open("./foo.md","r",encoding="utf-8") as f:
        generate_code(f.read())