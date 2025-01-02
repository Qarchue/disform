
from pydantic_settings import BaseSettings
from .custom_log import LOG
from .form_load import *

class Config(BaseSettings):
    """機器人的配置"""

    main_server_id: int = 0  # 範例，把0改成: 1283298446570968165
    """伺服器 ID"""                     # (假的伺服器 ID ，示範用)
    application_id: int = 0  # 範例，把0改成: 1246979890831816573  # (假的 Application ID ，示範用)
    """機器人 Application ID，從 Discord Developer 網頁上取得"""
    bot_token: str = ""  # 範例: "MTI4O0NNTU34NDYFvmdMA.G2kW0E.eGub5Gvc-T1Dv129TA532919TA4jgHfuL7-XR5T667KU"
    """機器人 Token，從 Discord Developer 網頁取得"""             # (這當然是假token，外洩token的後果是很嚴重的)


    sheets_key: str = ""  # 範例: "1A2196WJP0ByqesCNfOdd4b51541bWtk87VZePUdQ"
    """Google Sheets 的 Key"""  # (Google Sheets 的 Key 必須是正確的，我沒寫錯誤的報錯:P)
    account_file: str = ""  # 範例: "sheetsapi-42034567-fb934dk8b7d.json"
    """Google Sheets 的帳戶憑證檔案"""    # (需要是正確的檔案名稱包括副檔名)


    custom_command_prefix: str = ""  # 範例: - 
    """自訂指令的前綴"""              # (盡量別太複雜，不能保證不會出現預期外的錯誤)
    

    questionnaire_icon_url: str = ""  # 圖片 url ，可以為空
    """embed問卷最底下的圖片，如果不填，則不顯示"""


    


    slash_cmd_cooldown: float = 5.0
    """使用者重複呼叫部分斜線指令的冷卻時間（單位：秒）"""
    discord_view_long_timeout: float = 1800
    """Discord 長時間互動介面（例：下拉選單） 的逾時時間（單位：秒）"""
    discord_view_short_timeout: float = 60
    """Discord 短時間互動介面（例：確認、選擇按鈕）的逾時時間（單位：秒）"""
    questionnaire_timeout: float = 300
    """Discord 問卷的逾時時間（單位：秒）"""





    form_datas: dict = json_format_check(load_json_file("forms.json"))
    """使用者預設設定檔"""

    def reload_form(self):
        try:
            json_file = load_json_file("forms.json")
            form_datas = json_format_check(json_file)
            self.form_datas = form_datas
            return "重新載入成功"
        
        except FileNotFoundError:
            return f"找不到檔案"
        
        except:
            return f"檔案格式錯誤"        

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"




    


config = Config()  # type: ignore
