$(function () {

    var table = $('#tblParcels').DataTable({
        searching: false,  // Desactiva la barra de búsqueda
        lengthChange: false,  // Desactiva el selector de cantidad de registros mostrados
        paging: false,  // Desactiva la paginación
        info: false,  // Desactiva la información de registros mostrados
        // responsive: true, // Hace la tabla responsive
    });

    $('#add-to-table').on('click', function () {
        var description = $('[name="description"]').val();
        var weight = $('[name="weight"]').val();
        var declaredValue = $('[name="declared_value"]').val();
        var shippingCost = $('[name="shipping_cost"]').val();

        // Validar que los campos no estén en blanco
        if (!description || !weight || !declaredValue || !shippingCost) {
            alert('Por favor, complete todos los campos antes de agregar a la tabla.');
            return;
        }

        table.row.add([
            '1',
            description,
            weight,
            declaredValue,
            shippingCost,
            '<button type="button" class="btn btn-danger btn-sm">Eliminar</button>'
        ]).draw(false);

        // Limpiar los campos del formulario
        $('[name="description"]').val('');
        $('[name="weight"]').val('');
        $('[name="declared_value"]').val('');
        $('[name="shipping_cost"]').val('');
    });

    $('#tblParcels tbody').on('click', 'button', function () {
        table.row($(this).parents('tr')).remove().draw();
    });
});
