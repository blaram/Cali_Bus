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
            { "data": "senderID" },
            { "data": "receiverID" },
            { "data": "travelID" },
            { "data": "total" },
            { "data": "status" },
            { "data": "id" },
        ],
        columnDefs: [
            {
                targets: [5],  // Columna de estado
                class: 'text-center',
                render: function (data, type, row) {
                    // Usar parcelChoices para obtener el texto del estado
                    const translatedStatus = parcelChoices[data] || data; // If not found, use the original value
                    const statusColors = {
                        'pending': 'btn-warning',
                        'in_transit': 'btn-secondary',
                        'ready_for_pickup': 'btn-primary',
                        'delivered': 'btn-success',
                        'cancelled': 'btn-danger'
                    };
                    // Retornar el botón con la clase de color correcta
                    return `<button type="button" class="btn btn-sm ${statusColors[data]} btn-change-status" data-id="${row.id}" data-status="${data}"> 
                                ${translatedStatus}
                            </button>`;
                }
            },
            {
                targets: [-1],  // Column to actions
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/calibus/parcel/update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/calibus/parcel/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            // Handle the state change event
            $('#data').on('click', '.btn-change-status', function () {
                const parcelId = $(this).data('id');
                const currentStatus = $(this).data('status');

                // Display a modal or confirmation to change the status
                Swal.fire({
                    title: 'Cambiar estado',
                    text: '¿Deseas cambiar el estado de la encomienda?',
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonText: 'Si, cambiar',
                    cancelButtonText: 'Cancelar'
                }).then((result) => {

                    if (result.value) {

                        $.ajax({
                            url: '/calibus/parcel/change_status/',
                            type: 'POST',
                            data: {
                                id: parcelId,
                                status: currentStatus,
                                action: 'change_status',
                                // csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                            },
                            success: function (response) {
                                if (!response.error) {
                                    Swal.fire('Éxito', 'El estado ha sido cambiado.', 'success');

                                    // Update the button class and text
                                    const nextStatus = {
                                        'pending': 'in_transit',
                                        'in_transit': 'ready_for_pickup',
                                        'ready_for_pickup': 'delivered',
                                        'delivered': 'cancelled',
                                        'cancelled': 'pending'
                                    };

                                    const statusColors = {
                                        'pending': 'btn-warning',
                                        'in_transit': 'btn-secondary',
                                        'ready_for_pickup': 'btn-primary',
                                        'delivered': 'btn-success',
                                        'cancelled': 'btn-danger'
                                    };

                                    const newStatus = nextStatus[currentStatus];  // Get the new status
                                    const translatedStatus = parcelChoices[newStatus] || newStatus;
                                    const button = $(`button[data-id="${parcelId}"]`);
                                    console.log("Botón seleccionado:", button);

                                    // Update the button text and class
                                    button
                                        .text(translatedStatus)
                                        .data('status', newStatus)
                                        .removeClass('btn-warning btn-primary btn-success btn-secondary btn-danger btn-info') // Eliminar clases antiguas
                                        .addClass(statusColors[newStatus]);

                                    console.log("Clases del boton despues de actualizar:", button.attr('class'));

                                    // Recharge the DataTable if necessary
                                    $('#data').DataTable().ajax.reload(null, false); // Reload the Datatable
                                } else {
                                    Swal.fire('Error', response.error, 'error');
                                }
                            },
                            error: function () {
                                Swal.fire('Error', 'No se pudo cambiar el estado.', 'error');
                            }
                        });
                    }
                });
            });
        }
    });
});