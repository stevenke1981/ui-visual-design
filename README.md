# ui-visual-design

給 AI coding agents（Claude Code、Codex、Gemini CLI、OpenCode 等支援 `SKILL.md` 的工具）使用的介面外觀設計 skill。涵蓋 Web／CSS、瀏覽器擴充 popup、原生桌面（Win32 GDI 等），並提供 Apple（Liquid Glass）與 GNOME（Adwaita）風格語彙。

## 內容

| 檔案 | 用途 |
|---|---|
| `SKILL.md` | 工作流程、核心原則（層次、間距、顏色、深色模式、焦點、目標尺寸）、資料誠實原則、子代理分工建議 |
| `references/web.md` | 淺／深色 token 範本（已通過對比檢查）、元件 CSS、響應式、擴充 popup 限制、常見錯誤 |
| `references/styles.md` | Apple 與 GNOME 風格：形狀、材質、字體、系統色、元件語彙，以及實測的對比度陷阱 |
| `references/native.md` | 原生桌面（GDI）繪製、DPI、owner-draw 狀態、截圖驗收 |
| `references/review.md` | 交付前驗收清單 |
| `scripts/contrast.py` | WCAG 對比檢查：顏色對或掃描 CSS 自訂屬性，支援半透明合成、`--list`、`--only` |
| `scripts/shot.mjs` | 無頭 Chrome/Edge 多寬度 × 淺/深截圖，量測水平溢出並列出元素，可注入預覽狀態（Node 22+） |

## 安裝

```bash
git clone https://github.com/stevenke1981/ui-visual-design ~/.claude/skills/ui-visual-design
# 其他工具可用 symlink 指向同一份，例如：
ln -s ~/.claude/skills/ui-visual-design ~/.agents/skills/ui-visual-design
```

需求：Python 3.8+（contrast.py）、Node 22+ 與已安裝的 Chrome 或 Edge（shot.mjs，或設定 `CHROME_PATH`）。工具不下載任何東西，截圖使用暫時瀏覽器 profile。

## 依據

- WCAG 2.2：文字 4.5:1／大字 3:1（1.4.3）、非文字 3:1（1.4.11）、目標 24×24 CSS px（2.5.8）、焦點可見（2.4.7）
- Apple Liquid Glass 技術概覽與 WWDC25 設計系統 session（同心圓角、材質層）
- libadwaita CSS 變數與樣式類別文件（GNOME 48+、Adwaita Sans）

Apple、GNOME 為各自所有者之商標；本 skill 只描述設計語彙，不含其圖示、字型檔或官方元件。系統色數值為公開文件之近似值，使用前請以官方文件核對。
