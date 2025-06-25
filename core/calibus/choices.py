gender_choices = (
    ("male", "Masculino"),
    ("female", "Femenino"),
)
parcel_choices = (
    (
        "pending",
        "Pendiente",
    ),  # El envío está registrado pero aún no ha sido despachado.
    (
        "in_transit",
        "En tránsito",
    ),  # El envío está siendo transportado hacia su destino.
    (
        "ready_for_pickup",
        "Listo para recoger",
    ),  # El paquete llegó al destino y está disponible para ser retirado.
    ("delivered", "Entregado"),  # El paquete fue entregado al destinatario.
    ("cancelled", "Cancelado"),  # El envío fue anulado antes de llegar a destino.
)
remittance_choices = (
    (
        "pending",
        "Pendiente",
    ),  # La remesa está registrada pero aún no ha sido despachada.
    ("sent", "Enviado"),  # La remesa está siendo transportada hacia su destino.
    ("delivered", "Entregado"),  # La remesa fue entregada al destinatario.
    ("cancelled", "Cancelado"),  # La remesa fue anulada antes de llegar a destino.
)
travel_status_choices = (
    ("active", "Activo"),
    ("inactive", "Inactivo"),
)

ticket_type_choices = (
    ("reservado", "Reservado"),
    ("vendido", "Vendido"),
    ("libre", "Libre"),
)

cashbox_type_choices = (
    ("shift_change", "Cambio de turno"),
    ("cash_closing", "Cierre de caja"),
)

movement_type_choices = (
    ("income", "Ingreso"),
    ("expense", "Egreso"),
)

payment_method_choices = (
    ("qr", "Pago con QR"),
    ("cash", "Pago en efectivo"),
)

cashbox_status_choices = (
    ("open", "Abierto"),
    ("closed", "Cerrado"),
)
