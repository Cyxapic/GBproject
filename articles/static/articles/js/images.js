let filesInput = document.getElementById("id_image");
let filesInput1 = document.querySelector("file-cta");
let flits = document.getElementById('flits');
filesInput.addEventListener("change", handleFiles, false);
function handleFiles() {
    let fa = Array.from(this.files)
    fa.forEach(function(element) {
        let fPtah = document.createElement('span');
        fPtah.innerHTML = element.name;
        flits.append(fPtah);
    });
}