import subprocess

# 使用 powershell 读取 doc 文件内容
result = subprocess.run(['powershell', '-Command', '''
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open("d:\\class\\人工智能\\第一次实验\\17782065361055.doc")
    $doc.Content.Text
    $doc.Close()
    $word.Quit()
'''], capture_output=True, text=True, timeout=30)

print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
