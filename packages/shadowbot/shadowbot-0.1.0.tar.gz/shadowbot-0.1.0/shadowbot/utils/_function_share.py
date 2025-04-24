from datetime import datetime
import pytz
import tzlocal  
import os
import json
import uuid
import platform

def _client_id():
    if platform.system() == "Windows":
        import winreg
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\ShadowBotAssistant", 0, winreg.KEY_READ)
            app_id, _ = winreg.QueryValueEx(key, "UniqueID")
            winreg.CloseKey(key)
            return app_id
        except FileNotFoundError:
            app_id = str(uuid.uuid4())
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\ShadowBotAssistant")
            winreg.SetValueEx(key, "UniqueID", 0, winreg.REG_SZ, app_id)
            winreg.CloseKey(key)
            return app_id

    else:
        
        config_path = os.path.expanduser("~/.config/ShadowBotAssistant/settings.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    data = json.load(f)
                    if "UniqueID" in data:
                        return data["UniqueID"]
            except (json.JSONDecodeError, IOError):
                pass  

        
        app_id = str(uuid.uuid4())
        with open(config_path, "w") as f:
            json.dump({"UniqueID": app_id}, f)

        return app_id


def _current_time_zone():
    
    local_tz = tzlocal.get_localzone()

    
    utc_now = datetime.now(pytz.utc)
    
    timestamp = utc_now.timestamp()
    
    now = utc_now.astimezone(local_tz)
    
    iso_time = now.isoformat()
    return timestamp, local_tz.key, iso_time


import sys
import traceback

def _get_error_details():
    """获取精准的报错位置和信息"""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    last_traceback = traceback.extract_tb(exc_traceback)[-1]
    filename = last_traceback.filename
    lineno = last_traceback.lineno
    funcname = last_traceback.name
    return filename, lineno, funcname, exc_value


import hmac
import hashlib
def _m_sha256(key, message):
    key = key.encode()
    message = message.encode()
    hmac_hash = hmac.new(key, message, hashlib.sha256).hexdigest()
    
    return hmac_hash