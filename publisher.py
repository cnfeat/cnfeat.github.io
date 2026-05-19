# encoding: utf-8
"""
笨方法实验室 · 文章发布工具

在终端运行:  python publisher.py
然后在浏览器打开:  http://localhost:5001

填写标题、标签和内容，一键生成 Jekyll 文章到 _posts/ 目录。
Jekyll 服务可实时同步，无需手动创建文件。
"""

import http.server
import json
import os
import datetime
import re
import html as html_mod

PORT = 5001
POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_posts")

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>发布文章</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: #f5f5f5;
    color: #333;
    line-height: 1.6;
}
.wrapper { max-width: 800px; margin: 0 auto; padding: 30px 20px; }
h1 {
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 6px;
    color: #222;
}
.subtitle {
    font-size: 0.9rem;
    color: #999;
    margin-bottom: 30px;
}
.subtitle a { color: #00a67d; text-decoration: none; }
.form-group { margin-bottom: 16px; }
label {
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 4px;
    color: #555;
}
input[type="text"], textarea, select {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.95rem;
    font-family: inherit;
    transition: border-color 0.2s;
}
input[type="text"]:focus, textarea:focus { outline: none; border-color: #00a67d; }
textarea { resize: vertical; min-height: 400px; }
.input-row { display: flex; gap: 12px; }
.input-row .form-group { flex: 1; }
.btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 28px;
    background: #00a67d;
    color: #fff;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
}
.btn:hover { background: #008f6b; }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary {
    background: #e8e8e8;
    color: #555;
}
.btn-secondary:hover { background: #d5d5d5; }
.actions { display: flex; gap: 10px; margin-top: 20px; align-items: center; }
#message {
    padding: 10px 14px;
    border-radius: 4px;
    font-size: 0.9rem;
    display: none;
}
.success { background: #e6f7ee; color: #0e6b3e; display: block !important; }
.error { background: #fde8e8; color: #c53030; display: block !important; }
.preview-link { margin-left: auto; color: #00a67d; text-decoration: none; font-size: 0.9rem; }
.preview-link:hover { text-decoration: underline; }
.char-count { text-align: right; font-size: 0.8rem; color: #aaa; margin-top: 2px; }
.tag-hint { font-size: 0.8rem; color: #aaa; margin-top: 2px; }
.layout-option { display: flex; gap: 16px; margin-top: 4px; }
.layout-option label { font-weight: normal; display: inline-flex; align-items: center; gap: 4px; cursor: pointer; }
</style>
</head>
<body>
<div class="wrapper">
    <h1>✍️ 发布文章</h1>
    <p class="subtitle">保存至 <code>_posts/</code> · <a href="http://localhost:4000" target="_blank">预览站点 →</a></p>

    <form id="postForm">
        <div class="input-row">
            <div class="form-group">
                <label for="title">标题</label>
                <input type="text" id="title" name="title" placeholder="文章标题" required autofocus>
            </div>
            <div class="form-group">
                <label for="layout">布局</label>
                <select id="layout" name="layout">
                    <option value="default">default</option>
                    <option value="post">post</option>
                    <option value="main">main</option>
                </select>
            </div>
        </div>

        <div class="form-group">
            <label for="tags">标签（逗号分隔）</label>
            <input type="text" id="tags" name="tags" placeholder="卡片, 写作, 创作">
            <div class="tag-hint">例如：卡片, 写作, 读书</div>
        </div>

        <div class="form-group">
            <label for="content">内容（Markdown）</label>
            <textarea id="content" name="content" placeholder="在此写文章内容…"></textarea>
            <div class="char-count" id="charCount">0 字</div>
        </div>

        <div class="actions">
            <button type="submit" class="btn" id="submitBtn">📄 发布文章</button>
            <button type="reset" class="btn btn-secondary" onclick="clearAll()">清空</button>
            <div id="message"></div>
        </div>
    </form>
</div>

<script>
const form = document.getElementById('postForm');
const submitBtn = document.getElementById('submitBtn');
const msg = document.getElementById('message');
const content = document.getElementById('content');
const charCount = document.getElementById('charCount');

// 字数统计
content.addEventListener('input', () => {
    const text = content.value.replace(/\\s/g, '');
    charCount.textContent = text.length + ' 字';
});

function showMessage(text, type) {
    msg.textContent = text;
    msg.className = type;
    setTimeout(() => { msg.className = ''; }, 5000);
}

function clearAll() {
    if (confirm('确定清空所有内容？')) {
        form.reset();
        charCount.textContent = '0 字';
        msg.className = '';
    }
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ 发布中…';

    const data = {
        title: document.getElementById('title').value.trim(),
        layout: document.getElementById('layout').value,
        tags: document.getElementById('tags').value.trim(),
        content: content.value
    };

    if (!data.title) {
        showMessage('请输入标题', 'error');
        submitBtn.disabled = false;
        submitBtn.textContent = '📄 发布文章';
        return;
    }

    try {
        const resp = await fetch('/publish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await resp.json();

        if (result.success) {
            showMessage('✅ ' + result.message, 'success');
            document.getElementById('title').value = '';
            content.value = '';
            charCount.textContent = '0 字';
            document.getElementById('tags').value = '';
        } else {
            showMessage('❌ ' + result.message, 'error');
        }
    } catch (err) {
        showMessage('❌ 请求失败: ' + err.message, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = '📄 发布文章';
    }
});

// Ctrl+Enter 快捷键提交
document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        form.dispatchEvent(new Event('submit'));
    }
});
</script>
</body>
</html>"""


class PublishHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/publish':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._json_response(False, '请求数据格式错误')
                return

            title = data.get('title', '').strip()
            layout = data.get('layout', 'default').strip()
            tags_raw = data.get('tags', '').strip()
            content = data.get('content', '')

            if not title:
                self._json_response(False, '标题不能为空')
                return

            # 处理标签
            tags = [t.strip() for t in tags_raw.split(',') if t.strip()]

            # 生成文件名
            today = datetime.date.today()
            safe_title = re.sub(r'[^\w\u4e00-\u9fff\- ]', '', title)
            safe_title = re.sub(r'[ \s]+', '-', safe_title.strip())
            safe_title = safe_title[:80]
            filename = f'{today.strftime("%Y-%m-%d")}-{safe_title}.md'
            filepath = os.path.join(POSTS_DIR, filename)

            # 处理同名文件
            counter = 1
            while os.path.exists(filepath):
                filename = f'{today.strftime("%Y-%m-%d")}-{safe_title}-{counter}.md'
                filepath = os.path.join(POSTS_DIR, filename)
                counter += 1

            # 构建 front matter
            front_matter = ['---']
            front_matter.append(f'title: {title}')
            front_matter.append(f'layout: {layout}')
            if tags:
                front_matter.append(f'tags: [{", ".join(tags)}]')
            front_matter.append('---')
            front_matter.append('')

            md_content = '\n'.join(front_matter) + content

            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                self._json_response(True, f'文章已发布 → {filename}')
            except Exception as e:
                self._json_response(False, f'写入失败: {str(e)}')
        else:
            self.send_response(404)
            self.end_headers()

    def _json_response(self, success, message):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        resp = json.dumps({'success': success, 'message': message}, ensure_ascii=False)
        self.wfile.write(resp.encode('utf-8'))

    def log_message(self, format, *args):
        pass  # 安静模式


if __name__ == '__main__':
    os.makedirs(POSTS_DIR, exist_ok=True)
    server = http.server.HTTPServer(('0.0.0.0', PORT), PublishHandler)
    import sys
    import locale
    sys.stdout.reconfigure(encoding='utf-8')

    print('')
    print('  [发布工具] 笨方法实验室 - 文章发布工具')
    print('  ------------------------------------------')
    print(f'  打开浏览器访问: http://localhost:{PORT}')
    print('')
    print('  Jekyll 预览(请确保已启动): http://localhost:4000')
    print('')
    print('  按 Ctrl+C 停止服务')
    print('')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n  服务已停止。')
        server.server_close()
