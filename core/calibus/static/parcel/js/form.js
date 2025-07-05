$(function () {
    // Inicializar Select2
    $('.select2').select2({
        theme: 'bootstrap4',
        language: 'es',
        placeholder: 'Seleccione una opción',
        allowClear: true
    });

    // Inicializar datetimepicker
    $('#date_joined').datetimepicker({
        format: 'YYYY-MM-DD',
        date: moment().format('YYYY-MM-DD'),
        locale: 'es',
        minDate: moment().format('YYYY-MM-DD')
    });

    const tableBody = $('#tblParcels tbody');

    // Función para limpiar los campos del formulario
    function clearFields() {
        $('#description').val('');
        $('#quantity').val('');
        $('#weight').val('');
        $('#declared_value').val('');
        $('#shipping_cost').val('');
    }

    // Función para calcular el total de la columna "Costo de envío"
    function calculateTotal() {
        let total = 0;

        // Iterar sobre las filas de la tabla y sumar los valores de la columna "Costo de envío"
        $('#tblParcels tbody tr').each(function () {
            const shippingCost = parseFloat($(this).find('td:eq(4)').text()) || 0; // Columna 4: Costo de envío
            total += shippingCost;
        });

        // Actualizar el total en el DOM
        $('#totalShippingCost').text(total.toFixed(2)); // Mostrar con 2 decimales
    }

    // Agregar un artículo a la tabla
    $('#add-to-table').on('click', function () {
        const description = $('#description').val();
        const quantity = $('#quantity').val();
        const weight = $('#weight').val();
        const declaredValue = $('#declared_value').val();
        const shippingCost = $('#shipping_cost').val();

        if (description && quantity && weight && declaredValue && shippingCost) {
            const newRow = `
                <tr>
                    <td>${quantity}</td>
                    <td>${description}</td>
                    <td>${weight}</td>
                    <td>${declaredValue}</td>
                    <td>${shippingCost}</td>
                    <td>
                        <button type="button" class="btn btn-warning btn-sm edit-item">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button type="button" class="btn btn-danger btn-sm remove-item">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
            tableBody.append(newRow);

            // Limpiar los campos
            clearFields();

            // Recalcular el total
            calculateTotal();
        } else {
            alert('Por favor, complete todos los campos antes de agregar a la tabla.');
        }
    });

    // Eliminar un artículo de la tabla
    tableBody.on('click', '.remove-item', function () {
        $(this).closest('tr').remove();

        // Recalcular el total
        calculateTotal();
    });

    // Editar un artículo de la tabla
    tableBody.on('click', '.edit-item', function () {
        const row = $(this).closest('tr');
        const quantity = row.find('td:eq(0)').text();
        const description = row.find('td:eq(1)').text();
        const weight = row.find('td:eq(2)').text();
        const declaredValue = row.find('td:eq(3)').text();
        const shippingCost = row.find('td:eq(4)').text();

        // Cargar los valores en los campos del formulario
        $('#quantity').val(quantity);
        $('#description').val(description);
        $('#weight').val(weight);
        $('#declared_value').val(declaredValue);
        $('#shipping_cost').val(shippingCost);

        // Eliminar la fila actual
        row.remove();

        // Recalcular el total
        calculateTotal();
    });

    // Manejar el evento submit del formulario
    $('form').on('submit', function (e) {
        e.preventDefault(); // Evitar el envío tradicional del formulario

        const items = [];
        let total = 0;

        // Iterar sobre las filas de la tabla y calcular el total
        $('#tblParcels tbody tr').each(function () {
            const row = $(this);
            const shippingCost = parseFloat(row.find('td:eq(4)').text()) || 0; // Columna 4: Costo de envío
            total += shippingCost; // Sumar el costo de envío total

            items.push({
                quantity: row.find('td:eq(0)').text(),
                description: row.find('td:eq(1)').text(),
                weight: row.find('td:eq(2)').text(),
                declared_value: row.find('td:eq(3)').text(),
                shipping_cost: row.find('td:eq(4)').text(),
            });
        });

        const parcelData = {
            action: $('input[name="action"]').val(),
            senderID: $('[name="senderID"]').val(),
            receiverID: $('[name="receiverID"]').val(),
            travelID: $('[name="travelID"]').val(),
            date_joined: $('#date_joined').val(),
            total: total.toFixed(2),
            items: items,
        };

        parcelData.payment_method = $('#payment_method').val();

        // Imprimir los datos en la consola
        console.log('Datos enviados:', parcelData);

        // Usar submit_with_ajax para enviar los datos
        submit_with_ajax(
            window.location.pathname, // URL actual
            'Notificación', // Título de la confirmación
            '¿Estás seguro de realizar esta acción?', // Mensaje de confirmación
            JSON.stringify(parcelData), // Datos a enviar
            function (response) {
                if (response.parcel_id) {
                    window.open('/calibus/parcel/receipt/pdf/' + response.parcel_id + '/', '_blank');
                }
                window.location.href = '/calibus/parcel/list/'; // Redirigir después de éxito
            }
        );
    });
});