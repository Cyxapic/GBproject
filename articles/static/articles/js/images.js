let filesInput = document.getElementById("id_image");
let flits = document.getElementById('flits');
filesInput.addEventListener("change", handleFiles, false);

function handleFiles() {
    let file = this.files[0];
    let fPtah = document.createElement('span');
    fPtah.innerHTML = file.name;
    flits.append(fPtah);
};