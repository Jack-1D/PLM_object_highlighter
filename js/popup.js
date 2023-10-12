const submit_button = document.getElementById("submit_button");
const connect_button = document.getElementById("connect");


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
connected.then(data => { if (data) connect_button.style = "display:none"; });

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

// 主程式
submit_button.addEventListener("click", async (e) => {
    e.preventDefault();
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: analyze,
        args: [ip_address]
    },
        (analyze_result) => {
            console.log(analyze_result);
        });
});

function analyze(ip_address) {
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
            'BOM': BOM
        })
    })
        .then(response => response.json())
        .then(data => {
            return data;
        })
}