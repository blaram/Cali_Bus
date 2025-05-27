$(function () {

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { "data": "id" },
            { "data": "route.origin" },
            { "data": "departure" },
            { "data": "departure_time" },
            { "data": "arrival" },
            { "data": "status" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/calibus/ticket/add/?travel=' + row.id + '" class="btn btn-success btn-xs btn-flat"><i class="fas fa-ticket-alt"></i> Vender Pasaje</a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
});