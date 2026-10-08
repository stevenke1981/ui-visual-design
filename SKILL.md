---
name: ui-visual-design
description: 介面外觀設計與美化的實作指南（GUI / Web 頁面 / 瀏覽器擴充 popup / 原生桌面視窗如 Win32 GDI、WinUI、Qt、Tauri、Electron）。提供設計 token、色彩與深色模式、字級與間距、元件狀態、資料視覺的誠實原則、無障礙門檻（WCAG 2.2 AA），Apple（Liquid Glass／SF／同心圓角）與 GNOME（Adwaita／libadwaita）風格語彙，以及可執行的對比度檢查與多寬度截圖驗收工具。只要任務涉及「美化介面」「設計頁面」「改 UI / CSS / 樣式」「做一個面板／控制台／設定頁」「深色模式」「排版不好看」「按鈕／卡片／表單樣式」「Apple 風／Mac 風／iOS 風」「GNOME 風／Adwaita」，或要派子代理（含 Haiku）做任何畫面相關工作，就使用本 skill，即使使用者沒說「設計」二字。
---

# UI Visual Design

目標：做出**一眼能懂、層次分明、在淺色／深色與窄螢幕都不壞**的介面，並以截圖與數據驗收，而非憑感覺宣稱「已美化」。

適用任何畫面技術。通用原則在本檔；技術細節依需要讀：

- Web / CSS / 擴充 popup → [references/web.md](references/web.md)（token 範本、元件 CSS、深色模式、響應式、擴充 CSP 限制）
- 原生桌面（Win32 GDI 為主，其他框架通用概念）→ [references/native.md](references/native.md)
- 指定風格（Apple、GNOME／Adwaita）→ [references/styles.md](references/styles.md)（形狀、材質、字體、系統色、元件語彙、實測對比陷阱）
- 交付前驗收清單 → [references/review.md](references/review.md)

沒有指定風格時，延續專案既有識別；使用者要「更精緻、更現代」但沒指名時，可借用 styles.md 中較貼近專案個性的一種，並在回報中說明選了哪種、為什麼。

## 工作流程

1. **先讀現況再動手。** 讀既有樣式、設計文件（DESIGN-INTENT.md、README、既有 token），截一張「改前」圖。延續既有品牌色與字體，除非使用者要求換風格。美化不是重做識別。
2. **寫下 3 句意圖**：誰用、在什麼情境、最重要的一個動作是什麼。最重要的動作在視覺上必須最突出；其他元素讓位。
3. **建立或整理 token**（顏色、字級、間距、圓角、陰影），所有元件只引用 token。這讓深色模式與後續修改只需改一處。
4. **先排版與層次，後上色。** 用灰階就能看出主次，才加品牌色；顏色用來表達意義（主要動作、狀態、警告），不是裝飾。
5. **補齊元件狀態**：預設、hover、按下、focus、停用、載入中、錯誤、空狀態。缺狀態是「看起來不專業」的主因。
6. **驗收**：跑 `scripts/contrast.py`（以真實 token 指定配對）與 `scripts/shot.mjs`（或原生程式的截圖模式），親眼看每張圖，對照 [review.md](references/review.md)。回報時區分「已截圖看過」與「只改了程式碼」。

## 核心原則（附理由）

**層次靠三個槓桿：大小、粗細、顏色。** 一次用一到兩個，不要三個疊加——全部加粗加大等於沒有重點。次要文字用較淡的文字色（muted token），而非縮到看不清。

**間距用固定刻度**（4/8 基底：4, 8, 12, 16, 24, 32, 48, 64）。相關的東西靠近、不相關的拉開（接近律），比加框線更能分組。寧可先留太多空白再收，擠在一起是業餘感的最大來源。

**顏色有限且有語意。** 一個品牌主色、一個危險／錄音紅、一個警示琥珀、成功綠可與品牌合併；中性色帶一點品牌色相，不用純灰、不用純黑 #000 當文字。漸層、多種強調色只在有理由時使用。

**深色模式是重新映射 token，不是反相。** 深色底上降低飽和度、表面越「高」越亮一點（以亮度表達層級，陰影在深色下幾乎無效），強調色需重新檢查對比。

**數字用等寬數字**（`font-variant-numeric: tabular-nums`），計時器、檔案大小、表格才不會跳動。

**元件尺寸**：可點擊目標至少 24×24 CSS px（WCAG 2.2 AA 2.5.8），主要按鈕建議 40–48px 高；觸控介面以 44px 為目標。

**焦點必須看得見**（WCAG 2.4.7 AA）：2px 以上外框、與相鄰顏色 3:1。同一個 focus 色在淺色與深色底往往無法同時達標——各主題分別設定 `--focus`。

**文字對比**：一般文字 4.5:1、大字（24px 一般或 18.66px 粗體以上）3:1；有意義的非文字元素（輸入框邊框、圖示按鈕、焦點框、圖表線）3:1（WCAG 1.4.3 / 1.4.11）。純裝飾的卡片邊框與停用元件不受此限。

**動態要克制**：只用來表達狀態變化（錄音中脈動、展開收合），150–250ms；尊重 `prefers-reduced-motion`。

## 資料與狀態的誠實

畫面上的每個數值與圖形都必須來自真實資料：音量計來自真實 peak、進度條來自真實進度、歷史圖不足時留白。**禁止**隨機波形、假進度、假「完成」。預覽或示範用的合成值必須在畫面上明示（如「預覽合成值 · 非真實資料」）。狀態文字明確區分「已保存」「已取消」「失敗：原因＋下一步」，不用含糊的「完成」。

理由：使用者依畫面判斷是否真的錄到、存到；假的回饋會讓他們在錯誤時毫無察覺，比醜更糟。

## 給子代理（含 Haiku）的分工建議

派工時在 prompt 中寫明：

- 只能改哪些檔案；必須保留的 id / class / API 契約（其他代理依賴它們）。
- 要使用本 skill：「設計前讀 ~/.claude/skills/ui-visual-design/SKILL.md 與相關 reference」。
- 驗收指令與截圖路徑；要求回報「看過哪些截圖、哪些沒看」。
- 不得新增權限、外部字型或 CDN（擴充與離線 App 常有 CSP / 離線限制）。

一個代理改 HTML/CSS、另一個改行為 JS 時，先由主代理訂好 DOM 契約（id 清單、`body[data-state]` 值），避免互相等待或衝突。

## 工具

```bash
T=~/.claude/skills/ui-visual-design/scripts   # 或本 skill 實際所在目錄的 scripts/
# 對比度：先列出檔案實際的 token 名稱，再用真實名稱指定配對（預設配對只適用 web.md 的命名）
python $T/contrast.py --css path/to/style.css --list
python $T/contrast.py --css path/to/style.css --pairs "text/bg,muted/surface,focus/bg:3,brand-ink/brand"
python $T/contrast.py "#5e726a" "#f3f6f5"            # 單一顏色對；半透明色會自動合成（--base 指定底色）
# 截圖＋水平溢出量測（Node 22+，無頭 Chrome/Edge、暫時 profile）；溢出時列出超出的元素並 exit 1
node $T/shot.mjs path/to/page.html out_dir --widths 360,1280 --schemes light,dark --full
node $T/shot.mjs path/to/page.html out_dir --state preview.js   # 注入「預覽狀態」腳本，輸出檔名含 -preview
```

- 每次跑對比都用 `--pairs` 對照真實 token（文字、次要文字、焦點、按鈕字／按鈕底、狀態色文字／其底色）。缺少的 token 會列為 skip，不是通過。
- 只在某元件範圍覆寫 token 的區塊（如 `.panel { --focus: ... }`）會被拿去和頁面背景比而誤報；用 `--only` 排除，或另用該區塊實際底色的配對檢查。
- 截圖後用 Read 工具逐張檢視。`--state` 的畫面是預覽，不是功能驗收；回報時要說明。頁面依賴執行期 API（如擴充的 `chrome.*`）而報 JS 錯誤時，靜態截圖只驗證版面。
