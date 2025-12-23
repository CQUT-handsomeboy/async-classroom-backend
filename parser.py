from markdown_it import MarkdownIt
from markdown_it.rules_inline import StateInline
import re

TAG_RE = re.compile(r'\{tag\s+(\w+)=(\w+)\}')

def custom_tag_rule(state: StateInline, silent: bool):
    pos = state.pos
    src = state.src

    if not src.startswith('{tag', pos):
        return False

    m = TAG_RE.match(src[pos:])
    if not m:
        return False

    key, value = m.groups()
    start = pos + m.end()
    end = src.find('{/tag}', start)
    if end == -1:
        return False

    if not silent:
        # 创建 token
        token = state.push('custom_tag', 'span', 0)
        token.meta = {'attrs': {key: value}}

        # 一定要传入一个列表，不要 None
        token.children = []
        state.md.inline.parse(src[start:end], state.md, state.env, token.children)

    state.pos = end + len('{/tag}')
    return True



md = MarkdownIt()
md.inline.ruler.before('emphasis', 'custom_tag', custom_tag_rule)

def render_custom_tag(self, tokens, idx, options, env):
    token = tokens[idx]
    attrs = token.meta['attrs']
    content = self.renderInline(token.children, options, env)
    attr_str = ' '.join(f'data-{k}="{v}"' for k, v in attrs.items())
    return f'<span {attr_str}>{content}</span>'

md.add_render_rule('custom_tag', render_custom_tag)

text = "这是一个 {tag key=value}内联内容{/tag} 的例子。"
html = md.render(text)
print(html)