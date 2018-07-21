CKEDITOR.replace('id_text', {
    toolbar: [{
        name: 'clipboard',
        items: ['Undo', 'Redo']
    }, {
        name: 'styles',
        items: ['Styles', 'Format']
    }, {
        name: 'basicstyles',
        items: ['Bold', 'Italic', 'Strike', '-', 'RemoveFormat']
    }, {
        name: 'paragraph',
        items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote']
    }, {
        name: 'insert',
        items: ['Image', 'EmbedSemantic', 'Table']
    }, {
        name: 'tools',
        items: ['Maximize']
    }, {
        name: 'editing',
        items: ['Scayt']
    }],
});
let filesInput = document.getElementById("id_image");
let filesInput1 = document.querySelector("file-cta");
let flits = document.getElementById('flits');
filesInput.addEventListener("change", handleFiles, false);
function handleFiles() {
    let fa = Array.from(this.files)
    fa.forEach(function(element) {
        let fPtah = document.createElement('ol');
        fPtah.innerHTML = `/media/articles/${element.name}`
        flits.append(fPtah);
    });
}