function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        var html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + value + '</li>';
        });
        html += '</ul>';
    }
    else {
        html = '<p>' + obj + '</p>';
    }

    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}