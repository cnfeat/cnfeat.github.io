#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Joplin → Jekyll 博客同步工具
============================
从 Joplin 指定笔记本读取笔记，自动转换为 Jekyll 格式并同步到 _posts/ 目录。

前置条件：
  1. 在 Joplin 中开启 Web Clipper 服务：
     工具 → 选项 → Web Clipper → 启用 Web Clipper 服务
  2. 获取 API Token：
     工具 → 选项 → Web Clipper → 高级选项 → 复制 Token

用法：
  # 首次使用：列出所有笔记本，找到目标笔记本名称
  python joplin_sync.py --list

  # 同步指定笔记本（例如「博客文章」）
  python joplin_sync.py --notebook "博客文章"

  # 预览模式（不实际写入）
  python joplin_sync.py --notebook "博客文章" --dry-run

  # 强制全部重新同步
  python joplin_sync.py --notebook "博客文章" --force
"""

import requests
import os
import sys
import json
import re
import argparse
import datetime
from pathlib import Path
from urllib.parse import urljoin

# Windows 兼容：强制 UTF-8 输出，解决 emoji 编码问题
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============================================================
# 配置
# ============================================================
SCRIPT_DIR = Path(__file__).parent.resolve()
POSTS_DIR = SCRIPT_DIR / "_posts"
SYNC_STATE_FILE = SCRIPT_DIR / ".joplin_sync_state.json"
CONFIG_FILE = SCRIPT_DIR / ".joplin_sync_config.json"

# Joplin Web Clipper API 默认地址
DEFAULT_API_URL = "http://localhost:41184"
DEFAULT_TOKEN = ""


def load_config():
    """加载配置文件，如果不存在则返回默认值"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"api_url": DEFAULT_API_URL, "token": DEFAULT_TOKEN, "notebook": ""}


def save_config(config):
    """保存配置文件"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_sync_state():
    """加载同步状态"""
    if SYNC_STATE_FILE.exists():
        with open(SYNC_STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_sync_state(state):
    """保存同步状态"""
    with open(SYNC_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


class JoplinToJekyll:
    """Joplin 笔记同步到 Jekyll 博客"""

    def __init__(self, api_url, token, notebook_name, dry_run=False):
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.notebook_name = notebook_name
        self.dry_run = dry_run
        self.session = requests.Session()
        self.session.timeout = 10

    # ---------- API 请求 ----------

    def _get(self, endpoint, params=None):
        """发送 GET 请求到 Joplin API"""
        if params is None:
            params = {}
        params["token"] = self.token
        url = f"{self.api_url}/{endpoint.lstrip('/')}"
        try:
            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
        except requests.ConnectionError:
            print(f"\n❌ 无法连接到 Joplin API ({self.api_url})")
            print("   请确认：")
            print("   1. Joplin 正在运行")
            print("   2. Web Clipper 服务已启用（工具 → 选项 → Web Clipper）")
            print("   3. API Token 配置正确")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ API 请求失败: {e}")
            sys.exit(1)

    # ---------- Joplin 数据读取 ----------

    def list_notebooks(self):
        """列出所有笔记本"""
        data = self._get("folders")
        print("\n📚 Joplin 笔记本列表：\n")
        print(f"  {'名称':<30} ID")
        print(f"  {'─'*30} {'─'*20}")
        for folder in data.get("items", []):
            print(f"  {folder['title']:<30} {folder['id']}")
        print(f"\n  共 {len(data.get('items', []))} 个笔记本")
        return data.get("items", [])

    def find_notebook(self):
        """根据名称查找笔记本"""
        data = self._get("folders")
        for folder in data.get("items", []):
            if folder["title"] == self.notebook_name:
                return folder
        return None

    def get_notes_in_folder(self, folder_id):
        """获取笔记本中的所有笔记"""
        all_notes = []
        page = 1
        while True:
            data = self._get(f"folders/{folder_id}/notes", {
                "fields": "id,title,body,created_time,updated_time,source_url",
                "order_by": "created_time",
                "order_dir": "ASC",
                "limit": 100,
                "page": page,
            })
            all_notes.extend(data.get("items", []))
            if not data.get("has_more"):
                break
            page += 1
        return all_notes

    def get_note_tags(self, note_id):
        """获取笔记的标签"""
        data = self._get(f"notes/{note_id}/tags", {"fields": "id,title"})
        return [t["title"] for t in data.get("items", [])]

    # ---------- 内容转换 ----------

    @staticmethod
    def sanitize_filename(title):
        """将标题转换为安全的文件名"""
        # 保留中英文、数字、连字符、空格
        safe = re.sub(r'[^\w\u4e00-\u9fff\- ]', '', title)
        safe = re.sub(r'[ \s]+', '-', safe.strip())
        return safe[:80] if safe else "untitled"

    @staticmethod
    def clean_body(body, source_url=""):
        """清洗笔记正文"""
        lines = body.split("\n")
        cleaned = []

        for line in lines:
            # 跳过 Joplin 内部的资源链接标记（形如 [](:/xxx) 的链接）
            if re.match(r'^\[\]:/.*$', line.strip()):
                continue
            # 跳过纯资源 ID 行
            cleaned.append(line)

        text = "\n".join(cleaned).strip()

        # 如果笔记有来源 URL，在末尾添加原文链接
        if source_url:
            text += f"\n\n---\n原文链接：[{source_url}]({source_url})"

        return text

    def build_front_matter(self, note, tags):
        """构建 Jekyll Front Matter"""
        created = datetime.datetime.fromtimestamp(
            note["created_time"] / 1000, tz=datetime.timezone.utc
        )
        updated = datetime.datetime.fromtimestamp(
            note["updated_time"] / 1000, tz=datetime.timezone.utc
        )

        fm = ["---"]
        fm.append(f"title: \"{note['title']}\"")
        fm.append("layout: post")

        # 标签
        filtered_tags = [t for t in tags if t not in ("blog", "published")]
        if filtered_tags:
            tags_str = ", ".join(f'"{t}"' for t in filtered_tags)
            fm.append(f"tags: [{tags_str}]")

        fm.append(f"date: {created.strftime('%Y-%m-%d %H:%M:%S +0800')}")
        fm.append(f"joplin_id: {note['id']}")
        fm.append(f"joplin_updated: {updated.strftime('%Y-%m-%d %H:%M:%S +0800')}")
        fm.append("---")
        fm.append("")

        return "\n".join(fm)

    def note_to_post(self, note):
        """将 Joplin 笔记转换为 Jekyll 文章"""
        tags = self.get_note_tags(note["id"])
        title = note["title"]
        created = datetime.datetime.fromtimestamp(
            note["created_time"] / 1000, tz=datetime.timezone.utc
        )
        safe_title = self.sanitize_filename(title)
        date_prefix = created.strftime("%Y-%m-%d")
        filename = f"{date_prefix}-{safe_title}.md"

        front_matter = self.build_front_matter(note, tags)
        body = self.clean_body(note.get("body", ""), note.get("source_url", ""))
        # 标题由 Jekyll layout 渲染（post.html 的 {{ page.title }}），
        # 正文中不再重复添加 # 标题，避免重复显示两次
        content = front_matter + body + "\n"

        return filename, content

    # ---------- 同步逻辑 ----------

    def sync(self):
        """执行同步"""
        print(f"\n🔍 查找笔记本「{self.notebook_name}」...")
        notebook = self.find_notebook()

        if not notebook:
            print(f"\n❌ 未找到笔记本「{self.notebook_name}」")
            print("   使用 --list 查看所有笔记本，确认名称是否正确")
            sys.exit(1)

        print(f"✅ 找到笔记本：{notebook['title']} (ID: {notebook['id']})")

        # 获取笔记
        print("📥 正在获取笔记列表...")
        notes = self.get_notes_in_folder(notebook["id"])
        print(f"   共 {len(notes)} 篇笔记")

        if not notes:
            print("\n⚠️  该笔记本中没有笔记，无需同步")
            return

        # 加载同步状态
        state = load_sync_state()

        # 统计
        new_count = 0
        updated_count = 0
        skipped_count = 0
        synced_files = []

        # 确保 _posts 目录存在
        os.makedirs(POSTS_DIR, exist_ok=True)

        for note in notes:
            jid = note["id"]
            joplin_updated = note["updated_time"]

            # 检查是否需要同步
            if jid in state:
                prev_updated = state[jid].get("joplin_updated", 0)
                if joplin_updated <= prev_updated:
                    skipped_count += 1
                    continue
                status = "更新"
            else:
                status = "新增"

            # 转换为 Jekyll 文章
            filename, content = self.note_to_post(note)
            filepath = POSTS_DIR / filename

            if self.dry_run:
                print(f"  [{status}] {note['title']} → {filename} (预览)")
            else:
                # 处理文件名冲突
                counter = 1
                original_filename = filename
                while filepath.exists():
                    # 检查是否同一个 Joplin 笔记（通过 front matter 中的 joplin_id）
                    existing_jid = self._read_joplin_id(filepath)
                    if existing_jid == jid:
                        break  # 同一条笔记，直接覆盖
                    stem = original_filename.rsplit(".", 1)[0]
                    filename = f"{stem}-{counter}.md"
                    filepath = POSTS_DIR / filename
                    counter += 1

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

                if status == "新增":
                    new_count += 1
                else:
                    updated_count += 1

                print(f"  [{status}] {note['title']} → {filename}")

            # 记录同步状态
            state[jid] = {
                "filename": filename,
                "title": note["title"],
                "joplin_updated": joplin_updated,
                "synced_at": datetime.datetime.now().isoformat(),
            }
            synced_files.append(filename)

        # 保存同步状态
        if not self.dry_run:
            save_sync_state(state)

        # 输出统计
        print(f"\n{'─'*50}")
        print(f"📊 同步完成！")
        print(f"   ✨ 新增: {new_count} 篇")
        print(f"   🔄 更新: {updated_count} 篇")
        print(f"   ⏭️  跳过: {skipped_count} 篇")
        if self.dry_run:
            print(f"\n   ⚠️  这是预览模式，未实际写入文件")
            print(f"   移除 --dry-run 参数以执行真正的同步")
        else:
            print(f"\n   📂 文章已写入: {POSTS_DIR}")
            print(f"   📋 同步状态已保存: {SYNC_STATE_FILE}")
            print(f"\n   💡 接下来：")
            print(f"      git add _posts/")
            print(f"      git commit -m 'sync: Joplin 博客同步 ({new_count}+{updated_count}篇)'")
            print(f"      git push")

    @staticmethod
    def _read_joplin_id(filepath):
        """从已有文章中读取 joplin_id"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read(2000)  # 只读前 2000 字符足够
                match = re.search(r'joplin_id:\s*(\S+)', content)
                return match.group(1) if match else None
        except Exception:
            return None


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Joplin → Jekyll 博客同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python joplin_sync.py --list                     # 列出所有笔记本
  python joplin_sync.py --notebook "博客文章"       # 同步指定笔记本
  python joplin_sync.py --notebook "博客文章" --dry-run  # 预览
  python joplin_sync.py --notebook "博客文章" --force    # 强制全覆盖

首次使用请先设置 API Token:
  python joplin_sync.py --token "你的JoplinToken" --list
        """,
    )

    parser.add_argument("--list", action="store_true", help="列出所有 Joplin 笔记本")
    parser.add_argument("--notebook", "-n", type=str, help="要同步的笔记本名称")
    parser.add_argument("--token", "-t", type=str, help="Joplin Web Clipper API Token")
    parser.add_argument("--api-url", type=str, default=DEFAULT_API_URL, help="Joplin API 地址")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际写入文件")
    parser.add_argument("--force", "-f", action="store_true", help="强制全部重新同步（忽略同步状态）")

    args = parser.parse_args()

    # 加载配置
    config = load_config()
    api_url = args.api_url or config.get("api_url", DEFAULT_API_URL)
    token = args.token or config.get("token", DEFAULT_TOKEN)

    if not token:
        print("❌ 未设置 Joplin API Token")
        print("\n   请先获取 Token：")
        print("   1. 打开 Joplin → 工具 → 选项 → Web Clipper")
        print("   2. 确保「启用 Web Clipper 服务」已勾选")
        print("   3. 点击「高级选项」，复制 Authorization Token")
        print(f"\n   然后运行：")
        print(f"   python joplin_sync.py --token \"你的Token\" --list")
        sys.exit(1)

    # 保存 token 到配置
    if args.token:
        config["token"] = token
        config["api_url"] = api_url
        save_config(config)
        print("✅ Token 已保存到配置文件\n")

    # 创建同步器
    syncer = JoplinToJekyll(api_url, token, args.notebook or "", dry_run=args.dry_run)

    # --list 模式
    if args.list:
        syncer.list_notebooks()
        return

    # --notebook 模式
    if args.notebook:
        config["notebook"] = args.notebook
        save_config(config)

        if args.force:
            # 清空同步状态
            if SYNC_STATE_FILE.exists():
                SYNC_STATE_FILE.unlink()
                print("🔄 已清空同步状态（强制全覆盖模式）\n")

        syncer.sync()
        return

    # 无参数：显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
