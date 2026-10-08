# 風格語彙：Apple 與 GNOME（Adwaita）

使用者說「Apple 風／像 Mac／像 iOS」或「GNOME 風／Adwaita／像 Linux 桌面」時讀本檔。風格是**語彙**（形狀、材質、層次、顏色用法），不是複製商標或系統圖示。不要使用 Apple／GNOME 的 logo、SF Symbols 圖形本身或宣稱是官方元件。

兩者共通：內容優先、控制項退後；顏色克制，強調色只給可互動元素與選取狀態；支援淺色／深色；標準位置放標準動作。

## 目錄
1. Apple（macOS / iOS 26，Liquid Glass）
2. GNOME（libadwaita 1.7+／GNOME 48+）
3. 對照表與選擇
4. 對比度陷阱（已實測）

---

## 1. Apple 風格

**精神**：Apple 的 Liquid Glass 指引強調建立層次（hierarchy）、和諧（harmony）、一致（consistency）。版面與導覽讓最重要的內容成為焦點；控制項與導覽列要克制用色，讓內容透出來；採用標準圖示語意與可預期的動作位置。

**形狀**
- 三種形狀：固定圓角、膠囊（半徑＝高度一半）、**同心圓角**（concentric：內層半徑＝外層半徑 − 內距）。巢狀容器一定用同心，否則角落會「不平行」而顯得廉價。
  CSS：`.card{--r:20px;--pad:12px;border-radius:var(--r);padding:var(--pad)} .card>.inner{border-radius:calc(var(--r) - var(--pad))}`
- 主要按鈕與獨立動作常用膠囊；工具列按鈕群組成一顆膠囊。
- 觸控目標 44pt 以上。

**材質（玻璃層）**：只放在「浮在內容上方」的控制層（工具列、側欄、浮動按鈕、popover），內容層保持不透明。玻璃不要疊玻璃。
```css
.glass {
  background: color-mix(in srgb, var(--surface) 72%, transparent);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid color-mix(in srgb, var(--text) 10%, transparent);
  box-shadow: 0 8px 32px rgb(0 0 0 / .12);
}
@media (prefers-reduced-transparency: reduce) { .glass { background: var(--surface); backdrop-filter: none; } }
@media (prefers-contrast: more) { .glass { border-color: var(--text); } }
```

**字體**：網頁用 `-apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, "PingFang TC", "Microsoft JhengHei UI", sans-serif`（不要打包 SF 字型檔，授權只限 Apple 平台）。iOS 文字樣式：Large Title 34、Title 1 28、Title 2 22、Title 3 20、Headline 17 semibold、**Body 17**、Callout 16、Subheadline 15、Footnote 13、Caption 12 / 11。macOS 內文較小（13）。大標題字距略收（`letter-spacing:-0.02em`）。

**顏色（系統色，sRGB 近似）**

| 名稱 | 淺色 | 深色 |
|---|---|---|
| Blue（強調） | #007AFF | #0A84FF |
| Green | #34C759 | #30D158 |
| Red | #FF3B30 | #FF453A |
| Orange | #FF9500 | #FF9F0A |
| 背景 | #FFFFFF / 群組背景 #F2F2F7 | #000000 / 提升表面 #1C1C1E、#2C2C2E |
| 文字 | #1D1D1F（或 #000） | #FFFFFF |
| 次要文字 | #3C3C43 @ 60% 不透明 ≈ #6E6E73（在 #F5F5F7 上） | #98989D |
| 分隔線 | #3C3C43 @ 29% | #545458 @ 60% |

深色模式以「提升」表面表達層級（#1C1C1E → #2C2C2E → #3A3A3C），不是陰影。

**元件語彙**
- 分組列表（inset grouped）：灰底 #F2F2F7 上的白色圓角卡（10–12px），列高 44、列間 0.5px 分隔線且左側縮排對齊文字。
- 分段控制（segmented）：灰色軌道＋白色滑塊、滑塊有細微陰影。
- 開關（switch）：綠色為開。
- 大數字（計時器）：SF 等寬數字的感覺 → `font-variant-numeric: tabular-nums; font-weight: 300–500`，Apple 偏好輕而大的數字。
- 動畫：彈簧感（`cubic-bezier(.32,.72,0,1)`，250–350ms）。

**避免**：到處用強調藍、按鈕都加框、過深陰影、玻璃疊玻璃、用玻璃當內容背景導致文字對比不足。

---

## 2. GNOME（Adwaita）風格

**精神**：GNOME HIG 追求簡潔、專注、空間有效利用；libadwaita 實作它。一個視窗做一件事，主要動作明確，次要功能收進選單（主選單「☰」放在 header bar 右側）。

**結構**
- **Header bar**：標題置中，左側返回／主要動作，右側選單與視窗按鈕；沒有傳統選單列。
- **Boxed list**：把設定或資訊列組成一張卡片，列之間有分隔線；寬螢幕時以 clamp 限制最大寬度（約 600–800px）置中，窄時去掉兩側留白。
- **Status page**：空狀態用大圖示＋標題＋說明＋一顆 pill 按鈕。
- **Toast**：非阻斷通知，底部浮出。
- 自適應：窄寬度改單欄、側欄收合為可切換的分頁。

**形狀與尺寸**：視窗圓角 15px（`--window-radius`）；按鈕、輸入框約 6px；卡片與 boxed list 約 12px；`pill`（膠囊）用於獨立大動作；`circular` 用於圖示按鈕。toolbar 間距 6px。邊框用前景色 15% 不透明（高對比模式 50%）。

**字體**：GNOME 48 起預設 **Adwaita Sans**（源自 Inter，SIL OFL，可打包），等寬 **Adwaita Mono**（源自 Iosevka）。網頁堆疊：`"Adwaita Sans", Inter, Cantarell, system-ui, "Noto Sans TC", sans-serif`。字級類別：title-1…title-4（標題層級）、heading（預設大小粗體）、body（加大行高）、caption（次要小字）、numeric（等寬數字）、dimmed（55% 不透明的次要文字）。

**顏色（libadwaita 預設 CSS 變數）**

| 變數 | 淺色 | 深色 |
|---|---|---|
| `--accent-bg-color`（按鈕底） | #3584E4 | #3584E4 |
| `--accent-color`（獨立文字／圖示用） | #0461BE | #81D0FF |
| `--destructive-bg-color` | #E01B24 | #C01C28 |
| `--destructive-color` | #C30000 | #FF938C |
| `--success-bg-color` / `--success-color` | #2EC27E / #007C3D | #26A269 / #78E9AB |
| `--warning-bg-color` / `--warning-color` | #E5A50A / #905400 | #CD9309 / #FFC252 |
| `--window-bg-color` | #FAFAFB | #222226 |
| `--view-bg-color`（內容區） | #FFFFFF | #1D1D20 |
| `--headerbar-bg-color` | #FFFFFF | #2E2E32 |
| `--sidebar-bg-color` | #EBEBED | #2E2E32 |
| `--card-bg-color` | #FFFFFF | 白 8% 疊加 |
| `--window-fg-color` | rgb(0 0 6 / 80%) | #FFFFFF |

強調色可由使用者選：blue #3584E4、teal #2190A4、green #3A944A、yellow #C88800、orange #ED5B00、red #E62D42、pink #D56199、purple #9141AC、slate #6F8396。**關鍵設計**：libadwaita 把「當底色用的強調色」與「當文字用的強調色」分開——文字版本在淺色更深、在深色更亮，以保持對比。自己的設計也該如此。

**按鈕類別**：`suggested-action`（強調色底，對話框的肯定鍵）、`destructive-action`（紅色，破壞性）、`flat`（平時像標籤，hover 才有底）、`pill`、`circular`。一個畫面最多一顆 suggested-action。

**避免**：自訂視窗標題列以外的選單列、一畫面多個強調按鈕、硬編碼顏色（應跟隨使用者強調色與深淺模式）、在 boxed list 外再包框。

---

## 3. 對照與選擇

| 面向 | Apple | GNOME |
|---|---|---|
| 主要動作 | 膠囊／填色強調藍，常在右上或底部 | header bar 或 suggested-action，最多一顆 |
| 圓角 | 大、同心、膠囊 | 中等（6 / 12 / 15），pill 用於獨立動作 |
| 層次手段 | 玻璃材質、提升表面 | 平面＋細分隔線、boxed list |
| 字體 | SF（系統） | Adwaita Sans（Inter 系，可打包） |
| 內文大小 | iOS 17 / macOS 13 | 約 11pt（≈15px） |
| 個性 | 精緻、通透、動態彈簧 | 樸素、整齊、功能優先 |

在 Windows 原生（GDI）程式模仿：Apple → 大圓角、膠囊按鈕、淺灰群組背景＋白卡、細分隔線；GNOME → header 區塊、boxed list 卡、6px 按鈕圓角、單一強調按鈕。玻璃模糊在 GDI 無法真實實作，用不透明表面替代，不要用假的半透明貼圖。

## 4. 對比度陷阱（以 scripts/contrast.py 實測）

| 組合 | 比值 | 結論 |
|---|---|---|
| Apple Blue #007AFF 上的白字／白底上的藍字 | 4.02:1 | 小字未達 4.5。網頁小字連結改 #0066CC（5.57:1），或只用於 ≥ 18.66px 粗體／按鈕大字 |
| Apple Red #FF3B30 白字 | 3.55:1 | 只用於大字或圖示；小字錯誤訊息用更深的紅 |
| Apple Green #34C759 在白底 | 2.22:1 | 不可做文字，只做開關／圖示底色 |
| Apple 次要灰 #8E8E93 在白底 | 3.26:1 | 不可做內文；次要文字用 #6E6E73（在 #F5F5F7 上 4.66:1） |
| Apple 深色 Blue #0A84FF 在 #1C1C1E | 4.66:1 | 可用 |
| 白字在 #0071E3 | 4.70:1 | 可做按鈕 |
| GNOME accent #3584E4 白字 | 3.77:1 | 按鈕標籤需粗體大字；獨立小字用 `--accent-color` #0461BE（6.07:1），深色 #81D0FF（9.93:1） |
| GNOME destructive #E01B24 白字 | 4.83:1 | 可用 |

結論：照抄品牌系統色常常不達 WCAG。保留色相、調整明度，並對每個主題跑對比檢查。
