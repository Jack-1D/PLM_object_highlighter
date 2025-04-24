const submit_button = document.getElementById("submit_button");
const connect_button = document.getElementById("connect");
const exist_text = document.getElementById("exist_text");
const not_exist_text = document.getElementById("not_exist_text");
const exist_itemNum = document.getElementById("exist_itemNum");
const not_exist_itemNum = document.getElementById("not_exist_itemNum");
const team_select = document.getElementById("team");
const title = document.getElementById("title");
const loading = document.getElementById("loading");
const failed = document.getElementById("failed");


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
    }
});

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

document.getElementById('team').addEventListener('change', (event) => {
    const target = document.getElementById("team");
    const targetValue = target.value;
    check_result = fetch(ip_address, {
        method: 'POST',
        headers: { "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" },
        body: JSON.stringify({
            'team':targetValue 
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const changetxt = document.getElementById("lastUpdate");
            changetxt.textContent = "上次更新時間: " + data["time"];
        });
});

// 主程式
submit_button.addEventListener("click", async (e) => {
    e.preventDefault();
    failed.style = "display: none;";
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    loading.style = "display: block;";
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: analyze,
        args: [ip_address, team_select.value]
    },
        (analyze_result) => {
            // 處理非200
            if (analyze_result[0].result.hasOwnProperty('failed')) {
                failed.style = "display: block;";
                exist_text.innerText = "0";
                not_exist_text.innerText = "0";
                exist_itemNum.innerText = "";
                not_exist_itemNum.innerText = "";
                localStorage.setItem("team_select", team_select.value);
            }
            // 處理200
            else {
                console.log(analyze_result);
                exist_text.innerText = analyze_result[0].result.exist_list.length;
                not_exist_text.innerText = analyze_result[0].result.not_exist_list.length;
                exist_itemNum.innerText = analyze_result[0].result.exist_list.join('\n');
                not_exist_itemNum.innerText = analyze_result[0].result.not_exist_list.join('\n');
                localStorage.setItem("team_select", team_select.value);
            }
            loading.style = "display: none;";
        });
});

function analyze(ip_address, team) {
    var BOM = [];
    // var Item = document.getElementById("treegrid_ITEMTABLE_BOM").getElementById("ITEMTABLE_BOM").getElementsByClassName("GMPageOne")[1].getElementsByClassName("GMSection")[0].getElementsByTagName("tbody")[0].querySelectorAll("tr.GMDataRow");
    if (document.getElementById("ITEMTABLE_BOM") !== null)
        var Item = document.getElementById("ITEMTABLE_BOM").getElementsByClassName("GMBodyMid")[0].querySelectorAll("tr.GMDataRow");
    else
        var Item = document.getElementById("BOM_EXPANDED_DISPLAY_1").getElementsByClassName("GMBodyMid")[0].querySelectorAll("tr.GMDataRow");
    for (var i = 0; i < Item.length; i++) {
        console.log(Item[i].querySelectorAll("td")[4].getElementsByTagName("a").innerText);
    }
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
    console.log(ip_address);
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
            if (data.hasOwnProperty('failed')) {
                for (var i = 0; i < Item.length; i++) {
                    if ((Item[i].hasAttribute('style') && Item[i].getElementsByTagName("tr") && Item[i].getElementsByClassName("GMDataRow"))) {
                        var Item2 = Item[i];
                        var cells = Item2.getElementsByTagName("td");
                        for (var j = 0; j < cells.length; j++) {
                            cells[j].style.backgroundColor = "#FFFFFF";
                        }
                    }
                }
                return data;
            }
            data.exist_list = new Array();
            data.not_exist_list = new Array();
            for (var i = 0; i < Item.length; i++) {
                let bom_result = data.bom[i];
                var prefix_list = data.prefix_list;
                console.log(bom_result);
                // if (Item[i].hasAttribute('style')) {
                //     if (Item[i].style.display == "none")
                //         Item[i].style.display = '';
                // }
                if ((Item[i].hasAttribute('style') && Item[i].getElementsByTagName("tr") && Item[i].getElementsByClassName("GMDataRow"))) {
                    var Item2 = Item[i];
                    if (bom_result.status == "exist") {
                        var cells = Item2.getElementsByTagName("td");
                        for (var j = 0; j < cells.length; j++) {
                            cells[j].style.backgroundColor = '#28FF28';
                        }
                        data.exist_list.push(bom_result.itemNumber);
                    } else if (bom_result.status == "not_exist") {
                        let match_flag = false;
                        for (var index = 0; index < prefix_list.length; index++) {
                            if (bom_result.itemNumber.match(new RegExp(prefix_list[index])) !== null) {
                                match_flag = true;
                                var cells = Item2.getElementsByTagName("td");
                                for (var j = 0; j < cells.length; j++) {
                                    cells[j].style.backgroundColor = "#FF9797";
                                }
                                data.not_exist_list.push(bom_result.itemNumber);
                                break;
                            }
                        }
                        if (!match_flag) {
                            var cells = Item2.getElementsByTagName("td");
                            for (var j = 0; j < cells.length; j++) {
                                cells[j].style.backgroundColor = "#FFFFFF";
                            }
                        }
                    }
                }
            }
            return data;
        });
    return check_result;
}