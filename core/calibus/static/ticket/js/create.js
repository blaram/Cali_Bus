$(function () {
    // Variables desde el template (deben estar definidas en un <script> antes de este archivo)
    // let totalSeats = {{ total_seats|default:0 }};
    // let occupiedSeats = {{ occupied_seats|default:"[]"|safe }};
    // No uses window.totalSeats ni window.occupiedSeats

    // Si por alguna razón no están definidas, pon valores por defecto
    if (typeof totalSeats === 'undefined') totalSeats = 0;
    if (typeof occupiedSeats === 'undefined') occupiedSeats = [];
    if (typeof occupiedSeats === 'string') {
        try { occupiedSeats = JSON.parse(occupiedSeats); } catch (e) { occupiedSeats = []; }
    }

    if (typeof soldSeats === 'undefined') soldSeats = [];
    if (typeof reservedSeats === 'undefined') reservedSeats = [];
    if (typeof soldSeats === 'string') {
        try { soldSeats = JSON.parse(soldSeats); } catch (e) { soldSeats = []; }
    }
    if (typeof reservedSeats === 'string') {
        try { reservedSeats = JSON.parse(reservedSeats); } catch (e) { reservedSeats = []; }
    }
    // Generar el layout de asientos
    function generateSeatMap(totalSeats, soldSeats, reservedSeats) {
        let html = '<div class="bus-container">';
        html += '<div class="row mb-2">';
        html += '<div class="col-6 d-flex align-items-center justify-content-start"><button type="button" class="btn btn-primary btn-block" disabled><i class="fas fa-user-tie"></i> Conductor</button></div>';
        html += '<div class="col-6 d-flex align-items-center justify-content-end"><button type="button" class="btn btn-info btn-block" disabled><i class="fas fa-user"></i> Copiloto</button></div>';
        html += '</div>';
        let seatsPerRow = 4;
        let rows = Math.ceil(totalSeats / seatsPerRow);
        for (let r = 0; r < rows; r++) {
            html += '<div class="row">';
            // Lado izquierdo (2 asientos)
            html += '<div class="col-6 d-flex">';
            for (let c = 0; c < 2; c++) {
                let seatNum = r * seatsPerRow + c + 1;
                if (seatNum > totalSeats) break;
                let seatClass = '';
                if (soldSeats.includes(seatNum)) {
                    seatClass = 'seat occupied';
                } else if (reservedSeats.includes(seatNum)) {
                    seatClass = 'seat reserved';
                } else {
                    seatClass = 'seat available';
                }
                html += `<div class="flex-fill mb-2 d-flex justify-content-start"><button type="button" class="${seatClass}" data-seat="${seatNum}" ${(soldSeats.includes(seatNum) || reservedSeats.includes(seatNum)) ? 'disabled' : ''}>${seatNum}</button></div>`;
            }
            html += '</div>';
            // Lado derecho (2 asientos)
            html += '<div class="col-6 d-flex">';
            for (let c = 0; c < 2; c++) {
                let seatNum = r * seatsPerRow + 2 + c + 1;
                if (seatNum > totalSeats) break;
                let seatClass = '';
                if (soldSeats.includes(seatNum)) {
                    seatClass = 'seat occupied';
                } else if (reservedSeats.includes(seatNum)) {
                    seatClass = 'seat reserved';
                } else {
                    seatClass = 'seat available';
                }
                html += `<div class="flex-fill mb-2 d-flex justify-content-end"><button type="button" class="${seatClass}" data-seat="${seatNum}" ${(soldSeats.includes(seatNum) || reservedSeats.includes(seatNum)) ? 'disabled' : ''}>${seatNum}</button></div>`;
            }
            html += '</div>';
            html += '</div>';
        }
        html += '</div>';
        $('.seat-layout').html(html);
    }

    generateSeatMap(totalSeats, soldSeats, reservedSeats);

    // Manejar selección de asientos
    let selectedSeats = [];
    $(document).on('click', '.seat.available', function () {
        let seat = parseInt($(this).data('seat'));
        if (!selectedSeats.includes(seat)) {
            selectedSeats.push(seat);
            $(this).addClass('selected');
        } else {
            selectedSeats = selectedSeats.filter(s => s !== seat);
            $(this).removeClass('selected');
        }
        updateSelectedSeats();
        updateButtons();
    });

    function updateSelectedSeats() {
        if (selectedSeats.length) {
            let html = '';
            selectedSeats.forEach(function (seat) {
                html += `<div class="seat-info-item">
                    <span>Asiento ${seat}</span>
                    <select name="passenger_${seat}" class="form-control form-control-sm d-inline-block ml-2 select2-occupant" style="width: 60%;"></select>
                    <span class="remove-seat" data-seat="${seat}">&times;</span>
                </div>`;
            });
            $('#selectedSeatsList').html(html);
            // Inicializar select2 en los nuevos selects
            $('.select2-occupant').select2({
                theme: 'bootstrap4',
                language: 'es',
                placeholder: 'Buscar cliente...',
                allowClear: true,
                ajax: {
                    url: '/calibus/client/autocomplete/', // Ajusta la URL según tu proyecto
                    dataType: 'json',
                    delay: 250,
                    data: function (params) {
                        return {
                            term: params.term
                        };
                    },
                    processResults: function (data) {
                        return data;
                    },
                    cache: true
                },
                minimumInputLength: 1
            });
        } else {
            $('#selectedSeatsList').html('<div class="text-muted text-center p-3"><i class="fas fa-hand-pointer fa-2x"></i><p class="mt-2">Selecciona asientos en el mapa del bus</p></div>');
        }
        $('#seatCount').val(selectedSeats.length);
        // Si tienes precio por asiento, actualiza aquí
        // $('#seatPrice').val(...);
    }

    // Quitar asiento desde el panel derecho
    $(document).on('click', '.remove-seat', function () {
        let seat = parseInt($(this).data('seat'));
        selectedSeats = selectedSeats.filter(s => s !== seat);
        $(`.seat[data-seat='${seat}']`).removeClass('selected');
        updateSelectedSeats();
        updateButtons();
    });

    function addPassengerForm(seatNumber) {
        const formHtml = `
          <div class="passenger-form" id="passengerForm${seatNumber}">
            <h6><i class="fas fa-user"></i> Pasajero para asiento ${seatNumber}</h6>
            <div class="row">
              <div class="col-md-12">
                <div class="form-group">
                  <label>Pasajero:</label>
                  <input type="text" name="passenger_${seatNumber}" class="form-control occupant-autocomplete" placeholder="Buscar cliente..." required autocomplete="off">
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-12">
                <div class="form-group">
                  <label>Precio:</label>
                  <div class="input-group">
                    <input type="number" name="price_${seatNumber}" class="form-control seat-price-input" value="${seatPrice}" step="0.01" min="0" required>
                    <div class="input-group-append">
                      <span class="input-group-text">Bs</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
        $('#passengerForms').append(formHtml);
        $(`#passengerForm${seatNumber}`).slideDown();
        $(`input[name='passenger_${seatNumber}']`).autocomplete({
            minLength: 1,
            source: function (request, response) {
                $.ajax({
                    url: '/client/autocomplete/',
                    dataType: 'json',
                    data: { term: request.term },
                    success: function (data) {
                        response($.map(data.results, function (item) {
                            return {
                                label: item.text,
                                value: item.text,
                                id: item.id
                            };
                        }));
                    }
                });
            },
            select: function (event, ui) {
                // Puedes guardar el id del cliente seleccionado en un input hidden si lo necesitas
                $(this).data('client-id', ui.item.id);
            }
        });
    }

    $('#id_clientID').select2({
        theme: 'bootstrap4',
        language: 'es',
        placeholder: 'Buscar cliente...',
        allowClear: true,
        ajax: {
            url: '/calibus/client/autocomplete/',
            dataType: 'json',
            delay: 250,
            data: function (params) {
                return { term: params.term };
            },
            processResults: function (data) {
                return data;
            },
            cache: true
        },
        minimumInputLength: 1
    });

    // Actualiza el precio total cuando cambian los precios de los asientos
    function updateTotalPrice() {
        let cantidad = parseInt($('#seatCount').val()) || 0;
        let precio = parseFloat($('#seatPrice').val()) || 0;
        let total = cantidad * precio;
        $('#id_total_price').val(total.toFixed(2));
    }

    // Cuando cambie el precio o la cantidad, recalcula el total
    $(document).on('input', '#seatPrice, #seatCount', function () {
        updateTotalPrice();
    });

    // Manejar el evento submit del formulario de ticket
    $('form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const details = [];
        let total = 0;
        const reservationTicketId = $('#reservationTicketId').val();

        // Iterar sobre los asientos seleccionados y armar los detalles
        selectedSeats.forEach(function (seat) {
            const price = parseFloat($('#seatPrice').val()) || 0; // Toma el precio general
            total += price;
            details.push({
                seat_number: seat,
                passengerID: $(`[name='passenger_${seat}']`).val(),
                price: price
            });
        });

        const ticketData = {
            action: 'add',
            ticket: {
                clientID: $('#id_clientID').val(),
                travelID: $('input[name="travelID"]').val(),
                purchase_date: $('#id_purchase_date').val(),
                ticket_type: $('#id_ticket_type').val(),
                total_price: total.toFixed(2)
            },
            details: details,
            payment_method: $('#id_payment_method').val()
        };

        if (reservationTicketId) {
            ticketData.reservation_ticket_id = reservationTicketId;
        }

        // Usar submit_with_ajax para enviar los datos
        submit_with_ajax(
            window.location.pathname, // URL actual
            'Notificación',
            '¿Estás seguro de realizar esta acción?',
            JSON.stringify(ticketData),
            function () {
                window.location.href = '/calibus/ticket/list/';
            }
        );
    });

    function updateButtons() {
        const hasSelection = selectedSeats.length > 0;
        $('#submitBtn, #reserveBtn').prop('disabled', !hasSelection);
    }

    // Llama a updateButtons() también al limpiar la selección
    $('#clearSelection').click(function () {
        selectedSeats = [];
        $('.seat.selected').removeClass('selected');
        $('#selectedSeatsList').html('<div class="text-muted text-center p-3"><i class="fas fa-hand-pointer fa-2x"></i><p class="mt-2">Selecciona asientos en el mapa del bus</p></div>');
        $('#seatCount').val(0);
        updateButtons();
    });
    // Mostrar/ocultar la tabla de reservas y la info de viaje
    $('#showReservationsBtn').on('click', function () {
        $('#reservationsTable').toggle();
        $('#infoTravel').toggle();
    });

    // Mostrar/ocultar la lista de pasajeros
    $('#showPassengerListBtn').on('click', function () {
        $('#passengerListTable').toggle();
    });
    // Cuando se hace click en "Vender" de la tabla, muestra la info de viaje y oculta la tabla
    $(document).on('click', '.load-reservation', function () {
        $('#reservationsTable').hide();
        $('#infoTravel').show();

        // Obtener datos de la reserva
        const clientId = $(this).data('client');
        const seats = $(this).data('seats').toString().split(',').map(Number);
        const ticketId = $(this).data('ticket');
        $('#reservationTicketId').val(ticketId); // Guarda el ticket_id de la reserva

        // Selecciona el cliente en el formulario
        $('#id_clientID').val(clientId).trigger('change');

        // Limpia selección actual y selecciona los asientos reservados
        selectedSeats = [];
        $('.seat.selected').removeClass('selected');
        seats.forEach(function (seat) {
            selectedSeats.push(seat);
            $(`.seat[data-seat='${seat}']`).addClass('selected');
        });
        updateSelectedSeats();
        updateButtons();

        // Rellenar el precio por asiento y el total automáticamente
        const seatPrice = $(this).data('seat-price');
        $('#seatPrice').val(seatPrice);
        // Actualiza el total
        updateTotalPrice();
    });

    // Modal de la lista de pasajeros
    $('#openPassengerListModal').on('click', function () {
        // Obtén el HTML del bloque de la lista de pasajeros
        var content = $('#passengerListTable .card').html();
        $('#modalPassengerListContent').html(content);
        $('#passengerListModal').modal('show');
    });

    // Botón para imprimir directamente
    $('#printModalPassengerList').on('click', function () {
        var printContents = document.getElementById('modalPassengerListContent').innerHTML;
        var win = window.open('', '_blank');
        win.document.write('<html><head><title>Lista de Pasajeros</title>');
        win.document.write('<link rel="stylesheet" href="/static/lib/bootstrap-4.6.2/css/bootstrap.min.css">');
        win.document.write('<style>body{padding:30px;} .btn, .modal-header, .modal-footer{display:none !important;} @media print { body { background: #fff; } }</style>');
        win.document.write('</head><body>');
        win.document.write(printContents);
        win.document.write('</body></html>');
        win.document.close();
        win.focus();
        win.print();
    });

    // Botón para descargar como PDF usando print dialog (el usuario debe elegir "Guardar como PDF")
    $('#downloadPdfPassengerList').on('click', function () {
        var printContents = document.getElementById('modalPassengerListContent').innerHTML;
        var win = window.open('', '_blank');
        win.document.write('<html><head><title>Lista de Pasajeros</title>');
        win.document.write('<link rel="stylesheet" href="/static/lib/bootstrap-4.6.2/css/bootstrap.min.css">');
        win.document.write('<style>body{padding:30px;} .btn, .modal-header, .modal-footer{display:none !important;} @media print { body { background: #fff; } }</style>');
        win.document.write('</head><body>');
        win.document.write(printContents);
        win.document.write('</body></html>');
        win.document.close();
        win.focus();
        setTimeout(function () {
            win.print();
        }, 500); // Espera a que cargue el contenido antes de abrir el diálogo de impresión
    });

    // Función para mostrar/ocultar el método de pago
    $('#id_ticket_type').on('change', function () {
        if ($(this).val() === 'vendido') {
            $('#paymentMethodRow').show();
        } else {
            $('#paymentMethodRow').hide();
            $('#id_payment_method').val('');
        }
    });
});
