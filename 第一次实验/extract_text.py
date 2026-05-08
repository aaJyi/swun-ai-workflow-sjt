import re
import sys

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

# 读取 .doc 文件并提取中文文本
with open('17782065361055.doc', 'rb') as f:
    content = f.read()

# 提取所有可能的中文字符（Unicode 范围）
text = ''
for i in range(0, len(content) - 1, 2):
    # 检查是否是中文字符的 Unicode 编码
    if content[i] >= 0x4e and content[i] <= 0x9f:
        try:
            char = content[i:i+2].decode('utf-16-le')
            if char.isprintable():
                text += char
            else:
                text += ' '
        except:
            text += ' '
    elif 32 <= content[i] < 127:
        text += chr(content[i])
    else:
        text += ' '

# 清理文本
text = re.sub(r'\s+', ' ', text).strip()
print(text.encode('utf-8', errors='ignore').decode('utf-8'))
