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
                    // Button to change the status
                    return `<button type="button" class="btn btn-sm btn-info btn-change-status" data-id="${row.id}" data-status="${data}">
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

                console.log("Botón clickeado. ID:", parcelId, "Estado actual:", currentStatus); // Depuración


                // Display a modal or confirmation to change the status
                Swal.fire({
                    title: 'Cambiar estado',
                    text: '¿Deseas cambiar el estado de la encomienda?',
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonText: 'Si, cambiar',
                    cancelButtonText: 'Cancelar'
                }).then((result) => {
                    console.log("Resultado de la confirmación:", result); // Depuración
                    console.log("Resultado de la confirmación:", result.isConfirmed); // Depuración
                    if (result.value) {
                        console.log("Confirmado. Enviando solicitud AJAX..."); // Depuración
                        // Change the request to the backend to change the state
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
                                console.log("Respuesta del servidor:", response);
                                if (!response.error) {
                                    Swal.fire('Éxito', 'El estado ha sido cambiado.', 'success');
                                    $('#data').DataTable().ajax.reload(); // Reload the Datatable
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