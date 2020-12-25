let Add=Array.from(document.querySelectorAll('.add'));
Add.forEach(item=>{
    item.addEventListener('click',function(){
        if(localStorage.hasOwnProperty('book'))
        {
            localStorage.setItem('book',localStorage.getItem('book')+'///'+this.getAttribute('data'))
        }
        else{
            localStorage.setItem('book',this.getAttribute('data'))
        }
        alert("Book had been added to cart");
    })
})