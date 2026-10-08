# Web / CSS / 瀏覽器擴充

## 目錄
1. Token 範本（淺色＋深色）
2. 字級與排版
3. 元件：按鈕、卡片、輸入、分段選擇、狀態膠囊、計量條、數值磁貼
4. 響應式
5. 動態
6. 瀏覽器擴充 popup / 頁面的限制
7. 常見錯誤

## 1. Token 範本

把以下當起點，依品牌色調整。元件只寫 `var(--x)`，不直接寫 hex。

```css
:root {
  --font-ui: system-ui, "Segoe UI", "Microsoft JhengHei UI", "PingFang TC", "Noto Sans TC", sans-serif;
  --font-num: "Segoe UI", system-ui, sans-serif;

  /* 表面與文字（中性色帶一點品牌色相，不用純灰） */
  --bg: #f3f6f5;  --surface: #ffffff;  --surface-2: #eef3f1;
  --text: #1d302b;  --muted: #5a6d66;  --border: #dce5e0;  --input-border: #76887f;

  /* 語意色 */
  --brand: #146e59;  --brand-ink: #ffffff;      /* 主要動作 */
  --danger: #b3261e; --danger-ink: #ffffff;     /* 刪除、停止錄音、錯誤 */
  --warn: #8a5a00;   --warn-bg: #fff4d6;        /* 警示文字需深色才達 4.5:1 */
  --ok: #1b7a4b;
  --focus: #1f5fbf;                             /* 淺色底：深藍焦點框，3:1 以上 */

  --r-sm: 8px; --r-md: 12px; --r-lg: 16px;
  --s-1: 4px; --s-2: 8px; --s-3: 12px; --s-4: 16px; --s-5: 24px; --s-6: 32px; --s-7: 48px;
  --shadow: 0 1px 2px rgb(0 0 0 / .06), 0 8px 24px rgb(0 0 0 / .08);
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #0e1a17; --surface: #15241f; --surface-2: #1c2f29;
    --text: #e4efea; --muted: #a2b8af; --border: #2b4139; --input-border: #6f877e;
    --brand: #5fcca6; --brand-ink: #062019;     /* 深色下改亮色底配深字 */
    --danger: #ff8a80; --danger-ink: #2a0503;
    --warn: #f2c66d; --warn-bg: #3a2e12; --ok: #5fd69a;
    --focus: #f2cc73;                            /* 深色底：亮琥珀焦點框 */
    --shadow: 0 1px 2px rgb(0 0 0 / .4);
    color-scheme: dark;
  }
}
:root[data-theme="dark"] { /* 同上深色值，供手動切換 */ }
body { margin: 0; background: var(--bg); color: var(--text); font: 16px/1.6 var(--font-ui); }
```

要點：
- 深色模式不是反相：表面由深到淺表示層級（`--bg` < `--surface` < `--surface-2`），陰影弱化。
- 每個主題各自設定 `--focus`。同一個琥珀色在白底只有約 1.6:1。
- 淺色頁面中「永遠深色」的面板（如錄音面板、深色頁首）：在該面板選擇器內覆寫 `--focus`（亮色），並檢查面板內的文字／按鈕配對。
- 半透明底（如 `rgba(紅, .16)` 的狀態膠囊）上的文字要以合成後的顏色計算對比；淺色主題常需改用深色文字 token。
- 改完 token 一律跑 `scripts/contrast.py --css <file>`。

## 2. 字級與排版

- 一頁 5–7 個字級即可：12 / 14 / 16（內文）/ 18 / 24 / 32 / 48+（展示數字）。比例約 1.2–1.33。
- 內文行高 1.5–1.7；標題 1.2–1.35。中文內文不小於 14px，主要內文 16px。
- 字重 3 種：400 / 600 / 700。
- 長字串（檔名、網址、標題）加 `overflow-wrap: anywhere`，避免窄螢幕水平溢出。
- 計時器、大小、表格數字加 `font-variant-numeric: tabular-nums`。
- 行寬控制在 60–80 字元（`max-width: 72ch`）。

## 3. 元件

```css
.btn { min-height: 44px; padding: 0 var(--s-4); border-radius: var(--r-sm);
  font: 600 15px/1 var(--font-ui); border: 1px solid transparent; cursor: pointer;
  display: inline-flex; align-items: center; justify-content: center; gap: var(--s-2); }
.btn-primary { background: var(--brand); color: var(--brand-ink); }
.btn-danger  { background: var(--danger); color: var(--danger-ink); }
.btn-secondary { background: var(--surface); color: var(--text); border-color: var(--input-border); }
.btn-ghost { background: transparent; color: var(--brand); }
.btn:hover:not(:disabled) { filter: brightness(1.06); }
.btn:active:not(:disabled) { transform: translateY(1px); }
.btn:disabled { opacity: .45; cursor: not-allowed; }
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }

.card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--r-lg);
  padding: var(--s-5); box-shadow: var(--shadow); }

/* 分段選擇：用 radio，鍵盤與螢幕閱讀器自然可用 */
.seg { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr; padding: 4px;
  background: var(--surface-2); border-radius: var(--r-md); }
.seg input { position: absolute; opacity: 0; }
.seg label { text-align: center; padding: 8px; border-radius: var(--r-sm); cursor: pointer; }
.seg input:checked + label { background: var(--surface); box-shadow: var(--shadow); font-weight: 600; }
.seg input:focus-visible + label { outline: 2px solid var(--focus); }

/* 狀態膠囊：文字＋色點，不只靠顏色表意 */
.pill { display: inline-flex; gap: 6px; align-items: center; padding: 4px 10px;
  border-radius: 999px; font-size: 13px; background: var(--surface-2); }
.pill::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: currentColor; }
body[data-state="recording"] .pill { color: var(--danger); }
@media (prefers-reduced-motion: no-preference) {
  body[data-state="recording"] .pill::before { animation: pulse 1.2s ease-in-out infinite; }
}
@keyframes pulse { 50% { opacity: .35; } }

/* 數值磁貼 */
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: var(--s-2); }
.tile dt { font-size: 12px; color: var(--muted); } .tile dd { margin: 0; font: 600 18px var(--font-num); font-variant-numeric: tabular-nums; }
```

計量條（音量、進度）：
- 音量以 dB 刻度映射（例如 −60…0 dBFS → 0…1），線性 peak 會讓正常音量看起來幾乎沒動。
- `<meter low high optimum>` 會整條換色；警示門檻設在真正需要注意處（如 −6 dBFS），不要讓正常電平就變琥珀。
- 歷史圖用 canvas：依 `devicePixelRatio` 設 `canvas.width/height`，顏色從 CSS token 讀（`getComputedStyle`），靜音不畫。

空狀態：寫出「現在沒有什麼」＋「下一步做什麼」，例如「尚無保存的錄音 · 按上方按鈕開始」。

錯誤：紅色文字＋原因＋下一步，`role="alert"` 或 `aria-live="polite"`。

## 4. 響應式

- 用 `grid` / `flex` + `minmax(0, 1fr)`、`min-width: 0`，避免長字串撐破。
- 窄於 560px：按鈕直向堆疊、內距由 24 降到 16、展示數字縮小一級。
- 必測 360px 寬無水平捲動：`node scripts/shot.mjs page.html out --widths 360` 會量測 `scrollWidth` 並列出超出的元素。
- 頁面左右至少 16px 留白。

## 5. 動態

150–250ms、`ease-out`；只用於狀態變化與回饋。不要讓整頁元素依序飛入。所有循環動畫包在 `prefers-reduced-motion: no-preference` 內。

## 6. 瀏覽器擴充 popup / 頁面

- Popup 寬度建議 320–400px，高度由內容決定（上限約 600px）；不可依賴視窗寬度的 media query 來排版 popup。
- MV3 CSP：不能載入外部字型、CDN、inline script；所有資源打包在擴充內。字體用系統字型堆疊。
- Popup 一失焦就關閉：長時間工作（錄音、下載）放在 background / offscreen，popup 只顯示狀態並可重新開啟讀回。
- 開啟時自動聚焦最主要按鈕，Enter 即可執行；提供快捷鍵（`commands`）時在 UI 上寫出來。
- 只顯示來源 origin，不顯示含查詢參數的完整 URL（隱私）。

## 7. 常見錯誤

| 症狀 | 原因 | 修正 |
|---|---|---|
| 看起來「擠」「業餘」 | 間距不一致、太小 | 套用間距刻度，區塊間 ≥ 24px |
| 什麼都很重要 | 太多粗體、太多顏色 | 一個主要動作，其他降為次要／幽靈按鈕 |
| 深色模式髒、灰濛 | 直接反相或沿用淺色強調色 | 重新映射 token，降低飽和度 |
| 焦點看不到 | 同一 focus 色兩主題共用 | 各主題設 `--focus`，跑對比檢查 |
| 數字跳動 | 比例字寬 | `tabular-nums` |
| 窄螢幕水平捲動 | 長檔名、固定寬度 | `overflow-wrap:anywhere`、`min-width:0` |
| 停用按鈕看不出停用 | 只改游標 | 降低不透明度＋`cursor:not-allowed` |
