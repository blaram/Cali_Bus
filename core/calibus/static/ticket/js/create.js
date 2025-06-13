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
    // Generar el layout de asientos
    function generateSeatMap(totalSeats, occupiedSeats) {
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
                let seatClass = occupiedSeats.includes(seatNum) ? 'seat occupied' : 'seat available';
                html += `<div class="flex-fill mb-2 d-flex justify-content-start"><button type="button" class="${seatClass}" data-seat="${seatNum}" ${occupiedSeats.includes(seatNum) ? 'disabled' : ''}>${seatNum}</button></div>`;
            }
            html += '</div>';
            // Lado derecho (2 asientos)
            html += '<div class="col-6 d-flex">';
            for (let c = 0; c < 2; c++) {
                let seatNum = r * seatsPerRow + 2 + c + 1;
                if (seatNum > totalSeats) break;
                let seatClass = occupiedSeats.includes(seatNum) ? 'seat occupied' : 'seat available';
                html += `<div class="flex-fill mb-2 d-flex justify-content-end"><button type="button" class="${seatClass}" data-seat="${seatNum}" ${occupiedSeats.includes(seatNum) ? 'disabled' : ''}>${seatNum}</button></div>`;
            }
            html += '</div>';
            html += '</div>';
        }
        html += '</div>';
        $('.seat-layout').html(html);
    }

    generateSeatMap(totalSeats, occupiedSeats);

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

});
