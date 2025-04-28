import re


def extract_image_url(style_string):
    pattern = r'url\("(.*?)"\)'
    match = re.search(pattern, style_string)
    if match:
        return match.group(1)
    return None


# 示例调用
style_string = 'background-image: url("https://mmbiz.qpic.cn/sz_mmbiz_jpg/OAeCMzEJygLXJOKXk8XbxXibVNeVF6WLDx2fOw9iaR5hHdcXLRR9I3STagGFr6JIKYicPokEXWiaXMBXjJKo2NKEzw/0?wx_fmt=jpeg");'
image_url = extract_image_url(style_string)
if image_url:
    print(image_url)
else:
    print("未找到有效的 URL")