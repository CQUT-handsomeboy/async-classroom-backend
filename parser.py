from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline
import re

# 匹配 {tagName key1=value1 key2=value2} 内联内容 {/tagName}
TAG_RE = re.compile(r'\{(\w+)\s*((?:\w+=\w+\s*)*)\}')

def custom_tag_rule(state: StateInline, silent: bool):
    pos = state.pos
    src = state.src

    if src[pos] != '{':
        return False

    m = TAG_RE.match(src[pos:])
    if not m:
        return False

    tag_name = m.group(1)
    attrs_str = m.group(2).strip()
    attrs = dict(attr.split('=') for attr in attrs_str.split()) if attrs_str else {}

    start = pos + m.end()
    end_tag = f'{{/{tag_name}}}'
    end = src.find(end_tag, start)
    if end == -1:
        return False

    if not silent:
        token = state.push('custom_tag', tag_name, 0)
        token.meta = {'attrs': attrs, 'tag_name': tag_name}
        token.children = []
        state.md.inline.parse(src[start:end], state.md, state.env, token.children)

    state.pos = end + len(end_tag)
    return True

md = MarkdownIt()
md.inline.ruler.before('emphasis', 'custom_tag', custom_tag_rule)

def render_custom_tag(self, tokens, idx, options, env):
    token = tokens[idx]
    tag_name = token.meta['tag_name']
    attrs = token.meta['attrs']
    content = self.renderInline(token.children, options, env)
    attr_str = ' '.join(f'{k}="{v}"' for k, v in attrs.items())
    return f'<{tag_name} {attr_str}>{content}</{tag_name}>'

md.add_render_rule('custom_tag', render_custom_tag)

render = lambda text : md.render(text)

if __name__ == "__main__":
    text = "这是一个 {tag1 key1=value1 key2=value2}内联内容{/tag1}"
    html = render(text)
    print(html)