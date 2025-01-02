from datetime import datetime

from pydantic_settings import BaseSettings
import json
from pathlib import Path
from .custom_log import LOG

def load_json_file(file_name: str) -> dict:
    """讀取 configs 資料夾中的 JSON 檔案"""

    # 取得當前檔案的父目錄，並找到 configs 資料夾
    base_dir = Path(__file__).resolve().parent.parent  # 移動到父目錄
    json_path = base_dir / "forms" / file_name
    # 檢查檔案是否存在，並讀取檔案
    if not json_path.exists():
        raise FileNotFoundError(f"找不到檔案: {json_path}")
    try:
        with json_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except:
        raise json.decoder.JSONDecodeError(f"檔案格式錯誤: {json_path}")

    
def json_format_check(form_datas) -> dict:
    """檢查格式"""
    ban_command = [
        "record",
        "info",
        "remove",
        "help",
    ]
    return_dict = {}
    
    if not isinstance(form_datas, dict): return {}
    """如果輸入的值不是字典"""
    
    for key, value in form_datas.items():
        form_command, form_data = key, value
        if form_command in ban_command: continue
        """如果指令不再禁詞內"""
        if not len(form_command): continue
        """如果指令的字數大於0"""
        # 檢查 "name"
        if "name" not in form_data or not isinstance(form_data['name'], str):
            print("Missing or invalid 'name' in 'ey'")
            continue
        # 檢查 'questions'
        if "questions" not in form_data or not isinstance(form_data['questions'], list):
            print("Missing or invalid 'questions' in 'ey'")
            continue
        
        question_list = []
        for question in form_data["questions"]:
            if "question" not in question or not isinstance(question['question'], str): continue
            if "description" not in question or not isinstance(question['description'], str): continue
            if "class_check" not in question or not isinstance(question['class_check'], str): continue
            question_list.append(question)
        if len(question_list):
            return_dict[key] = value
            LOG.System(f"成功載入表單: {key}")
    return return_dict

