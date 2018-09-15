let filesInput = document.getElementById("id_image");
let btnSave = document.getElementById('save');
if (filesInput){
    filesInput.addEventListener("change", handleFiles, false);
}
if (btnSave) {
    btnSave.addEventListener("click", catgoryAdd, false);
}

function handleFiles() {
    let flits = document.getElementById('flits');
    let file = this.files[0];
    let fPtah = document.createElement('span');
    fPtah.innerHTML = file.name;
    flits.append(fPtah);
};

function catgoryAdd() {
    let form = document.getElementById('category-add-form');
    let msg = document.getElementById('cat-msg');
    let catSelect = document.getElementById('id_category');
    let url = form.getAttribute('data-url');
    let csrftoken = document.getElementsByName('csrfmiddlewaretoken');
    let headers = new Headers({
        'X-CSRFToken': csrftoken[0].value
    });
    data = {
        "name": form.elements.name.value,
        "description": form.elements.description.value,
    };
    let init = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data),
    };
    fetch(url, init).then(function(response) {
        if (response.status !== 200) {
            console.log('Error. Status Code: ' + response.status);
            return;
        }
        response.json().then(function(data) {
            let result = '';
            let resultStyle = '';
            if (data.error) {
                result = data.error;
                resultStyle = 'message is-danger has-text-centered';
            } else {
                result = 'Категория добавлена!';
                resultStyle = 'message is-primary has-text-centered';
                let pk = data.pk;
                let name = data.name;
                let opt = document.createElement("option");
                opt.value = pk;
                opt.innerHTML = name;
                catSelect.append(opt);
                form.reset();
            }
            let div = document.createElement("div");
            div.className = resultStyle;
            div.innerHTML = result;
            msg.append(div);
        });
    });
}

function like(){
    let url = document.getElementById('id_like').getAttribute('data-url');
    let csrftoken = document.getElementsByName('csrfmiddlewaretoken');
    let headers = new Headers({
        'X-CSRFToken': csrftoken[0].value
    });
    let init = {
        method: 'POST',
        headers: headers,
    };
    fetch(url, init).then(function(response) {
        if (response.status !== 200) {
            console.log('Error. Status Code: ' + response.status);
            return;
        }
        response.json().then(function(resp) {
            if (resp.error) {
                console.log(resp.error);
                return;
            } else {
                let el = document.getElementById('thumb');
                let count = document.getElementById('id_count');
                el.innerHTML = `<i class="fas fa-thumbs-up"></i>`;
                count.innerHTML = `Нравится: ${resp.count}`
            }
        });
    });
}