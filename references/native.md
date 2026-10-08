# 原生桌面介面（以 Win32 GDI 為主，概念通用於 WinUI / Qt / GTK / Tauri）

## 原則
- 同樣使用 token：在程式頂端集中定義顏色常數（BG、SURFACE、TEXT、MUTED、LINE、BRAND、DANGER、FOCUS）、字型表與間距，繪製程式只引用常數。
- 所有尺寸以 96 DPI 設計值撰寫，經 `px(n) = n * dpi / 96` 換算；字型在 DPI 改變（`WM_DPICHANGED`）時重建。Per-Monitor V2 感知。
- 版面由一個純函式 `layout(width) -> 各區塊矩形` 產生，可單元測試「不重疊、不超出寬度」。
- 能用真正控制項（按鈕、下拉、清單）就用，保留鍵盤 Tab 與螢幕閱讀器；外觀再以 owner-draw 美化。

## GDI 繪圖要點
- 圓角卡片／按鈕：`RoundRect`（第 5、6 參數是圓角**直徑**，8px 圓角傳 `px(16)`）。先用父表面色填滿矩形，避免四角露出舊底色。
- 每個 `CreateSolidBrush` / `CreatePen` / `CreateFontW` 都要 `DeleteObject`；`SelectObject` 後還原舊物件。洩漏會在長時間執行後讓視窗變黑或當掉。
- 文字：`SetBkMode(TRANSPARENT)`、`DrawTextW` 加 `DT_END_ELLIPSIS`（單行）或 `DT_WORDBREAK`（多行），中文字型用 "Microsoft JhengHei UI"，數字用 "Segoe UI"。
- 雙緩衝：在記憶體 DC 繪製後一次 `BitBlt`，避免閃爍（尤其是計量條每 100ms 重繪）。
- 圓點指示（錄音中）用 `Ellipse`，不要用「●」字元（字型差異會偏移）。
- GDI 沒有真正的透明模糊；不要用假的半透明貼圖冒充玻璃材質，以不透明表面表達層級。

## Owner-draw 按鈕狀態
`DRAWITEMSTRUCT.itemState`：`ODS_SELECTED`（按下，底色加深）、`ODS_DISABLED`（淡底＋淡字）、`ODS_FOCUS`（2px 焦點外框，對比 3:1）。樣式分 primary / danger / secondary / ghost，依功能指定，不依位置。

## 計量與即時資料
- 由 worker 執行緒傳真實數值（peak、位元組、經過時間），UI 計時器只負責重繪。
- 歷史圖每收到一筆真實量測推入一格，不要依 UI 計時器重複取樣同一值。
- dB 刻度：`level = (clamp(20*log10(peak), -60, 0) + 60) / 60`；−6 dBFS 以上警示色、0 dBFS 削波色。

## 驗收
- 提供截圖模式（例如 `--gui-smoke out.bmp <dpi> <w> <h> <fixture>`），以 `PrintWindow`/`WM_PRINT` 只渲染自己的視窗，並輸出控制項邊界稽核（是否超出、重疊、標籤被截）。
- 至少檢查：96 與 144 DPI、寬版與窄版、閒置／執行中／錯誤／空狀態、捲到底部。
- 預覽狀態若用合成值，畫面上要標示「預覽」。
