import re
from mistletoe import Document
from mistletoe.block_token import BlockToken
from mistletoe.html_renderer import HtmlRenderer

class QuestionBlock(BlockToken):
    pattern = re.compile(r'^\s*<question>(.*?)</question>\s*$', re.DOTALL | re.MULTILINE)
    
    def __init__(self, match):
        self.content = match.group(1).strip()

    @classmethod
    def start(cls, line):
        return line.strip().startswith('<question>')

    @classmethod
    def read(cls, lines):
        line_buffer = [next(lines)]
        for line in lines:
            line_buffer.append(line)
            if '</question>' in line:
                break
        return cls.pattern.search(''.join(line_buffer))

class AnswerBlock(BlockToken):
    pattern = re.compile(r'^\s*<answer>(.*?)</answer>\s*$', re.DOTALL | re.MULTILINE)
    
    def __init__(self, match):
        self.content = match.group(1).strip()

    @classmethod
    def start(cls, line):
        return line.strip().startswith('<answer>')

    @classmethod
    def read(cls, lines):
        line_buffer = [next(lines)]
        for line in lines:
            line_buffer.append(line)
            if '</answer>' in line:
                break
        return cls.pattern.search(''.join(line_buffer))

class Extractor(HtmlRenderer):
    def __init__(self):
        super().__init__(QuestionBlock,AnswerBlock)
        self.questions = []
        self.answers = []

    def render_question_block(self, token):
        self.questions.append(token.content)
        return ""

    def render_answer_block(self, token):
        self.answers.append(token.content)
        return ""

with open("./foo.md","r",encoding="utf-8") as f:
    markdown_content = f.read()

with Extractor() as renderer:
    renderer.render(Document(markdown_content))
    print(renderer.questions) 
    print(renderer.answers) 