from get_ip import get_ipv4
from checker import excel_to_list
from checker import add_check_status, match_list
from flask import Flask, request
from flask_cors import CORS
import json
from typing import Final

PORT: Final[int] = 5000

app = Flask(__name__)
CORS(app)
@app.route("/", methods=["POST", "GET"])
def interact():
    if request.method == "POST":
        target_list = match_list(json.loads(list(request.form.keys())[0])["team"])
        bom = json.loads(list(request.form.keys())[0])["BOM"]
        add_check_status(target_list, bom)
        return json.dumps(bom)
    return json.dumps({"connected":True})


if __name__ == "__main__":
    get_ipv4(PORT)
    app.run(ssl_context="adhoc", host="0.0.0.0", port=PORT)