document.addEventListener('DOMContentLoaded', () => {
    initApiTests();
    initTokenTests();
});

function initTokenTests() {
    let btn = document.getElementById("api-user-token-button");
    let res = document.getElementById("api-user-token-result");
    if(btn) btn.addEventListener('click', () => {
        fetch(`/user`, {
            method: 'GET',
            headers: {  
                "Authorization": "Basic YWRtaW46YWRtaW4=",
            }
        })
        .then(r => {
            if(r.status == 200) {
                r.json().then(j => {  
                    console.log(j);                  
                    let [_, jwtPayload, __] = j.data.split('.');
                    res.innerHTML = `<i id="token">${j.data}</i><br/>` + 
                        objToHtml(JSON.parse(atob(jwtPayload)));
                });
            }
            else {
                r.text().then(t => {res.innerHTML = t});
            }            
        });        
    });
}

function initApiTests() {
    const apiNames = ["user", "product"];
    const apiMethods = ["get", "post"];
    for(let apiName of apiNames) {
        for(let apiMethod of apiMethods) {
            let id = `api-${apiName}-${apiMethod}-button`;
            let btn = document.getElementById(id);
            if(btn) btn.addEventListener('click', apiButtonClick);
        }
    }
}

function apiButtonClick(e) {
    const btn = e.target;
    const [_, apiName, apiMethod, __] = btn.id.split('-');
    const resId = `api-${apiName}-${apiMethod}-result`;
    const res = document.getElementById(resId);
    if(res) {
        let tokenElement = document.getElementById("token");
        let auth = tokenElement ? `Bearer ${tokenElement.innerText}` : "Basic YWRtaW46YWRtaW4=";
        let conf = {
            method: apiMethod.toUpperCase(),
            headers: {  
                // YWRtaW06YWRtaW4= admim:admin
                // YWRtaW46YWRtaW0= admin:admim
                // YWRtaW46YWRtaW4= admin:admin
                "Authorization": auth,
                "Custom-Header": "custom-value"
            }
        };
        /*
        Д.З. Реалізувати на тестовій сторінці API User
        щонайменше три кнопки для тестування автентифікації:
            правильний логін - неправильний пароль
            правильний пароль - неправильний логін
            правильне все
        до звіту додати скріншот(и) результатів роботи кнопок    
        */
        const body = btn.getAttribute("data-body");
        if(body) {
            conf.body = body;
            conf.headers["Content-Type"] = "application/json; charset=utf-8";
        }
        fetch(`/${apiName}`, conf)
        .then(r => {
            if(r.status == 200) {
                r.json().then(j => {res.innerHTML = objToHtml(j)});
            }
            else {
                r.text().then(t => {res.innerHTML = t});
            }            
        });        
    }
    else throw resId + " not found";
}

function objToHtml(j, level=0) {
    if(typeof(j)=="string") return j.replace('<', '&lt;');
    let sp = "&emsp;".repeat(level);
    let html = "{<br/>";
    html += Object.keys(j).map(k => {
        let val = j[k] && typeof j[k] == 'object' ? objToHtml(j[k], level + 1) : j[k];
        return `${sp}&emsp;${k}: ${val}`;
    }).join(",<br/>");
    // for(let k in j) {
    //     let val = typeof j[k] == 'object' ? objToHtml(j[k], level + 1) : j[k];
    //     html += `${sp}&emsp;${k}: ${val}<br/>`
    // }
    html += `<br/>${sp}}`;
    return html;
}

/*
Д.З. Створити АРІ контролер для адреси /order (замовлення)
Створити тестову сторінку для нього (посилання на сторінку додати до головної сторінки сайту)
Реалізувати перевірку методів GET, POST, PUT, PATCH, DELETE
Для методів POST, PUT, PATCH додати тіла, для інших - ні
*/