$(function () {
    $('.select2').select2({
        theme: 'bootstrap4',
        language: 'es',
    });

    $('#transaction_date').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format("YYYY-MM-DD"),
        locale: 'es',
        minDate: moment().format("YYYY-MM-DD"),
    });

    // $('input[name="commission_percentage"]').TouchSpin({
    //     min: 0,
    //     max: 100,
    //     step: 0.1,
    //     decimals: 2,
    //     boostat: 5,
    //     maxboostedstep: 10,
    //     postfix: '%',
    //     buttons: false,
    // });

    function calculateCommissionAndTotal() {
        let amount = parseFloat($('#id_amount_to_send').val()) || 0;
        let percentage = 10;
        let commission = amount * percentage / 100;
        let total = amount + commission;

        $('#id_commission_percentage').val(percentage);
        $('#id_commission_amount').val(commission.toFixed(2));
        $('#id_total_amount').val(total.toFixed(2));
    }

    $('#id_amount_to_send').on('input', calculateCommissionAndTotal);

    // Calculate on page load (in case there are initial values)
    calculateCommissionAndTotal();

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        // Mostrar el contenido en la consola
        for (var pair of parameters.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }
        submit_with_ajax(
            window.location.pathname,
            'Notificación',
            '¿Estas seguro de realizar la siguiente acción?',
            parameters,
            function () {
                location.href = '/calibus/dashboard/';
            }
        );
    });



});