import re

def extract_tag_contents(text, tag_name):
    pattern = rf'<{tag_name}>(.*?)</{tag_name}>'
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

def extract_all_tags(text):
    tag_names = set(re.findall(r'<([a-zA-Z0-9]+)>', text))
    
    result = {}
    for tag in tag_names:
        contents = extract_tag_contents(text, tag)
        if contents:
            result[tag] = contents
    
    return result

def extract_top_level_tags_in_order(text):
    results = []
    pattern = r'<([a-zA-Z0-9]+)>(.*?)</\1>'
    matches = re.findall(pattern, text, re.DOTALL)
    for i, (tag_name, content) in enumerate(matches, 1):
        result = {}
        result["tag"] = tag_name
        result["content"] =content
        results.append(result)
    return results