function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
};
let orders = localStorage.getItem('book');
try {
    let ids = orders.split('///');
    const list = document.getElementById('orderlist');
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/event/getorder');
    xhr.setRequestHeader("content-type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.onload = function() {
        let res = JSON.parse(this.response);
        let totprice = 0;
        for (var i = 0; i < res.length; i++) {
            let node = document.createElement('tr');
            bkid = res[i].bookid;
            bkname = res[i].name;
            bkauthor = res[i].author;
            price = res[i].price;
            totprice += Number(price);
            const template = `<td style='display:none' class='bkid'>${bkid}</td><td>${bkname}</td><td>${bkauthor}</td><td class='price'>${price}</td><td class="text-danger delete"><button>Delete</button></td>`
            node.innerHTML = template;
            list.appendChild(node);
        }
        document.getElementById('totprice').innerText = 'Rs:' + totprice + '(expected)';
        let delet = Array.from(document.querySelectorAll('.delete'));
        delet.forEach(elem => {
            elem.addEventListener('click', function() {
                let par = elem.parentNode;
                list.removeChild(par);
                calcprice();
            })
        })
    }
    params = JSON.stringify({ 'books': ids });
    xhr.send(params);
} catch {
    console.log('No orders');
}

function calcprice() {
    let prices = Array.from(document.querySelectorAll('.price'));
    totprice = 0;
    prices.forEach(elem => {
        totprice += Number(elem.innerText);
    })
    document.getElementById('totprice').innerText = 'Rs:' + totprice + '(expected)';

}

let placeorder = document.getElementById('placeorder');
placeorder.addEventListener('click', function() {
    let bid = Array.from(document.querySelectorAll('.bkid'));
    if (bid.length == 0) {
        alert("No books selected");
        return;
    }
    message = "";
    bid.forEach(elem => {
        message += elem.innerText + "///";
    })
    document.getElementById('formorder').value = message;
    localStorage.removeItem('book');
    document.getElementById('form').submit();
})