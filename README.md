# Tinder-Gemini 專案 🚀❤️

想讓您的 Tinder 聊天脫穎而出？這個專案結合了 Tinder API 和 Google 的 Gemini API，幫助您模仿自己的聊天風格，自動回覆！不僅如此，它還使用您的個人資料和常用的台灣語句生成自然、有趣且吸引人的回應，讓每一次對話都充滿個人特色和幽默感 😎。

---

## **功能** 🎯

- 💬 自動獲取您的 Tinder 匹配和消息。
- 🤖 使用 Gemini API 生成自然語言回應。
- 📂 上傳個人資料和上下文文件以增強聊天的準確性。
- 🧑‍💻 模仿您的個性和聊天風格。

---

## **需求** 🛠️

### **環境**

- Python 3.8+
- 建議使用虛擬環境

### **API**

- 🔑 Tinder API Token
- 🔑 Google Gemini API Key

### **依賴**

所需依賴項已列在 `requirements.txt` 文件中：

```plaintext
python-dotenv
requests
google-generativeai
```

---

## **安裝指南** 📝

### **1. 克隆存儲庫**

```bash
git clone https://github.com/alichaw/tinder-gemini.git
cd tinder-gemini
```

### **2. 創建虛擬環境**

```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 `venv\Scripts\activate`
```

### **3. 安裝依賴**

```bash
pip install -r requirements.txt
```

### **4. 配置環境變量**

在項目根目錄中創建 `.env` 文件，內容如下：

```plaintext
GEMINI_API_KEY=your_google_gemini_api_key
TINDER_API_TOKEN=your_tinder_api_token
```

將 `your_google_gemini_api_key` 和 `your_tinder_api_token` 替換為您的實際 API 金鑰。

---

## **使用說明** 📖

### **1. 準備數據**

將您的個人資料和常用語句放置在 `data/` 文件夾中：

- `data/profile.md`：您的個人資料，使用 Markdown 格式。
- `data/taiwanese_phrases.md`：常用台灣語句，使用 Markdown 格式。

### **2. 運行應用程式**

```bash
python main.py
```

### **3. 查看輸出**

- 該腳本將執行以下操作：
  1. 📤 上傳您的數據文件到 Gemini API。
  2. 🔍 獲取您的 Tinder 匹配和消息。
  3. 🤝 使用 Gemini API 生成並發送回應。

- 輸出將包括您的個人資料、匹配名稱和生成的回應。

---

## **項目結構** 🗂️

```plaintext
project/
│
├── main.py
├── data_processing.py
├── tinder_api.py
├── file_upload.py
├── data/                 # 個人資料放置區
│   ├── profile.md        # 建立您的個人資料
│   ├── taiwanese_phrases.md  # 常用台灣語句
├── requirements.txt＝
├── .env
└── README.md
```

---

## **注意事項** ⚠️

### **API 限制**

- 注意 Tinder 和 Gemini 的 API 限制。

### **隱私** 🔒

- 確保 API 金鑰和個人數據未公開在公共存儲庫中。
- 使用單獨的 Tinder 測試賬戶以避免潛在問題。

### **錯誤處理** 🛠️

- 該腳本包含基本的錯誤處理，但在生產環境中可能需要添加更多檢查。

---

## **未來增強** 🚀

- 支持更複雜的上下文對話。
- 集成更多 API 以增強功能。
- 改進錯誤處理和日誌機制。

---

## **參與貢獻** 🤝

歡迎貢獻！請 Fork 此存儲庫並提交您的 Pull Request。
