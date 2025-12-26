document.addEventListener('DOMContentLoaded', () => {
    initApiTests();
    initTokenTests();
    for(let btn of document.querySelectorAll("[data-token]")) {
        btn.addEventListener('click', selfTestClick);
    }
    const allTests = document.getElementById("all-self-tests");
    if(allTests)allTests.addEventListener('click', allTestsClick)
});

function allTestsClick() {
    for(let btn of document.querySelectorAll("[data-token]")) {
        btn.click();
    }
}

function selfTestClick(e) {
    const token = e.target.closest("[data-token]").getAttribute("data-token");
    const tr = e.target.closest("[data-selftest]");
    const dtl = tr.querySelector("[data-details]");
    const res = tr.querySelector("[data-result]");
    fetch("/product", {
        headers: {  
            "Authorization": token,
        }
    }).then(r => {
        return r.json();
    }).then(j => {
        let cls, expected, param, isPassed = true, cond;

        param = "status-code";
        expected = dtl.getAttribute(`data-${param}`);
        cond = j.status.code == 200;
        cls = `test-res-${cond}`;
        dtl.innerHTML = `<span title="Expected value ${expected}" class="${cls}">Status.code: ${j.status.code}<span><br/>`;
        isPassed &&= cond;

        expected = dtl.getAttribute("data-status-phrase");        
        cond = j.status.phrase == expected;
        cls = `test-res-${cond}`;
        dtl.innerHTML += `<span title="Expected value ${expected}" class="${cls}">Status.phrase: ${j.status.phrase}<span><br/>`;
        isPassed &&= cond;

        expected = dtl.getAttribute("data-auth-code");        
        cond = j.meta.auth.code == expected;
        cls = `test-res-${cond}`;
        dtl.innerHTML += `<span title="Expected value ${expected}" class="${cls}">Auth.code: ${j.meta.auth.code}<span><br/>`;
        isPassed &&= cond;

        expected = dtl.getAttribute("data-auth-data");     
        cond = j.meta.auth.data == expected;
        cls = `test-res-${cond}`;
        dtl.innerHTML += `<span title="Expected value ${expected}" class="${cls}">Auth.data: ${j.meta.auth.data}<span><br/>`;
        isPassed &&= cond;

        expected = dtl.getAttribute("data-auth-status");     
        cond = j.meta.auth.status.toString() == expected;
        cls = `test-res-${cond}`;
        dtl.innerHTML += `<span title="Expected value ${expected}" class="${cls}">Auth.status: ${j.meta.auth.status}<span><br/>`;
        isPassed &&= cond;

        res.innerHTML = `<span class="test-res-${isPassed}">${isPassed ? "OK" : "Fail"}<span>`;
    });
    
}

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
    for(let btn of document.querySelectorAll('[data-test]')) {
        btn.addEventListener('click', apiTestClick);
    }
}

function apiTestClick(e) {
    let btn = e.target.closest('[data-test]');
    if(!btn) throw "closest('[data-test]') not found";
    let testAttr = btn.getAttribute('data-test');
    let res = btn.closest("tr").querySelector('.test-result');
    if(!res) throw ".test-result not found";
    // res.innerHTML =  objToHtml(testAttr);
    
    fetch("/user?test=" + testAttr, {
        method: 'TEST',
    }).then(r => r.json()).then(j => {
        res.innerHTML = `<p>token: ${j.data}</p>`;
        fetch("/product", {
             headers: {  
                "Authorization": `Bearer ${j.data}`,
            }
        }).then(r => r.json()).then(j => {
            switch(testAttr) {
                case 'nbf': 
                    report = {};
                    let res = typeof j.meta.auth != 'undefined';
                    let key = `<span class="test-res-${res}">у відповіді мають бути метадані з полем 'auth'</span>`;
                    report[key] = res ? "++" : "--";

                    res = typeof j.meta.auth.status != 'undefined' && j.meta.auth.data != 'undefined';
                    key = `<span class="test-res-${res}">у полі 'auth' мають бути два полі: 'status' i 'data'</span>`;
                    report[key] = res ? "++" : "--";
                    // поле 'status' повинно дорівнювати false
                    // поле 'data' повинно містити слово 'nbf'                    
                    break;
                    // TODO додати загальний статус тестування: чи пройдені всі тести

                    /*
                    Д.З. Реалізувати детальний звіт тестування сервісу перевірки токенів (авторизації)
                    у режимі "ехр"
                    - у відповіді мають бути метадані з полем 'auth'
                    - у полі 'auth' мають бути два полі: 'status' i 'data
                    - поле 'status' повинно дорівнювати false (зауважити, що порівння з false може пройти null, 0 тощо)
                    - поле 'data' повинно містити слово 'exp', але не як частина іншого слова (на кшталт expert) 
                    - у полі 'data' повинно розпізаватись число (кількість секунд)
                    */

                default: throw "testAttr not recognized: " + testAttr;
            }
            res.innerHTML += objToHtml(report);
            res.innerHTML += "<hr/>";
            res.innerHTML += objToHtml(j);
        });
    });
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
Д.З. Додати до сторінки перевірки АРІ авторизації
зведений звіт про виконання усіх тестів, що запускались.
! Врахувати, що тести виконуються асинхронно і необхідно
  дочекатись завершення останнього з них
*/