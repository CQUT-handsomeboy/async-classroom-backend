from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from ex import *
from pprint import pp

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('code.py.tpl')

def generate_code(scripts:str):   
    lines = []
    top_levels = extract_top_level_tags_in_order(scripts)
    for top_level in top_levels:
        print(top_level["tag"])
    result = template.render(lines=lines)
    
    with open("./result.py","w",encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    with open("./foo.md","r",encoding="utf-8") as f:
        generate_code(f.read())