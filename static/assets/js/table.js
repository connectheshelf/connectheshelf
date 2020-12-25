let status = Array.from(document.querySelectorAll('.issue_status'));
status.forEach(element => {
    if (element.innerText == 'missing') {
        element.parentNode.classList.add('bg-danger');
        element.parentNode.classList.add('text-light');
    } else if (element.innerText == 'late') {
        element.parentNode.classList.add('bg-secondary');
        element.parentNode.classList.add('text-light');
    }
});

let table = document.getElementById('print');
$('#default').click(function() {
    status.forEach(element => {
        if (element.innerText != 'missing' && element.innerText != 'late') {
            element.parentNode.parentNode.removeChild(element.parentNode);
            console.log(element.innerText, element.parentNode);
        }
    })
})
$("#printbtn").click(function() {
    let dat = document.querySelector('#print .default-table');
    $('#form_input').val(dat.innerHTML);
    $('#form').submit();
})