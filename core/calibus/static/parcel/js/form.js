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

        console.log({ description, weight, declaredValue, shippingCost, travelText });

        // Validar que los campos no estén en blanco
        if (!description || !weight || !declaredValue || !shippingCost || !travelText || !senderID || !receiverID) {
            alert('Por favor, complete todos los campos antes de agregar a la tabla.');
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
        $('[name="travelID"]').val(null).trigger('change'); // Limpia el campo de viaje
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
});