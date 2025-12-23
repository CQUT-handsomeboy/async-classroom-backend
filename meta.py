from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from ex import *
from pprint import pp
from typing import List

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('code.py.tpl')

def ex_question(raw:str) -> List[str]:
    for line in raw.split("\n"):
        if line == "": continue
        length = len(line)
        positions = [0]
        formula = False
        for i,c in enumerate(line):
            if "$" == c: 
                formula = not formula
                continue
            if formula: continue
            print(c,end="")
        # for i,pos in enumerate(positions):
        #     if i == 0: p = line[:pos]
        #     elif i == length: p = line[pos:]
        #     else: p = line[i:i+1]
        #     print(p)
def generate_code(scripts:str):   
    lines = []
    top_levels = extract_top_level_tags_in_order(scripts)
    for top_level in top_levels:
        if top_level["tag"] == "question":
            ex_question(top_level["content"])
                
    result = template.render(lines=lines)
    
    with open("./result.py","w",encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    with open("./foo.md","r",encoding="utf-8") as f:
        generate_code(f.read())