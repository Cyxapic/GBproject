tinymce.init({
    selector: '#id_text',
    setup: function(editor) {
        editor.on('change', function() {
            editor.save();
        });
    }
});