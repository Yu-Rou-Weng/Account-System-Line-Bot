
# Final Project Proposal
## Account System Bot
#### Group 1

組員：
唐磊
蔡怡葶
翁愉媃
林琛琛

### 一、介紹

  在智慧型手機普及的時代，記帳需求已成為人們日常生活的一部分，人人都希望能有效的理財，但是忙碌的生活總是讓記帳變得很困難。於是藉由應用程式商店（如：App Store, Google Play 等）提供的各種記帳軟體，人們得以輕鬆地管理財務，享受到趣味互動和跨裝置存取等進階功能。
由於 LINE 為臺灣廣受歡迎的通訊軟體，我們將記帳服務整合到 LINE Bot 中。透過這樣的方式，使用者不僅能夠省去安裝和熟悉新應用程式的麻煩，還能直接在慣用的 LINE 平台上進行記帳，提升了使用的便利性。
而由於大型語言模型的盛行，我們將大型語言模型整合進我們的記帳服務系統中，將記帳過程從繁複的步驟和指令轉變為口語的描述，使得記帳變得更加輕鬆和直觀，大幅降低使用的門檻，讓任何人都能輕鬆地使用這項服務。
本專案旨在結合 LINE Bot 與大型語言模型，以打造一個使用者友善的記帳服務，讓人們能夠以最輕鬆的方式管理自己的財務，實現財務自由的目標。


### 二、實作計畫
這份專案的主要目的是，採用BDD開發和測試框架，開發一個具有記帳功能的LineBot機器人，用戶提供了一個全面的記帳和財務管理工具，集成了現代的技術和AI元素，使得記帳和財務分析更加智能化和便捷。整個系統將使用Python語言編寫，並以Robot Framework作為開發和測試工具。以下是專案的具體實作計劃和API功能概述：
* LineBot機器人開發：利用BDD框架，確保開發過程符合預期行為。
* API server (Flask)：
    * Server 1：作為LineBot Webhook Endpoint，負責接收和回覆用戶透過Line發送的訊息。這個伺服器會維護一個有限狀態機，用於驗證訊息的正確性並將有效請求轉發給第二台伺服器。
    * Server 2：作為邏輯處理中心，處理來自Server 1的請求，進行資料庫操作或調用外部API（如LLM）來完成業務邏輯。
* 資料庫：選用PostgreSQL/sqlite3來儲存記帳資料。
* 語音轉文字：使用Whisper實現語音輸入功能。
* LLM：選用Claude3生成式AI平台，用於提供預算建議等進階功能。

### (1) 系統架構規劃

![Imgur Image](https://i.imgur.com/ZsYBiE4.png)
                  

### (2) 基於系統架構規劃之API流程設計構思
![Imgur Image](https://i.imgur.com/ccuWBre.png)


### (3) TDD 實作概念:
以 TDD 進行開發時，需為每個應有的功能撰寫相應的測試，並且在寫完程式後確認能否通過測試。若該測試能通過，則繼續下一個功能的開發與測試；如果測試失敗，則需要對原本的程式進行修正，直到能通過測試。當所有的功能都開發完成，代表同時也通過了所有的測試，此即 TDD 開發的概念。




### (4) API功能:




|  | API route | 功能敘述 |備註 |
| -------- | -------- | -------- | --------|
| 1    | POST /Transaction    | 紀錄一筆金額: 紀錄今日支出+今日收入     | 1.使用者: 紀錄 [食/衣/住/行] $800<br />2.Linebot: 紀錄一筆資料
| 2    | GET /Transaction   | 查詢一筆金額: 查詢本日支出+本日收入   |1.使用者: 查詢今日收支<br /> 2.Linebot: 給一個 Line Bot Flex Message 讓使用者可以選 [食/衣/住/行]|
| 3    | GET /Balance/Day    | 查詢當日的餘額    |1.使用者:  查詢20xx年x月餘額<br /> 2.Linebot: <br />20xx年x月<br />支出為:x元<br />收入為:x元|
| 4    | GET /Balance/Month    | 查詢月結餘    |     |
| 5    |      | 串接 Google 試算表 API 計算收支、結餘    |     |
| 6    |     | (Optional) 提供當月的支出和收入報告圓餅圖     |1.當月收支比例<br />2.依照食衣住行查看收支比|
| 7    |     | (Optional)結合LLM，根據過去的收支狀況，提供使用者未來預算建議     |1.Prompt Template: 收支比<br />2.生成式AI API回覆: 建議的未來預算|






### 三、分工


| 姓名 | 工作
| -------- | -------- | 
| 唐磊  | FSM(開發+Test)、Unit Testing、python-afl-fuzz|
| 蔡怡葶  | Line Bot 開發、Atheris-fuzz     |
| 翁愉媃  |Line Bot 開發、Unit Testing、K6 Testing、CI/Pylint|
| 林琛琛 | Line Bot 開發、Performance testing、Bandit|

### 四、時程

* Week1 4/22 設計User Story、Finite State Machine設計
* Week2 4/29 建立Line Bot
* Week3 5/6  記帳API Server實作+測試
* Week4 5/13 DB串接+測試
* Week5 5/20 Optional功能加入(LLM)+測試
* Week6 5/27 Buffer Week
* Week7 6/3  PPT完稿、準備Presentation
* Week8 6/13 上台報告





