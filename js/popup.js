const submit_button = document.getElementById("submit_button");
const connect_button = document.getElementById("connect");
const exist_text = document.getElementById("exist_text");
const not_exist_text = document.getElementById("not_exist_text");
const exist_itemNum = document.getElementById("exist_itemNum");
const not_exist_itemNum = document.getElementById("not_exist_itemNum");
const team_select = document.getElementById("team");
const title = document.getElementById("title");


var ip_address = "";
var rawFile = new XMLHttpRequest();
rawFile.open("GET", "../Server_Address.txt", false);
rawFile.onreadystatechange = function () {
    if (rawFile.readyState === 4) {
        if (rawFile.status === 200 || rawFile.status == 0) {
            ip_address = rawFile.responseText;
        }
    }
}
rawFile.send(null);

var connected = fetch(ip_address, {
    method: 'GET',
    headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" }
})
    .then(response => response.json())
    .then(data => {
        if (data.connected == true) return true;
    })
    .catch(() => { return false })
connected.then(data => {
    if (data) {
        connect_button.style = "display:none";
        title.style = "padding-left: 130px; text-align: center;color: #FF8000;"
} });

connect_button.addEventListener("click", async (e) => {
    e.preventDefault();
    openURL();
});
function openURL() {
    window.open(ip_address);
    connected = fetch(ip_address, {
        method: 'GET',
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" }
    })
        .then(response => response.json())
        .then(data => {
            if (data.connected == true) return true;
        })
        .catch(() => { return false; })
    connected.then(data => { if (data) connect_button.style = "display:none"; });
}

team_select.value = localStorage.getItem("team_select")

// 主程式
submit_button.addEventListener("click", async (e) => {
    e.preventDefault();
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: analyze,
        args: [ip_address, team_select.value]
    },
        (analyze_result) => {
            console.log(analyze_result);
            var analyze_bom = analyze_result[0].result.bom;
            var prefix = analyze_result[0].result.prefix;
            console.log(analyze_bom);
            console.log(prefix);
            var exist = [];
            var not_exist = [];
            for (var i = 0; i < analyze_bom.length; i++){
                if (analyze_bom[i].status == "exist") {
                    exist.push(analyze_bom[i]["itemNumber"]);
                } else if(analyze_bom[i].itemNumber.substring(0, 2) == prefix) {
                    not_exist.push(analyze_bom[i]['itemNumber']);
                }
            }
            exist_text.innerText = exist.length;
            not_exist_text.innerText = not_exist.length;
            exist_itemNum.innerText = exist.join('\n');
            not_exist_itemNum.innerText = not_exist.join('\n');
            localStorage.setItem("team_select", team_select.value)
        });
});

function analyze(ip_address, team) {
    var BOM = [];
    var Item = document.getElementById("ITEMTABLE_BOM").getElementsByClassName("GMPageOne")[1].getElementsByClassName("GMSection")[0].getElementsByTagName("tbody")[0].children;
    for (var i = 0; i < Item.length; i++) {
        if (Item[i].hasAttribute('class')) {
            if (Item[i].attributes['class'].value == "GMDataRow") {
                var row_context = Item[i].innerText;
                row_context = row_context.split("\t");
                var Findnum = row_context[2].trim();
                var itemNumber = row_context[4].trim();
                var SAPRelese = row_context[25].trim();
                var Substitute = row_context[9].trim();
                var Qty = row_context[10].trim();
                BOM.push({ "Findnum": Findnum, "itemNumber": itemNumber, "SAPRelese": SAPRelese, "Substitute": Substitute, "Qty": Qty })
            }
        }
    }
    console.clear();
    console.log(BOM);

    check_result = fetch(ip_address, {
        method: 'POST',
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: JSON.stringify({
            'BOM': BOM,
            'team': team
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            for (var i = 1; i < Item.length; i++) {
                let bom_result = data.bom[i - 1];
                console.log(bom_result);
                if (Item[i].hasAttribute('style')) {
                    if (Item[i].style.display == "none")
                        Item[i].style.display = '';
                }
                if ((Item[i].hasAttribute('style') && Item[i].getElementsByTagName("tr"))) {
                    var Item2 = Item[i];
                    if (bom_result.status == "exist") {
                        var cells = Item2.getElementsByTagName("td");
                        for (var j = 0; j < cells.length; j++) {
                            cells[j].style.backgroundColor = '#28FF28';
                        }
                    } else if (bom_result.status == "not_exist") {
                        var cells = Item2.getElementsByTagName("td");
                        for (var j = 0; j < cells.length; j++) {
                            cells[j].style.backgroundColor = "#FF9797";
                        }
                    }
                }
            }
            return data;
        });
    return check_result;
}