# llm-collab-room
A multi-LLM platform where different models discuss a problem to reach a final answer

---

## FastAPI Hello World API

此專案提供一個最小可執行的 FastAPI API，作為後續 multi-LLM chat room 服務的應用程式入口。

### 1. 本機執行

安裝相依套件：
```bash
pip install -r requirements.txt
```

啟動 API：
```bash
uvicorn app.main:app --reload
```

啟動後可用以下端點確認服務狀態：
```text
GET http://localhost:8000/
GET http://localhost:8000/health
```

### 2. 使用 Docker 建立映像檔

```bash
docker build -t llm-collab-room-api .
```

### 3. 使用 Docker 執行 API

```bash
docker run --rm -p 8000:8000 llm-collab-room-api
```

執行後可開啟：
```text
http://localhost:8000/
http://localhost:8000/docs
```

---

## 本機 MongoDB 啟動與操作指南 (Docker)

為了在本機開發並儲存與 LLM 的對話紀錄，我們使用 Docker 來快速啟動本機的 MongoDB 資料庫。

### 1. 啟動 MongoDB 容器
在終端機中執行以下指令來下載並在背景啟動 MongoDB 容器（對外映射 Port 為 `27017`）：
```bash
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

### 2. 常用資料庫控制指令
*   **停止資料庫容器**：
    ```bash
    docker stop mongodb
    ```
*   **重新啟動已存在的容器**：
    ```bash
    docker start mongodb
    ```
*   **查看容器執行狀態**：
    ```bash
    docker ps -a
    ```

---

## Python 測試寫入腳本執行指南

專案中提供了一個簡單的 `insert_message.py` 腳本，用來測試將會話紀錄寫入本機 MongoDB 中。

### 1. 建立並啟用 Python 虛擬環境
在專案根目錄下執行以下指令：
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. 安裝必要的相依套件
在虛擬環境啟用狀態下，安裝 MongoDB 官方的 Python 用戶端套件 `pymongo`：
```bash
pip install pymongo
```

### 3. 執行測試寫入腳本
執行腳本將一筆包含 `sessionId`、`message` 和自動產生的 `timestamp` (UTC) 資料寫入 `llm-collab-db` 資料庫的 `chat_history` 集合中：
```bash
python3 insert_message.py
```
寫入成功後，終端機將印出類似以下訊息（包含寫入的 Document ID）：
```text
Success: 664b4c6e9a8b1c4e7f8e9d0a
```

### 4. 關閉 MongoDB 容器
測試或開發完成後，若不需要繼續使用資料庫，請執行以下指令將 MongoDB 容器停止並關閉，以節省系統資源：
```bash
docker stop mongodb
```

### 5. 停用 Python 虛擬環境
測試完成後，若不需要繼續在虛擬環境中進行開發，請於終端機執行以下指令停用虛擬環境：
```bash
deactivate
```

---

## 程式碼架喚與命名規範 (SOLID)

為了維持程式碼的乾淨、高可讀性，並符合 SOLID 原則，腳本的設計完全排除任何註解，並藉由極具語意的命名與 Python 型別標記 (Type Hinting) 進行自我解釋。

### 1. ChatMessage 類別
此類別專注於封裝對話訊息的資料結構與格式轉換，符合單一職責原則 (SRP)。

*   **屬性**：
    *   `session_id: str`：對話會話的唯一識別碼。
    *   `message_content: str`：對話訊息的文字內容。
    *   `created_at_utc: datetime.datetime`：自動於初始化時產生的 UTC 時間戳記，指明資料的建立時間。
*   **方法**：
    *   `to_document() -> dict`：將物件屬性轉換為 MongoDB 格式的 Document 字典。該字典對應的鍵值分別為 `sessionId`、`message` 以及 `timestamp`（對應 `created_at_utc`）。

### 2. ChatMessageRepository 類別
此類別專注於處理與 MongoDB 資料庫的持久化互動。

*   **建構子參數**：
    *   `mongo_client: MongoClient`：傳入已建立的 MongoDB 客戶端實例。透過外部注入此實例，符合依賴反轉原則 (DIP) 與依賴注入 (DI)，方便未來進行單元測試與 Mock 替換。
    *   `database_name: str`：指定寫入的資料庫名稱，本專案預設為 `llm-collab-db`。
    *   `collection_name: str`：指定寫入的集合名稱，本專案預設為 `chat_history`。
*   **方法**：
    *   `insert_chat_message(chat_message: ChatMessage) -> str`：接收一個 `ChatMessage` 實例，將其序列化為 Document 並寫入指定的 MongoDB 集合。寫入成功後返回該 Document 的唯一 ID 字串 (`inserted_id`)。
