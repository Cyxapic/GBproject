let filesInput = document.getElementById("id_image");
let flits = document.getElementById('flits');
filesInput.addEventListener("change", handleFiles, false);
function handleFiles() {
    let file = this.files[0];
    let fPtah = document.createElement('span');
    fPtah.innerHTML = file.name;
    flits.append(fPtah);
};

let btnSave = document.getElementById('save');
btnSave.addEventListener("click", catgoryAdd, false);
function catgoryAdd(){
    let form = document.getElementById('category-add-form');
    let url = form.getAttribute('data-url');
    headers = {
        ''
    };
    data = {
        "name": form.elements.name.value,
        "description": form.elements.description.value,
    };
    fetch(url,);
}

