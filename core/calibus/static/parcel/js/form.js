$(function () {
    var table = $('#tblParcels').DataTable({
        searching: false,
        lengthChange: false,
        paging: false,
        info: false,
        responsive: true,
    });

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

        console.log({ description, weight, declaredValue, shippingCost, travelText });


        // Validar que los campos no estén en blanco
        if (!description || !weight || !declaredValue || !shippingCost || !travelText) {
            alert('Por favor, complete todos los campos antes de agregar a la tabla.');
            return;
        }

        table.row.add([
            '1',
            description,
            weight,
            declaredValue,
            shippingCost,
            travelText, // Agrega el texto del viaje a la tabla
            '<button type="button" class="btn btn-danger btn-sm">Eliminar</button>'
        ]).draw(false);

        // Actualizar el total
        updateTotal();

        // Limpiar los campos del formulario
        $('[name="description"]').val('');
        $('[name="weight"]').val('');
        $('[name="declared_value"]').val('');
        $('[name="shipping_cost"]').val('');
        $('[name="travelID"]').val(null).trigger('change'); // Limpia el campo de viaje
    });

    $('#tblParcels tbody').on('click', 'button', function () {
        table.row($(this).parents('tr')).remove().draw();
        // Actualizar el total
        updateTotal();
    });
});