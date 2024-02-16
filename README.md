# PLM_object_highlighter
(實習專案)PLM crawler

## 環境設置
``` bash
https://github.com/Jack-1D/PLM_object_highlighter.git
cd PLM_object_highlighter
python -m venv venv
venv/Scripts/activate
python -m pip install -r requirements.txt
``` 

## 執行(分成兩個process跑)
``` bash
python app.py
# or
# flask run --host=0.0.0.0 --cert=adhoc
# 刪除__pycache__、上傳ip
# python alive_process.py
# 目前改上傳到google drive
python upload.py
```
