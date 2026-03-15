# 🔗 NexusBridge: Clips (Modular Edition)

> **iOS (Pythonista 3) × PyKeys × iCloud Sync** > 「キーボードから一歩も動かない」を至上命題とした、iPad mini 開発者向け動的エクスパンダー。

---

## 💎 Concept
NexusBridge の一環として開発された **Clips** は、単なるクリップボード履歴管理ツールではありません。iCloud を介した PC との連携、および Python による動的なマクロ実行を統合した「iPad 開発用コマンドパレット」です。

## 🏗 Modular Architecture
本システムは安定性と拡張性を両立させるため、以下の2層構造で設計されています。

1.  **司令塔 (`Clips.py`)**: 
    * UI（リスト・ダイアログ）の制御と履歴管理を担当。
    * **Local Storage**: 履歴 (JSON) を iPad ローカル (`~/Documents`) に保存し、iCloud 同期による UI ロック（ゾンビ・ダイアログ現象）を物理的に排除。
2.  **魔法書 (`Clips_Macro.py`)**:
    * 具体的なアクション（保存・追記・読み込み）を定義。
    * **Cloud Sync**: マクロファイル本体は iCloud 上に配置。PC で書いたコードが即座に iPad のキーボードへ反映されます。

## ⚡️ Key Features
* **Dynamic Aliases**: `;ts` → タイムスタンプ、`;path` → カレントパス等の即時展開。
* **Smart Save/Append**: `# filename` や `++ filename` 形式のテキストをクリップボードから即座に iCloud へ保存。
* **High-Speed History**: ローカル JSON による爆速の履歴アクセス。
* **Self-Healing**: UI 競合を避けるための安全な例外処理と `\u202d` プロトコルによる履歴ループ防止。

## 📂 File Structure
```text
Pythonista 3/
├── dev/my-pykeys-scripts/
│   ├── Clips.py        # 司令塔 (本体)
│   └── Clips_Macro.py  # 魔法書 (マクロ定義)
└── [Local Documents]/
    └── Clips.json      # 履歴データ (自動生成)
```

## 🚀 How to Use
* Pythonista の PyKeys 設定から Clips.py を登録。
* キーボードから Clips を起動し、リストからアクションを選択。
* マクロを追加したい場合は、Clips_Macro.py の ACTIONS リストに関数を追記するだけ。

NexusBridge Project - Transforming iPad into a powerful development workstation.
