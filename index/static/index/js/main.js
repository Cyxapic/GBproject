const btnMenu = document.querySelector('.mob-btn');
btnMenu.addEventListener("click", show_menu, false);

function show_menu(){
    const menu = document.querySelector('#main-menu');
    const content = document.querySelector('#main-content');
    if (menu.style.display === 'none' || menu.style.display === ''){
        menu.style.display = 'block';
        content.style.display = 'none';
    } else {
        menu.style.display = 'none';
        content.style.display = 'block';
    }
};
function show_modal(selector) {
    document.querySelector(selector).style.display = "block";
};
function hide_modal(selector){
    document.querySelector(selector).style.display = "none";
};
