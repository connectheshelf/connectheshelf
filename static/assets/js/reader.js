const shelf = document.getElementById('bookShelf');
// shelf.appendChild(createBook('/static/books/book2.jpg', 'name1', 'author1', 'descriptoin hai idhar bahut saari'))
let bookCart = [];

function fetchbook() {
    let xhr = new XMLHttpRequest();
    xhr.open('post', '/reader/fetchbook');
    xhr.setRequestHeader("content-type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    filters = { "type": $("#type").val(), "category": $("#category").val() }
    xhr.onload = function() {
        let books = JSON.parse(this.response);
        // console.log(books);
        for (book of books) {
            // console.log(book)
            shelf.appendChild(createBook("/static/books/" + book.cover, book.name, book.author, book.description));
        }
    }
    filters = JSON.stringify(filters);
    xhr.send(filters)
    console.log(filters);
}

function createBook(cover, name, author, description) {
    let template = `
    <div class="card mb-4 box-shadow">
        <img class="card-img-top" data-src="holder.js/100px225?theme=thumb&amp;bg=55595c&amp;fg=eceeef&amp;text=Thumbnail" alt="Thumbnail [100%x225]" style="height: 225px; width: 100%; display: block;" src="${cover}" data-holder-rendered="true">
            <div class="card-body">
                <p class="card-text"><b> ${name} by ${author}</b> <br> ${description}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <div class="btn-group">
                        <button type="button" class="btn btn-sm btn-outline-primary" onClick="setModal('${name}')">View</button>
                    </div>
                </div>
            </div>
                </div>`
    let node = document.createElement('div');
    node.classList.add('col-md-4');
    node.innerHTML = template;
    return node;
}

function setModal(name) {
    $('#Add').text("Add to cart");
    $("#bookModal").modal('show');
    $("#stock").text(0);
    let stockxhr = new XMLHttpRequest();
    stockxhr.open('POST', '/reader/getstock/');
    stockxhr.setRequestHeader("content-type", "application/json");
    stockxhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    stockxhr.onload = function() {
        if (this.status == 200) {
            $("#stock").text(JSON.parse(this.response).stock);
            if ($("#stock").text() == '0') {
                alert('Not in stock')
                $("#Add").text('You may request for book');
            }
        }
    }
    $("#name").text(name);
    let stockparams = JSON.stringify({ 'name': name });
    stockxhr.send(stockparams);
}


$("#Add").click(function() {
    let node = document.createElement('tr');
    if ($("#Add").text() == "You may request for book") {
        window.location = 'http://127.0.0.1:8000';
        return;
    }
    if (Number($("#stock").text()) > 0) {
        name = $("#name").text();
        node.setAttribute("Id", name);
        node.innerHTML = `<td>${name}</td><td> <button class="button" onClick="Remove('${name}')">Remove</button></td>`;
        let cart = document.getElementById("cart");
        cart.appendChild(node);
        $("#bookModal").modal('hide');
        bookCart.push(name);
    } else {
        window.alert("Not in Stock");
        $("#bookModal").modal('hide');
    }
})

function Remove(Id) {
    bookCart.splice(bookCart.indexOf(document.getElementById(Id).innerText), 1);
    document.getElementById(Id).remove();
}

$("#order").click(function() {
    let order = new XMLHttpRequest();
    order.open('POST', '/reader/order/');
    order.setRequestHeader("content-type", "application/json");
    order.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    params = { "books": bookCart, "reference": Math.round(10000 + Math.random() * 10000) };
    order.onload = function() {
        res = JSON.parse(this.response);
        if (res['response'] == true) {
            window.alert(`SUCCESSFULL\nReference number is ${res['reference']}`);
        } else {
            window.alert("Not successfull");
        }
    }
    params = JSON.stringify(params);
    order.send(params);

})

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
}

fetchbook();
$('#form-submit').click(function() {
    shelf.innerHTML = '';
    fetchbook();
})