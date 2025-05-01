$(function () {
    function updateTotal() {
        let total = 0;
        $('#tblParcels tbody tr').each(function () {
            const shippingCost = parseFloat($(this).find('td:eq(4)').text()) || 0;
            total += shippingCost;
        });
        $('#totalShippingCost').text(total.toFixed(2));
    }

    $('#add-to-table').on('click', function () {
        const description = $('[name="description"]').val();
        const weight = $('[name="weight"]').val();
        const declaredValue = $('[name="declared_value"]').val();
        const shippingCost = $('[name="shipping_cost"]').val();
        const travelText = $('[name="travelID"] option:selected').text(); // Captura el texto del viaje seleccionado
        const senderID = $('[name="senderID"]').val(); // Captura el valor del remitente
        const receiverID = $('[name="receiverID"]').val(); // Captura el valor del consignatario

        // Validar que los campos no estén en blanco o inválidos
        if (!description || !senderID || !receiverID) {
            alert('Por favor, complete todos los campos de texto antes de agregar a la tabla.');
            return;
        }

        // Validar que los campos numéricos sean válidos y mayores a 0
        if (isNaN(weight) || weight <= 0) {
            alert('Por favor, ingrese un peso válido mayor a 0.');
            return;
        }
        if (isNaN(declaredValue) || declaredValue <= 0) {
            alert('Por favor, ingrese un valor declarado válido mayor a 0.');
            return;
        }
        if (isNaN(shippingCost) || shippingCost <= 0) {
            alert('Por favor, ingrese un costo de envío válido mayor a 0.');
            return;
        }

        // Validar que travelText no sea vacío ni igual a "--------"
        if (!travelText || travelText === '---------') {
            alert('Por favor, seleccione una salida válida.');
            return;
        }

        // Crear una nueva fila con íconos para las acciones
        const newRow = `
            <tr>
                <td>1</td>
                <td>${description}</td>
                <td>${weight}</td>
                <td>${declaredValue}</td>
                <td>${shippingCost}</td>
                <td>${travelText}</td>
                <td>
                    <div class="btn-group" role="group">
                        <button type="button" class="btn btn-warning btn-sm edit-row">
                            <i class="fas fa-pencil-alt"></i> <!-- Ícono de lápiz -->
                        </button>
                        <button type="button" class="btn btn-danger btn-sm delete-row">
                            <i class="fas fa-trash"></i> <!-- Ícono de basura -->
                        </button>
                    </div>
                </td>
            </tr>
        `;

        // Agregar la fila al cuerpo de la tabla
        $('#tblParcels tbody').append(newRow);

        // Actualizar el total
        updateTotal();

        // Limpiar los campos del formulario
        $('[name="description"]').val('');
        $('[name="weight"]').val('0.0');
        $('[name="declared_value"]').val('0.0');
        $('[name="shipping_cost"]').val('0.0');
        // $('[name="travelID"]').val(null).trigger('change'); // Limpia el campo de viaje
    });

    // Eliminar una fila al hacer clic en el botón "Eliminar"
    $('#tblParcels tbody').on('click', '.delete-row', function () {
        $(this).closest('tr').remove();
        // Actualizar el total
        updateTotal();
    });

    // Editar una fila al hacer clic en el botón "Editar"
    $('#tblParcels tbody').on('click', '.edit-row', function () {
        const row = $(this).closest('tr');
        const description = row.find('td:eq(1)').text();
        const weight = row.find('td:eq(2)').text();
        const declaredValue = row.find('td:eq(3)').text();
        const shippingCost = row.find('td:eq(4)').text();
        const travelText = row.find('td:eq(5)').text();

        // Cargar los valores en el formulario
        $('[name="description"]').val(description);
        $('[name="weight"]').val(weight);
        $('[name="declared_value"]').val(declaredValue);
        $('[name="shipping_cost"]').val(shippingCost);
        $('[name="travelID"] option').filter(function () {
            return $(this).text() === travelText;
        }).prop('selected', true).trigger('change');

        // Eliminar la fila actual
        row.remove();

        // Actualizar el total
        updateTotal();
    });

    // event submit
    $('form').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());

        // Capturar los datos de la tabla y agregarlos al FormData
        const parcels = [];
        $('#tblParcels tbody tr').each(function () {
            const row = $(this);
            const parcel = {
                senderID: $('[name="senderID"]').val(), // ID del remitente
                receiverID: $('[name="receiverID"]').val(), // ID del consignatario
                travelID: $('[name="travelID"]').val(), // ID del viaje
                date_joined: $('#date_joined').val(), // Fecha
                description: row.find('td:eq(1)').text(), // Descripción
                weight: parseFloat(row.find('td:eq(2)').text()), // Peso
                declared_value: parseFloat(row.find('td:eq(3)').text()), // Valor declarado
                shipping_cost: parseFloat(row.find('td:eq(4)').text()), // Costo de envío
            };
            parcels.push(parcel);
        });

        // Agregar los datos de las encomiendas al FormData como JSON
        parameters.append('parcels', JSON.stringify(parcels));

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