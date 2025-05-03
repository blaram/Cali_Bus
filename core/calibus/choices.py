gender_choices = (
    ('male','Masculino'),
    ('female','Femenino'),
)
parcel_choices = (
    ('pending', 'Pendiente'),  # El envío está registrado pero aún no ha sido despachado.
    ('in_transit', 'En tránsito'),  # El envío está siendo transportado hacia su destino.
    ('ready_for_pickup', 'Listo para recoger'),  # El paquete llegó al destino y está disponible para ser retirado.
    ('delivered', 'Entregado'),  # El paquete fue entregado al destinatario.
    ('cancelled', 'Cancelado'),  # El envío fue anulado antes de llegar a destino.
)