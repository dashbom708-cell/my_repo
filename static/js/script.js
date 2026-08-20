let alert = document.querySelector(".alert");
const time = 5000
document.addEventListener("DOMContentLoaded", function(){
    if (alert && alert.textContent){
        setTimeout(
            ()=>{
                alert.style.display = "none";
            },
            time)
    }
})

