from get_ip import get_ipv4
from checker import add_check_status, match_list
from get_file_date import match_date
from flask import Flask, request
from flask_cors import CORS
import json
import time
from typing import Final

PORT: Final[int] = 5000

app = Flask(__name__)
CORS(app)
@app.route("/", methods=["POST", "GET"])
def interact():
    if request.method == "POST":
        if "BOM" in json.loads(list(request.form.keys())[0]):
            try:
                target_list, prefix_list = match_list(json.loads(list(request.form.keys())[0])["team"])
                # 去掉頭尾可能出現的space
                target_list = [t.strip() for t in target_list]
                bom = json.loads(list(request.form.keys())[0])["BOM"]
                add_check_status(target_list, bom)
                return json.dumps({"bom":bom, "prefix_list":prefix_list})
            except Exception as e:
                print(e)
                return json.dumps({"failed": True})
        elif "team":
            return json.dumps({"time":match_date(json.loads(list(request.form.keys())[0])["team"])})
    return json.dumps({"connected":True})


if __name__ == "__main__":
    get_ipv4(PORT)
    app.run(ssl_context="adhoc", host="0.0.0.0", port=PORT)