import clipboard, datetime, dialogs, keyboard, os


# --- 共通設定 ---
ICLOUD_DOCS_PATH = "/private/var/mobile/Library/Mobile Documents/com~apple~CloudDocs/Pythonista 3/"

def get_macros(base_dir):
    SAVE_BASE_DIR = ICLOUD_DOCS_PATH

    ALIASES = {
        ';path':   lambda: base_dir,
        ';icloud': lambda: ICLOUD_DOCS_PATH,
        ';ver':    lambda: "v2.6 (Append/Default Optimized)",
        ';ts':     lambda: datetime.datetime.now().strftime('%Y%m%d_%H%M%S'),
    }

    def quick_save_macro():
        """ クリップボードの内容をiCloudへ保存(上書き) """
        text = clipboard.get()
        if not text: return "⚠️ Error: Clipboard is empty."
        
        # プレフィックス補完
        if not text.startswith('# '):
            text = "# Clip.txt\n" + text
            
        try:
            rel_path = text.splitlines()[0][2:].strip()
            full_path = os.path.join(SAVE_BASE_DIR, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(text)
            return f"\u202d☁️ iCloud SAVED: {rel_path}"
        except Exception as e:
            return f"⚠️ Save Error: {e}"

    def quick_append_macro():
        """ クリップボードの内容をファイルの『末尾』に追記する """
        text = clipboard.get()
        if not text: return "⚠️ Error: Clipboard is empty."
        
        # プレフィックス補完
        if not text.startswith('++ '):
            text = "++ Clip.txt\n" + text
            
        try:
            lines = text.splitlines()
            rel_path = lines[0][3:].strip()
            # 1行目(ファイル名)を除いた残りのテキストを追記
            content_to_append = "\n" + "\n".join(lines[1:]) 
            
            full_path = os.path.join(SAVE_BASE_DIR, rel_path)
            with open(full_path, 'a', encoding='utf-8') as f:
                f.write(content_to_append)
            return f"\u202d➕ APPENDED TO: {rel_path}"
        except Exception as e:
            return f"⚠️ Error: {e}"

    def import_file_macro():
        """ iCloud上のファイルを選んで読み込む(安定ソート版) """
        try:
            files_info = []
            for root, dirs, files in os.walk(SAVE_BASE_DIR):
                for f in files:
                    if f.startswith('.'): continue
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, SAVE_BASE_DIR)
                    if os.path.exists(full):
                        mtime = os.path.getmtime(full)
                        files_info.append({'rel': rel, 'mtime': mtime})
            
            if not files_info: return "⚠️ No files found."
            
            files_info.sort(key=lambda x: x['mtime'], reverse=True)
            display_list = [f"📄 {item['rel']}" for item in files_info]
            
            selected = dialogs.list_dialog('☁️ ICLOUD IMPORT', display_list)
            if selected:
                selected_rel = selected[2:]
                target_path = os.path.join(SAVE_BASE_DIR, selected_rel)
                with open(target_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            return f"⚠️ Import Error: {e}"

    def update_tree_macro():
        try:
            tree_text = f"【iCloud Tree: {datetime.datetime.now().strftime('%H:%M:%S')}】\n"
            for root, dirs, files in os.walk(SAVE_BASE_DIR):
                level = root.replace(SAVE_BASE_DIR, '').count(os.sep)
                if level > 2: continue 
                indent = '┃ ' * level
                tree_text += f"{indent}┣ 📂 {os.path.basename(root)}/\n"
                for f in files[:5]:
                    tree_text += f"{indent}┃ ┣ 📄 {f}\n"
            return tree_text
        except Exception as e:
            return f"Error: {e}"
    
    def copy_cursor_line_macro():
        cursor_line = ''.join([x if x else '' for x in keyboard.get_input_context()])
        clipboard.set(cursor_line)
        return "\u202d" + 'Cursor line Copied!'
    
    def copy_selection_macro():
        text = keyboard.get_selected_text()
        clipboard.set(text)
        return "\u202d" + 'Selection Copied!'

  

    # アクションリスト
    ACTIONS = [
        {'title': f"⌚️ {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}", 'value': lambda: datetime.datetime.now().strftime('%Y%m%d_%H%M%S')},
        {'title': '💾️ CLIP SAVE (#)', 'action': quick_save_macro},
        {'title': '📝 CLIP APPEND (++)', 'action': quick_append_macro},
        {'title': '📂 CLIP FILE', 'action': import_file_macro},
        {'title': '☁️🌳 ICLOUD TREE (Paste)', 'action': update_tree_macro},
        {'title': '📋 COPY CURSOR LINE', 'action': copy_cursor_line_macro},
        {'title': '📋 COPY SELECTIONS', 'action': copy_selection_macro},
    ]

    return ALIASES, ACTIONS
