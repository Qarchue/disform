# [disform]([https://www.github.com/Qarchue/disform](https://github.com/Qarchue/disform))

<p align="center">
    <a href="https://github.com/Qarchue/disform"><img src="https://img.shields.io/github/repo-size/Qarchue/disform"></a>
    <a href="https://github.com/Qarchue/disform"><img src="https://img.shields.io/github/languages/top/Qarchue/disform"></a>
    <a href="https://github.com/Qarchue/disform/stargazers"><img src="https://img.shields.io/github/stars/Qarchue/disform?style=socia"></a>
    <a href="https://discord.gg/w5CeZh3rNu"><img src="https://img.shields.io/discord/905865794683015208?style=flat-square&logo=Discord&logoColor=white&label=support&color=5865F2"></a>
</p>

> 歡迎將本專案所有或部分程式碼放入你自己的機器人中。

## 簡介

這是一個交談式表單填寫系統的Discord機器人，提供使用者在表單介面上填寫資料並提交至後台，並可以查詢或刪除已填寫的表單資料。

表單資料使用Google Sheet進行儲存，提供管理人員方便整理與歸納。



---





## 使用方式
私訊機器人特定命令來使用，以命令前綴加上命令來完成操作
以下示範假設命令前綴為 `-` :

`-(表單命令)`: 填寫表單，表單提交後會顯示表單 ID

`-record`: 查詢已提交的所有表單，可以透過下方的按鈕進行頁面及分類切換

`-reomve (表單 ID)`: 刪除已提交的表單

`-info (表單 ID)`: 查詢已提交的表單資料

**在填寫表單時，您可以透過以下命令來進行操作:**  

`-done`: 提交表單(前提是表單已經全部填完)

`-back`: 回到上一個問題重新填寫

`-(問題編號)`: 跳到指定問題填寫

##### *這些命令指示也會在所有題目填完之後跑出來

---





## 展示

[form_1]: https://raw.githubusercontent.com/Qarchue/images/master/disform/form_1.png
[form_2]: https://raw.githubusercontent.com/Qarchue/images/master/disform/form_2.png
[form_3]: https://raw.githubusercontent.com/Qarchue/images/master/disform/form_3.png
[form_4]: https://raw.githubusercontent.com/Qarchue/images/master/disform/form_4.png
[form_5]: https://raw.githubusercontent.com/Qarchue/images/master/disform/form_5.png
[form_6]: https://raw.githubusercontent.com/Qarchue/images/master/disform/form_6.png
[form_7]: https://raw.githubusercontent.com/Qarchue/images/master/disform/form_7.png


![圖片1][form_1] 
![圖片2][form_2]

  
![圖片3][form_3] 
![圖片4][form_4] 
![圖片5][form_5]

  
![圖片6][form_6]

  
![圖片7][form_7]

---





## 使用教學

此使用教學部分照搬原神小幫手的教學

### 架設 discord 機器人

需要在此步驟創建機器人並取得 Bot token

<details><summary>>>> 點此查看完整內容 <<<</summary>

1. 到 [Discord Developer](https://discord.com/developers/applications "Discord Developer") 登入 Discord 帳號

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_1.png)

2. 點選「New Application」建立應用，輸入想要的名稱後按「Create」

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_2.png)

3. 在 Bot 頁面，按「Reset Token」來取得機器人的 Token

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_3.png)

4. 第3步驟做完之後在下面將「Presence Intent」「Server Members Intent」「Message Content Intent」的開關打開

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_4.png)

5. 在 General Information，取得機器人的 Application ID

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_8.png)

5. 在 OAuth2/URL Generator，分別勾選「bot」「applications.commands」「Send Messages」

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_5.png)

6. 開啟最底下產生的 URL 將機器人邀請至自己的伺服器

![](https://raw.githubusercontent.com/Qarchue/images/master/discord_bot/discord_6.png)

</details>


### 取得 google sheets API

<details><summary>>>> 點此查看完整內容 <<<</summary>

1. 可以參考 https://sites.google.com/jes.mlc.edu.tw/ljj/linebot%E5%AF%A6%E5%81%9A/%E7%94%B3%E8%AB%8Bgoogle-sheet-api 來取得 google sheets API 的金鑰與帳戶憑證檔案

</details>

### 電腦端

1. 下載最新版本的 [Python](https://www.python.org/downloads/)。

2. 從 GitHub 下載此程式檔並解壓縮成資料夾。

3. 在程式資料夾內開啟命令提示字元並安裝依賴 `python3 -m pip install -r requirements.txt` 。

4. 將剛剛在 google sheets 取得的帳戶憑證檔案貼在專案目錄下。

5. 以文字編輯器開啟 `utility` 目錄下的 `config.py` 並依照程式中的註解編輯參數||抱歉我還沒研究docker怎麼用，但具體使用方式應該跟原神小幫手的用法一樣||

6. 運行 `start.bat` 就能開始使用了。

---





## 自訂表單

以文字編輯器開啟 `forms` 資料夾下的 `forms.json` 檔案進行新增或編輯。

預設有一個表單作為範例:
```json
{
    "t": {
        "name": "test_form",
        "questions": [
            {
                "question": "question1",
                "description": "``description1``",
                "class_check": "text"
            }
        ]
    }
}
```
`t` 表單命令，填寫表單需要使用命令前綴加上命令以填寫，預設前綴為 `-` 所以要填寫該表單就要使用 `-t` 命令。   
`name` 表單名稱，會當使用者提交表單後會以該名稱在 google sheets 上創建一個工作區來存放資料。   
`questions` 問題列表(串列)，可以依自己需求新增多個問題，串列內記錄著每個問題的資料。   
`question` 問題名稱，為 `embed` 的大標題。   
`description` 問題描述，為 `embed` 的副標題。   
`class_check` 需要輸入的資料類型，當輸入問題的回答後會偵測類型是否正確。   
 > 目前存在3個類型:   
- `text`: 文字  
- `position`: 座標，原本用於 minecraft 伺服器申請  
- `image`: 圖片

你可以依照個人需求進行修改:

```json
{
    "ey": {
        "name": "經濟產出申請",
        "questions": [
            {
                "question": "建築物名稱",
                "description": "``建築物名稱``",
                "class_check": "text"
            },
            {
                "question": "建築位置（正門或主要區域）",
                "description": "座標格式: ``x y z``",
                "class_check": "position"
            },
            {
                "question": "範圍",
                "description": "從線上地圖截圖，用編輯軟體標註範圍，然後將圖片貼至此處送出",
                "class_check": "image"
            }
        ]
    },
    "rs": {
        "name": "紅石連閃器申請",
        "questions": [
            {
                "question": "座標",
                "description": "``連閃器座標``",
                "class_check": "position"
            },
            {
                "question": "作用",
                "description": "``簡單描述連閃器作用``",
                "class_check": "text"
            }
        ]
    }
}
```


---





## 設定

以文字編輯器開啟 `utility` 目錄下的 `config.py` 並編輯物件裡的參數  
刪掉註解的話應該長這樣：
```python
#...以上省略
class Config(BaseSettings):
    """機器人的配置"""

    main_server_id: int = 0
    application_id: int = 0
    bot_token: str = ""

    sheets_key: str = ""
    account_file: str = ""

    custom_command_prefix: str = "-"
    
    questionnaire_icon_url: str = ""
    #以下省略...
```
`main_server_id`: 伺服器 ID，在discord內取得   
`application_id`: 機器人 Application ID，從 Discord Developer 網頁上取得   
`bot_token`: 機器人 Token，從 Discord Developer 網頁取得   
`sheets_key`: Google Sheets 的 Key   
`account_file`: Google Sheets 的帳戶憑證檔案   
`custom_command_prefix`: 自訂命令前綴   
`questionnaire_icon_url`: embed最底下的小icon，可以不填   

### 編輯完設定檔後記得儲存

---





## 專案資料夾結構

```
disform/
    ├── cogs/
    │   ├── admin/            = 管理員命令
    │   ├── bot_event/        = discord 事件管理
    │   └── form_cog/         = 表單操作 cog
    │       ├── ui/               = 各種關於 embed 的操作
    │       │   ├── info.py           = 處理 info 命令
    │       │   ├── questionnaire.py  = 表單系統函式庫
    │       │   ├── records.py        = 處理 record 命令
    │       │   └── remove.py         = 處理 remove 命令
    │       ├── cog.py            = 主 cog ，用於處理命令與創建表單
    │       ├── dataclass.py      = 自訂資料型態，與資料型態偵測
    │       └── embed_message.py  = 標準 embed 函式庫
    ├── forms/            = 表單資料 json 檔案
    ├── google_sheets/    = google sheets API 操作
    ├── utility/          = 一些本專案用到的設定、公用函式、Log、檔案操作...等程式碼
    ├── main.py           = 主程式
    ├── requirements.txt  = pip 依賴
    └── start.bat         = 執行檔
```

---





## 貢獻

程式架構修改自**原神小幫手**  
https://github.com/KT-Yeh/Genshin-Discord-Bot


record 命令的 embed ui 架構參考 **discord-pretty-help**  
https://github.com/CasuallyCalm/discord-pretty-help


意見提供: SSK新世界伺服器


程式撰寫: Qarchue


---





## 授權

此專案採用 MIT 授權，詳情請參閱 LICENSE 檔案。

