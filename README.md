# EPUB to Audio - 電子書轉有聲書專案

將電子書自動轉換成專業「說書」風格的有聲音檔，透過 AI 潤飾內容，讓閱讀體驗更生動有趣。

## 專案目標

很多時候，電子書的原文內容適合閱讀，但不適合直接轉成語音。這個專案透過 AI 大型語言模型（LLM）將書籍內容改寫成：
- 更口語化的表達
- 適合聆聽的節奏
- 說書人風格的敘述
- 保留核心知識，但更生動有趣

## 工作流程

```
EPUB 電子書
    ↓
自動提取章節文字
    ↓
LLM 改寫成「說書」腳本
    ↓
文字轉語音 (TTS)
    ↓
輸出音檔
```

### 詳細步驟

1. **放入電子書**
   - 將 `.epub` 檔案放入 `input/` 資料夾

2. **自動解析章節**
   - 程式讀取 EPUB 檔案
   - 提取每個章節的文字內容
   - 過濾掉版權頁、空白頁等無用內容

3. **AI 潤飾內容**
   - 使用 LLM（如 GPT-4、Claude）改寫內容
   - 轉換成適合「說書」的風格
   - 保持原意，但更適合聆聽

4. **批次轉語音**
   - 將潤飾後的文字送到 TTS 服務
   - 支援多種 TTS 引擎（OpenAI TTS、Google TTS 等）
   - 自動處理長文本分段

5. **輸出音檔**
   - 生成 MP3 或 WAV 格式
   - 按章節命名，方便管理
   - 儲存到 `output/` 資料夾

## 專案結構

```
epub_to_audio/
├── input/              # 放入 EPUB 電子書的地方
│   └── your_book.epub
├── output/             # 輸出的音檔
│   ├── chapter_01.mp3
│   ├── chapter_02.mp3
│   └── ...
├── scripts/            # Python 程式碼
│   ├── epub_reader.py      # EPUB 解析器
│   ├── llm_processor.py    # LLM 內容潤飾
│   ├── tts_converter.py    # 文字轉語音
│   └── main.py             # 主程式
├── config/             # 設定檔
│   └── config.yaml         # API 金鑰、參數設定
├── venv/               # Python 虛擬環境
├── requirements.txt    # Python 套件清單
└── README.md          # 本說明文件
```

## 快速開始

### 1. 環境設定

```bash
# 複製專案
cd ~/Desktop/epub_to_audio

# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate  # Mac/Linux
# 或
venv\Scripts\activate     # Windows

# 安裝套件
pip install -r requirements.txt
```

### 2. 設定 API 金鑰

建立 `config/config.yaml`：

```yaml
# LLM 設定（選擇其中一個）
llm:
  provider: "openai"  # 或 "anthropic", "local"
  api_key: "your-api-key-here"
  model: "gpt-4"      # 或 "claude-3-5-sonnet-20241022"

# TTS 設定（選擇其中一個）
tts:
  provider: "openai"  # 或 "google", "edge"
  api_key: "your-api-key-here"
  voice: "alloy"      # OpenAI 的語音選項
  language: "zh-TW"   # 繁體中文
```

### 3. 執行程式

```bash
# 放入電子書
cp your_book.epub input/

# 執行主程式（全自動）
python scripts/main.py

# 或分步驟執行
python scripts/epub_reader.py       # 步驟 1-2: 解析電子書
python scripts/llm_processor.py     # 步驟 3: LLM 潤飾
python scripts/tts_converter.py     # 步驟 4-5: 轉語音並輸出
```

## 使用範例

```bash
# 範例：處理「高效原力」這本書
python scripts/main.py --input "input/高效原力.epub" --output "output/高效原力/"
```

輸出結果：
```
output/高效原力/
├── 00_引言.mp3
├── 01_遊戲化思維.mp3
├── 02_自我賦權.mp3
├── 03_掌控關係能量.mp3
└── ...
```

## 進階設定

### 自訂 LLM 提示詞

編輯 `config/prompts.yaml` 來客製化改寫風格：

```yaml
storytelling_prompt: |
  你是一位專業的說書人。請將以下書籍內容改寫成適合聆聽的「說書」風格：
  
  要求：
  1. 使用口語化、生動的表達方式
  2. 適當加入過渡詞，讓聽眾容易跟上節奏
  3. 保留核心知識點，但用更有趣的方式呈現
  4. 長度控制在原文的 80-100%
  
  原文內容：
  {content}
```

### 調整音檔品質

修改 `config/config.yaml`：

```yaml
tts:
  format: "mp3"           # 或 "wav"
  bitrate: "192k"         # 音質（128k, 192k, 320k）
  speed: 1.0              # 播放速度（0.5-2.0）
  add_pause: true         # 章節間加入停頓
  pause_duration: 2.0     # 停頓秒數
```

---

**開發者：roy891030**
