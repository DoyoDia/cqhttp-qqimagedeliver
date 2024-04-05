import os
import json
import shutil
from typing import cast, Any

with open('config.json', 'r') as f:
    global user_config
    user_config = json.load(f)
    user_config = cast(dict[str, Any], user_config)
    
ADB_PATH = user_config["adb_path"]
DEVICE_ID = user_config["device_id"]
ADB_HEAD = user_config["adb_head"]
APPID = "com.tencent.mobileqq" 
ACTIVITY = "com.tencent.mobileqq.activity.SplashActivity"