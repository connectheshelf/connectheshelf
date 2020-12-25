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
let form = $("#return form");

form.submit(function(e) {
    e.preventDefault();
    let xhr = new XMLHttpRequest();
    xhr.open('POST', '/librarian/return/');
    xhr.setRequestHeader("content-type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhr.onload = function() {
        let res = JSON.parse(this.response);
        for (var i = 0; i < res.length; i++) {

            showstatus(res[i].id, res[i].status);
        }
    }

    if ($("#bookreturns").val() == "") {
        window.alert('invalid');
    } else {
        let params = {
            "returnbooks": $("#bookreturns").val()
        }
        params = JSON.stringify(params);
        console.log(params);
        xhr.send(params)
    }
})

function showstatus(id, status) {
    if (status == false) {
        bg = 'bg-danger text-light';
        status = 'Unsucessful';
    } else {
        bg = '';
        status = 'Successful';
    }
    let returntemp = `<li class='row ${bg}'>
                <span class="col-md-4">${id}</span>
                <span class="col-md-4">${status}</span>
            </li>`;
    let rptlist = document.getElementById('reportlist');
    rptlist.innerHTML = rptlist.innerHTML + returntemp;
}