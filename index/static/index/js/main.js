function show_modal() {
    let modal = document.querySelector('.modal');
    modal.style.display = "block";
}
function hide_modal(obj){
    obj.parentElement.style.display = "none";
}
function msg_modal(selector){
    let modal = document.querySelector(selector);
    modal.style.display = "none";
}