import os
import json

files = [f for f in os.listdir('.') if f.endswith('.c')]
files.sort()

html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>C 代码文件列表</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        * { box-sizing: border-box; }
        body { font-family: system-ui, -apple-system, sans-serif; max-width: 1200px; margin: 40px auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: #1e1e2f; color: white; padding: 20px 24px; }
        .header h1 { margin: 0 0 8px 0; font-size: 24px; }
        .header p { margin: 0; opacity: 0.7; }
        .file-list { padding: 0; margin: 0; list-style: none; }
        .file-item { border-bottom: 1px solid #eaeef2; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
        .file-item:hover { background: #f8fafc; }
        .file-name { font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace; font-size: 16px; font-weight: 500; color: #2c3e50; word-break: break-all; }
        .buttons { display: flex; gap: 10px; }
        button { border: none; padding: 6px 14px; border-radius: 6px; font-size: 13px; cursor: pointer; font-weight: 500; transition: all 0.2s; }
        .view-btn { background: #eef2ff; color: #1e40af; }
        .view-btn:hover { background: #1e40af; color: white; }
        .download-btn { background: #e6f7e6; color: #2e7d32; }
        .download-btn:hover { background: #2e7d32; color: white; }
        .code-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; justify-content: center; align-items: center; }
        .modal-content { background: #1e1e1e; width: 90%; max-width: 1000px; max-height: 85%; border-radius: 12px; overflow: hidden; display: flex; flex-direction: column; }
        .modal-header { padding: 16px 20px; background: #2d2d2d; color: white; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #444; }
        .modal-header h3 { margin: 0; font-family: monospace; }
        .close-btn { background: none; border: none; color: white; font-size: 24px; cursor: pointer; padding: 0 8px; }
        .close-btn:hover { color: #ff6b6b; }
        .modal-body { overflow: auto; padding: 16px; }
        pre { margin: 0; background: #1e1e1e; }
        code { font-family: 'SF Mono', Monaco, monospace; font-size: 14px; }
        @media (max-width: 600px) {
            .file-item { flex-direction: column; align-items: flex-start; }
            .buttons { width: 100%; }
            button { flex: 1; text-align: center; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📁 C 语言代码文件</h1>
        <p>共 ''' + str(len(files)) + ''' 个文件 · 点击查看代码或直接下载</p>
    </div>
    <ul class="file-list">
'''

for f in files:
    html += f'''
        <li class="file-item">
            <span class="file-name">📄 {f}</span>
            <div class="buttons">
                <button class="view-btn" data-file="{f}">👁️ 查看</button>
                <button class="download-btn" data-file="{f}">⬇️ 下载</button>
            </div>
        </li>
'''

html += '''
    </ul>
</div>

<div id="codeModal" class="code-modal">
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="modalFileName">文件名.c</h3>
            <button class="close-btn" id="closeModal">&times;</button>
        </div>
        <div class="modal-body">
            <pre><code id="modalCode" class="language-c">加载中...</code></pre>
        </div>
    </div>
</div>

<script>
    const rawBase = window.location.href.replace(/\\/[^/]*$/, '/');
    
    async function loadAndShowCode(filename) {
        const modal = document.getElementById('codeModal');
        const modalFileName = document.getElementById('modalFileName');
        const modalCode = document.getElementById('modalCode');
        
        modalFileName.textContent = filename;
        modalCode.textContent = '加载中...';
        modal.style.display = 'flex';
        
        try {
            const response = await fetch(rawBase + filename);
            const code = await response.text();
            modalCode.textContent = code;
            delete modalCode.dataset.highlighted;
            hljs.highlightElement(modalCode);
        } catch (err) {
            modalCode.textContent = '加载失败: ' + err.message;
        }
    }
    
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => loadAndShowCode(btn.dataset.file));
    });
    
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            window.location.href = rawBase + btn.dataset.file;
        });
    });
    
    document.getElementById('closeModal').onclick = () => {
        document.getElementById('codeModal').style.display = 'none';
    };
    
    window.onclick = (event) => {
        if (event.target === document.getElementById('codeModal')) {
            document.getElementById('codeModal').style.display = 'none';
        }
    };
</script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ 已生成 index.html，包含 {len(files)} 个 .c 文件")
