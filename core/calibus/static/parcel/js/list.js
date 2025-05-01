$(function () {

    $('.select2').select2({
        theme: 'bootstrap4',
        language: 'es',
        placeholder: 'Seleccione una opción',
        allowClear: true
    });

    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format('YYYY-MM-DD'),
        locale: 'es',
        //maxDate: moment().format('YYYY-MM-DD'),
        minDate: moment().format('YYYY-MM-DD'),
    });
});