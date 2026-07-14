$(document).ready(function () {
    $('#btn').on('click', function () {
        alert('click')
        // 글자변경
        $('#title-text').html('backEND');

        var v = $('#input-text').val();
        $('#title-text').html(v);
    });
})