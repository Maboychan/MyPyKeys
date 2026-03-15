# dev/my-pykeys-scripts/Clips.py
'''Clips_v2_1_4
【Clips : Modular Edition】
2026-03-14 07:42 履歴ファイルの保存場所をローカルに変更。
20260311_152535 📋 COPY CURSOR LINE を追加。
司令塔(本体)と魔法書(Macro)を分離した、拡張型エクスパンダー。

⌚️ 20260311_143421      # タイムスタンプ
💾️ CLIP SAVE (#)        # クリップボードの内容をファイルに保存
📝 CLIP APPEND (++)     # クリップボードの内容をファイルに追記
📂 CLIP FILE            # ファイルを選択してクリップボードへコピー
☁️🌳 ICLOUD TREE (Paste)# ファイルツリー
📋 COPY CURSOR LINE     # カーソル行をコピー
📋 COPY SELECTIONS      # 選択範囲をコピー

📅 TIMESTAMP            # 2026-03-11 13:27
✂ CLEAR CLIPBOADD️      # クリップボードをクリア
💣 DELEART HISTORY      # 履歴を削除‭
'''
import keyboard, dialogs, clipboard, json, os, datetime

# --- 1. 自律検知ユニット ---
CURRENT_FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(CURRENT_FILE_PATH)
LOCAL_DOCS = os.path.expanduser('~/Documents')
SCRIPT_NAME_STEM = os.path.splitext(os.path.basename(CURRENT_FILE_PATH))[0]
HISTORY_FILE = os.path.join(LOCAL_DOCS, f"{SCRIPT_NAME_STEM}.json")

MAX_HISTORY = 10

# --- 2. 魔法書(Macro)の動的ロード ---
DYNAMIC_ALIASES = {}
MACRO_ACTIONS = []
try:
    import Clips_Macro
    DYNAMIC_ALIASES, MACRO_ACTIONS = Clips_Macro.get_macros(BASE_DIR)
except ImportError:
    # マクロファイルがない場合は空のまま続行(安全設計)
    pass

# --- 3. コア・ロジック ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                content = json.load(f)
                return content if isinstance(content, list) else []
        except: return []
    return []

def save_history(history):
    if not isinstance(history, list): history = []
    seen = set()
    new_history = []
    for item in history:
        if item.get('value') in ("", "\u202d", None): continue
        if item['value'] not in seen:
            new_history.append(item); seen.add(item['value'])
    new_history = new_history[:MAX_HISTORY]
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_history, f, ensure_ascii=False, indent=2)

def add_to_history(text):
    if not text or not text.strip() or text in DYNAMIC_ALIASES: return
    history = load_history()
    title = (text.split('\n')[0][:15] + '...') if len(text) > 15 else text.split('\n')[0]
    history.insert(0, {'title': f'🕒 {title}', 'value': text})
    save_history(history)

def main():
    if not keyboard.is_keyboard():
        print(f"Clips.py: Online\nPath: {CURRENT_FILE_PATH}"); return

    input_text = clipboard.get() or keyboard.get_selected_text() or ""
    alias_item = []
    if input_text in DYNAMIC_ALIASES:
        expanded = DYNAMIC_ALIASES[input_text]()
        alias_item = [{'title': f'✨ ALIAS: {input_text} -> {expanded[:10]}...', 'value': expanded}]

    add_to_history(input_text)
    history = load_history()

    now = datetime.datetime.now()
    fixed_items = [
        {'title': f'📅 {now.strftime("%Y-%m-%d %H:%M:%S")}', 'value': now.strftime("%Y-%m-%d %H:%M:%S")},
        {'title': '✂️ CLEAR CLIPBOARD', 'value': ''},
        {'title': '💣 DELETE HISTORY', 'value': '\u202d'},
    ]

    # リスト構築
    m_sec = [{'title': '🤖 --- Macros --- 🤖', 'value': None}] if MACRO_ACTIONS else []
    all_items = alias_item + history + m_sec + MACRO_ACTIONS + [{'title': '⚙️ --- Utils --- ⚙️', 'value': None}] + fixed_items
    
    try:
        selected = dialogs.list_dialog(f'{SCRIPT_NAME_STEM.upper()} PASTER', all_items)
    except Exception as e:
        clipboard.set(str(e))
        dialogs.hud_alert(f'⚠️ error', duration=10)#####
        #dialogs.hud_alert(f'🏁Check_1', duration=10)#####

    if selected:
        keyboard.play_input_click()
        if 'action' in selected:
            dialogs.hud_alert("Executing...", duration=0.2)
            final_val = selected['action']()
        elif callable(selected.get('value')):    # 実行可能(lambuda)なら
            final_val = selected['value']()
            keyboard.insert_text(final_val)
        else:
            final_val = selected.get('value')
            keyboard.insert_text(final_val)

        if final_val is not None:
            if final_val == "\u202d":            # 💣 DELETE HISTORY
                save_history([])
                dialogs.hud_alert("History Deleted", duration=0.5)
                clipboard.set("")
            elif final_val == "":                # ✂️ CLEAR CLIPBOARD
                clipboard.set("")
                dialogs.hud_alert("Cleared", duration=0.5)
            elif final_val == "⚠️ Error":
                add_to_history(final_val)
                dialogs.hud_alert(final_val, duration=0.5)
            elif final_val[0] == "\u202d":
                dialogs.hud_alert(final_val[1:], duration=0.5)
            else:
                add_to_history(final_val)
                #dialogs.hud_alert(final_val, duration=0.5)
                dialogs.hud_alert(final_val[:15] + "...", duration=0.5)
                clipboard.set(final_val)

if __name__ == '__main__':
    main()
