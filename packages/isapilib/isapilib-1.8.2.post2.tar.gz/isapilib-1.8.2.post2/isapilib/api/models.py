from django.db import models

from isapilib.core.models import BaseModel


class Art(BaseModel):
    articulo = models.CharField(db_column='Articulo', primary_key=True, max_length=20)
    descripcion1 = models.CharField(db_column='Descripcion1', max_length=100, blank=True, null=True)
    descripcion2 = models.CharField(db_column='Descripcion2', max_length=255, blank=True, null=True)
    grupo = models.CharField(db_column='Grupo', max_length=50, blank=True, null=True)
    categoria = models.CharField(db_column='Categoria', max_length=50, blank=True, null=True)
    impuesto1 = models.FloatField(db_column='Impuesto1')
    impuesto2 = models.FloatField(db_column='Impuesto2', blank=True, null=True)
    impuesto3 = models.FloatField(db_column='Impuesto3', blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=20)
    precio_lista = models.DecimalField(db_column='PrecioLista', max_digits=19, decimal_places=4, blank=True, null=True)
    estatus = models.CharField(db_column='Estatus', max_length=15)
    usuario = models.CharField(db_column='Usuario', max_length=10, blank=True, null=True)
    precio2 = models.DecimalField(db_column='Precio2', max_digits=19, decimal_places=4, blank=True, null=True)
    precio3 = models.DecimalField(db_column='Precio3', max_digits=19, decimal_places=4, blank=True, null=True)
    precio4 = models.DecimalField(db_column='Precio4', max_digits=19, decimal_places=4, blank=True, null=True)
    precio5 = models.DecimalField(db_column='Precio5', max_digits=19, decimal_places=4, blank=True, null=True)
    precio6 = models.DecimalField(db_column='Precio6', max_digits=19, decimal_places=4, blank=True, null=True)
    precio7 = models.DecimalField(db_column='Precio7', max_digits=19, decimal_places=4, blank=True, null=True)
    precio8 = models.DecimalField(db_column='Precio8', max_digits=19, decimal_places=4, blank=True, null=True)
    precio9 = models.DecimalField(db_column='Precio9', max_digits=19, decimal_places=4, blank=True, null=True)
    precio10 = models.DecimalField(db_column='Precio10', max_digits=19, decimal_places=4, blank=True, null=True)
    situacion = models.CharField(db_column='Situacion', max_length=50, blank=True, null=True)
    tipo_compra = models.CharField(db_column='TipoCompra', max_length=20, blank=True, null=True)
    retencion1 = models.FloatField(db_column='Retencion1', blank=True, null=True)
    retencion2 = models.FloatField(db_column='Retencion2', blank=True, null=True)
    retencion3 = models.FloatField(db_column='Retencion3', blank=True, null=True)
    modelo = models.CharField(db_column='Modelo', max_length=4, blank=True, null=True)
    direccion = models.CharField(db_column='Direccion', max_length=100, blank=True, null=True)
    direccion_numero = models.CharField(db_column='DireccionNumero', max_length=20, blank=True, null=True)
    direccion_numero_int = models.CharField(db_column='DireccionNumeroInt', max_length=20, blank=True, null=True)
    observaciones = models.CharField(db_column='Observaciones', max_length=100, blank=True, null=True)
    colonia = models.CharField(db_column='Colonia', max_length=100, blank=True, null=True)
    delegacion = models.CharField(db_column='Delegacion', max_length=100, blank=True, null=True)
    poblacion = models.CharField(db_column='Poblacion', max_length=100, blank=True, null=True)
    estado = models.CharField(db_column='Estado', max_length=30, blank=True, null=True)
    pais = models.CharField(db_column='Pais', max_length=30, blank=True, null=True)
    codigo_postal = models.CharField(db_column='CodigoPostal', max_length=15, blank=True, null=True)
    tipo_impuesto1 = models.CharField(db_column='TipoImpuesto1', max_length=10, blank=True, null=True)
    tipo_impuesto2 = models.CharField(db_column='TipoImpuesto2', max_length=10, blank=True, null=True)
    tipo_impuesto3 = models.CharField(db_column='TipoImpuesto3', max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'Art'
        managed = False


class VentaD(BaseModel):
    id_venta = models.IntegerField(db_column='ID')
    renglon = models.FloatField(db_column='Renglon')
    renglon_sub = models.IntegerField(db_column='RenglonSub')
    renglon_id = models.IntegerField(db_column='RenglonID', blank=True, null=True)
    renglon_tipo = models.CharField(db_column='RenglonTipo', max_length=1, blank=True, null=True)
    cantidad = models.FloatField(db_column='Cantidad', blank=True, null=True)
    almacen = models.CharField(db_column='Almacen', max_length=10, blank=True, null=True)
    articulo = models.CharField(db_column='Articulo', max_length=20)
    precio = models.FloatField(db_column='Precio', blank=True, null=True)
    precio_sugerido = models.FloatField(db_column='PrecioSugerido', blank=True, null=True)
    impuesto1 = models.FloatField(db_column='Impuesto1', blank=True, null=True)
    impuesto2 = models.FloatField(db_column='Impuesto2', blank=True, null=True)
    impuesto3 = models.FloatField(db_column='Impuesto3', blank=True, null=True)
    descripcion_extra = models.CharField(db_column='DescripcionExtra', max_length=100, blank=True, null=True)
    costo = models.DecimalField(db_column='Costo', max_digits=19, decimal_places=4, blank=True, null=True)
    aplica = models.CharField(db_column='Aplica', max_length=20, blank=True, null=True)
    aplica_id = models.CharField(db_column='AplicaID', max_length=20, blank=True, null=True)
    unidad = models.CharField(db_column='Unidad', max_length=50, blank=True, null=True)
    fecha_requerida = models.DateTimeField(db_column='FechaRequerida', blank=True, null=True)
    hora_requerida = models.CharField(db_column='HoraRequerida', max_length=5, blank=True, null=True)
    agente = models.CharField(db_column='Agente', max_length=10, blank=True, null=True)
    departamento = models.IntegerField(db_column='Departamento', blank=True, null=True)
    sucursal = models.IntegerField(db_column='Sucursal')
    sucursal_origen = models.IntegerField(db_column='SucursalOrigen', blank=True, null=True)
    uen = models.IntegerField(db_column='UEN', blank=True, null=True)
    precio_lista = models.DecimalField(db_column='PrecioLista', max_digits=19, decimal_places=4, blank=True, null=True)
    tipo_impuesto1 = models.CharField(db_column='TipoImpuesto1', max_length=10, blank=True, null=True)
    tipo_impuesto2 = models.CharField(db_column='TipoImpuesto2', max_length=10, blank=True, null=True)
    tipo_impuesto3 = models.CharField(db_column='TipoImpuesto3', max_length=10, blank=True, null=True)
    retencion1 = models.FloatField(db_column='Retencion1', blank=True, null=True)
    retencion2 = models.FloatField(db_column='Retencion2', blank=True, null=True)
    retencion3 = models.FloatField(db_column='Retencion3', blank=True, null=True)
    tipo_retencion1 = models.CharField(db_column='TipoRetencion1', max_length=10, blank=True, null=True)
    tipo_retencion2 = models.CharField(db_column='TipoRetencion2', max_length=10, blank=True, null=True)
    tipo_retencion3 = models.CharField(db_column='TipoRetencion3', max_length=10, blank=True, null=True)
    comentarios = models.CharField(db_column='Comentarios', max_length=250, blank=True, null=True)
    servicio_tipo_orden = models.CharField(db_column='ServicioTipoOrden', max_length=20, blank=True, null=True)
    articulo_actual = models.CharField(db_column='ArticuloActual', max_length=20, blank=True, null=True)
    ut = models.FloatField(db_column='UT', blank=True, null=True)
    cc_tiempo_tab = models.FloatField(db_column='CCTiempoTab', blank=True, null=True)
    paquete = models.IntegerField(db_column='Paquete')

    class Meta:
        db_table = 'VentaD'
        managed = False
        unique_together = (('id', 'renglon', 'renglon_sub'),)


class Venta(BaseModel):
    id = models.AutoField(db_column='ID', primary_key=True)
    empresa = models.CharField(db_column='Empresa', max_length=5)
    mov = models.CharField(db_column='Mov', max_length=20)
    mov_id = models.CharField(db_column='MovID', max_length=20, blank=True, null=True)
    fecha_emision = models.DateTimeField(db_column='FechaEmision', blank=True, null=True)
    ultimo_cambio = models.DateTimeField(db_column='UltimoCambio', blank=True, null=True)
    concepto = models.CharField(db_column='Concepto', max_length=50, blank=True, null=True)
    uen = models.IntegerField(db_column='UEN', blank=True, null=True)
    moneda = models.CharField(db_column='Moneda', max_length=10)
    tipo_cambio = models.FloatField(db_column='TipoCambio', blank=True, null=True)
    usuario = models.CharField(db_column='Usuario', max_length=10, blank=True, null=True)
    referencia = models.CharField(db_column='Referencia', max_length=50, blank=True, null=True)
    observaciones = models.CharField(db_column='Observaciones', max_length=100, blank=True, null=True)
    estatus = models.CharField(db_column='Estatus', max_length=15, blank=True, null=True)
    situacion = models.CharField(db_column='Situacion', max_length=50, blank=True, null=True)
    situacion_fecha = models.DateTimeField(db_column='SituacionFecha', blank=True, null=True)
    situacion_usuario = models.CharField(db_column='SituacionUsuario', max_length=10, blank=True, null=True)
    situacion_nota = models.CharField(db_column='SituacionNota', max_length=100, blank=True, null=True)
    cliente = models.CharField(db_column='Cliente', max_length=10)
    almacen = models.CharField(db_column='Almacen', max_length=10)
    agente = models.CharField(db_column='Agente', max_length=10, blank=True, null=True)
    agente_servicio = models.CharField(db_column='AgenteServicio', max_length=10, blank=True, null=True)
    fecha_requerida = models.DateTimeField(db_column='FechaRequerida', blank=True, null=True)
    hora_requerida = models.CharField(db_column='HoraRequerida', max_length=5, blank=True, null=True)
    condicion = models.CharField(db_column='Condicion', max_length=50, blank=True, null=True)
    servicio_tipo = models.CharField(db_column='ServicioTipo', max_length=50, blank=True, null=True)
    servicio_articulo = models.CharField(db_column='ServicioArticulo', max_length=20, blank=True, null=True)
    servicio_serie = models.CharField(db_column='ServicioSerie', max_length=50, blank=True, null=True)
    servicio_contrato = models.CharField(db_column='ServicioContrato', max_length=20, blank=True, null=True)
    servicio_contrato_id = models.CharField(db_column='ServicioContratoID', max_length=20, blank=True, null=True)
    servicio_contrato_tipo = models.CharField(db_column='ServicioContratoTipo', max_length=50, blank=True, null=True)
    servicio_descripcion = models.CharField(db_column='ServicioDescripcion', max_length=100, blank=True, null=True)
    servicio_fecha = models.DateTimeField(db_column='ServicioFecha', blank=True, null=True)
    servicio_flotilla = models.BooleanField(db_column='ServicioFlotilla', blank=True, null=True)
    servicio_rampa = models.BooleanField(db_column='ServicioRampa', blank=True, null=True)
    servicio_identificador = models.CharField(db_column='ServicioIdentificador', max_length=20, blank=True, null=True)
    servicio_placas = models.CharField(db_column='ServicioPlacas', max_length=20, blank=True, null=True)
    servicio_kms = models.IntegerField(db_column='ServicioKms', blank=True, null=True)
    servicio_tipo_orden = models.CharField(db_column='ServicioTipoOrden', max_length=20, blank=True, null=True)
    servicio_tipo_operacion = models.CharField(db_column='ServicioTipoOperacion', max_length=50, blank=True, null=True)
    servicio_siniestro = models.CharField(db_column='ServicioSiniestro', max_length=20, blank=True, null=True)
    servicio_deducible_importe = models.DecimalField(db_column='ServicioDeducibleImporte', max_digits=19,
                                                     decimal_places=4, blank=True, null=True)
    servicio_numero = models.FloatField(db_column='ServicioNumero', blank=True, null=True)
    servicio_numero_economico = models.CharField(db_column='ServicioNumeroEconomico', max_length=20, blank=True,
                                                 null=True)
    servicio_aseguradora = models.CharField(db_column='ServicioAseguradora', max_length=10, blank=True, null=True)
    servicio_puntual = models.BooleanField(db_column='ServicioPuntual', blank=True, null=True)
    servicio_poliza = models.CharField(db_column='ServicioPoliza', max_length=20, blank=True, null=True)
    origen = models.CharField(db_column='Origen', max_length=20, blank=True, null=True)
    origen_id = models.CharField(db_column='OrigenID', max_length=20, blank=True, null=True)
    servicio_modelo = models.CharField(db_column='ServicioModelo', max_length=4, blank=True, null=True)
    sucursal = models.IntegerField(db_column='Sucursal')
    sucursal_destino = models.IntegerField(db_column='SucursalDestino', blank=True, null=True)
    comentarios = models.TextField(db_column='Comentarios', blank=True, null=True)
    fecha_entrega = models.DateTimeField(db_column='FechaEntrega', blank=True, null=True)
    hora_recepcion = models.CharField(db_column='HoraRecepcion', max_length=5, blank=True, null=True)

    class Meta:
        db_table = 'Venta'
        managed = False

    def create_ventad(self, art: Art, i: int) -> VentaD:
        service_detail = VentaD()
        service_detail.id_venta = self.id
        service_detail.renglon_sub = 0
        service_detail.renglon_tipo = 'N'
        service_detail.almacen = self.almacen
        service_detail.uen = self.uen
        service_detail.sucursal = self.sucursal
        service_detail.sucursal_origen = self.sucursal
        service_detail.agente = self.agente
        service_detail.hora_requerida = self.hora_requerida
        service_detail.renglon = 2048 * i
        service_detail.renglon_id = i
        service_detail.articulo = art.articulo
        service_detail.impuesto1 = art.impuesto1
        service_detail.descripcion_extra = art.descripcion1
        service_detail.comentarios = art.descripcion1
        service_detail.precio = 0
        service_detail.ut = 1
        service_detail.cc_tiempo_tab = 1
        return service_detail


class Vin(BaseModel):
    vin = models.CharField(db_column='VIN', primary_key=True, max_length=20)
    articulo = models.CharField(db_column='Articulo', max_length=20, blank=True, null=True)
    km = models.IntegerField(db_column='Km', blank=True, null=True)
    motor = models.CharField(db_column='Motor', max_length=20, blank=True, null=True)
    fecha = models.DateTimeField(db_column='Fecha', blank=True, null=True)
    cliente = models.CharField(db_column='Cliente', max_length=10, blank=True, null=True)
    conductor = models.CharField(db_column='Conductor', max_length=10, blank=True, null=True)
    alta = models.DateTimeField(db_column='Alta', blank=True, null=True)
    empresa = models.CharField(db_column='Empresa', max_length=5, blank=True, null=True)
    placas = models.CharField(db_column='Placas', max_length=20, blank=True, null=True)
    garantia_vencimiento = models.DateTimeField(db_column='GarantiaVencimiento', blank=True, null=True)
    registro = models.CharField(db_column='Registro', max_length=20, blank=True, null=True)
    fecha_carta_credito = models.DateTimeField(db_column='FechaCartaCredito', blank=True, null=True)
    fecha_factura = models.DateTimeField(db_column='FechaFactura', blank=True, null=True)
    fecha_ultimo_servicio = models.DateTimeField(db_column='FechaUltimoServicio', blank=True, null=True)
    fecha_siguiente_servicio = models.DateTimeField(db_column='FechaSiguienteServicio', blank=True, null=True)
    costo = models.FloatField(db_column='Costo', blank=True, null=True)
    modelo = models.CharField(db_column='Modelo', max_length=4, blank=True, null=True)
    tipo_compra = models.CharField(db_column='TipoCompra', max_length=1, blank=True, null=True)
    folio_factura_compra = models.CharField(db_column='FolioFacturaCompra', max_length=15, blank=True, null=True)
    fecha_factura_compra = models.DateTimeField(db_column='FechaFacturaCompra', blank=True, null=True)
    descripcion1 = models.CharField(db_column='Descripcion1', max_length=38, blank=True, null=True)
    descripcion2 = models.CharField(db_column='Descripcion2', max_length=38, blank=True, null=True)
    color_exterior = models.CharField(db_column='ColorExterior', max_length=10, blank=True, null=True)
    color_exterior_descripcion = models.CharField(db_column='ColorExteriorDescripcion', max_length=50, blank=True,
                                                  null=True)
    color_interior = models.CharField(db_column='ColorInterior', max_length=10, blank=True, null=True)
    color_interior_descripcion = models.CharField(db_column='ColorInteriorDescripcion', max_length=50, blank=True,
                                                  null=True)
    fecha_pago = models.DateTimeField(db_column='FechaPago', blank=True, null=True)
    venta_id = models.IntegerField(db_column='VentaID', blank=True, null=True)
    compra_id = models.IntegerField(db_column='CompraID', blank=True, null=True)
    estatus = models.CharField(db_column='Estatus', max_length=15, blank=True, null=True)
    situacion = models.CharField(db_column='Situacion', max_length=50, blank=True, null=True)
    situacion_fecha = models.DateTimeField(db_column='SituacionFecha', blank=True, null=True)
    agente = models.CharField(db_column='Agente', max_length=10, blank=True, null=True)
    tipo_venta = models.CharField(db_column='TipoVenta', max_length=1, blank=True, null=True)
    kilometraje_inicial = models.IntegerField(db_column='KilometrajeInicial', blank=True, null=True)
    cilindros = models.IntegerField(db_column='Cilindros', blank=True, null=True)
    puertas = models.CharField(db_column='Puertas', max_length=30, blank=True, null=True)
    pasajeros = models.IntegerField(db_column='Pasajeros', blank=True, null=True)
    capacidad_carga = models.IntegerField(db_column='CapacidadCarga', blank=True, null=True)
    combustible = models.CharField(db_column='Combustible', max_length=20, blank=True, null=True)
    primera_llamada = models.DateTimeField(db_column='PrimeraLlamada', blank=True, null=True)
    comentarios_primera_llamada = models.CharField(db_column='ComentariosPrimeraLLamada', max_length=1000, blank=True,
                                                   null=True)
    segunda_llamada = models.DateTimeField(db_column='SegundaLlamada', blank=True, null=True)
    comentarios_segunda_llamada = models.CharField(db_column='ComentariosSegundaLLamada', max_length=1000, blank=True,
                                                   null=True)
    tercera_llamada = models.DateTimeField(db_column='TerceraLlamada', blank=True, null=True)
    comentarios_tercera_llamada = models.CharField(db_column='ComentariosTerceraLLamada', max_length=1000, blank=True,
                                                   null=True)

    class Meta:
        db_table = 'VIN'
        managed = False


class Cte(BaseModel):
    cliente = models.CharField(db_column='Cliente', primary_key=True, max_length=10)
    nombre = models.CharField(db_column='Nombre', max_length=254, blank=True, null=True)
    nombre_corto = models.CharField(db_column='NombreCorto', max_length=20, blank=True, null=True)
    direccion = models.CharField(db_column='Direccion', max_length=100, blank=True, null=True)
    direccion_numero = models.CharField(db_column='DireccionNumero', max_length=50, blank=True, null=True)
    observaciones = models.CharField(db_column='Observaciones', max_length=100, blank=True, null=True)
    delegacion = models.CharField(db_column='Delegacion', max_length=100, blank=True, null=True)
    colonia = models.CharField(db_column='Colonia', max_length=100, blank=True, null=True)
    poblacion = models.CharField(db_column='Poblacion', max_length=100, blank=True, null=True)
    estado = models.CharField(db_column='Estado', max_length=30, blank=True, null=True)
    pais = models.CharField(db_column='Pais', max_length=100, blank=True, null=True)
    zona = models.CharField(db_column='Zona', max_length=30, blank=True, null=True)
    codigo_postal = models.CharField(db_column='CodigoPostal', max_length=15, blank=True, null=True)
    rfc = models.CharField(db_column='RFC', max_length=15, blank=True, null=True)
    curp = models.CharField(db_column='CURP', max_length=30, blank=True, null=True)
    telefonos = models.CharField(db_column='Telefonos', max_length=100, blank=True, null=True)
    telefonos_lada = models.CharField(db_column='TelefonosLada', max_length=6, blank=True, null=True)
    contacto1 = models.CharField(db_column='Contacto1', max_length=50, blank=True, null=True)
    contacto2 = models.CharField(db_column='Contacto2', max_length=50, blank=True, null=True)
    extencion1 = models.CharField(db_column='Extencion1', max_length=10, blank=True, null=True)
    extencion2 = models.CharField(db_column='Extencion2', max_length=10, blank=True, null=True)
    email1 = models.CharField(db_column='eMail1', max_length=50, blank=True, null=True)
    email2 = models.CharField(db_column='eMail2', max_length=50, blank=True, null=True)
    categoria = models.CharField(db_column='Categoria', max_length=50, blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=15, blank=True, null=True)
    situacion = models.CharField(db_column='Situacion', max_length=50, blank=True, null=True)
    agente = models.CharField(db_column='Agente', max_length=10, blank=True, null=True)
    agente_servicio = models.CharField(db_column='AgenteServicio', max_length=10, blank=True, null=True)
    estatus = models.CharField(db_column='Estatus', max_length=15)
    ultimo_cambio = models.DateTimeField(db_column='UltimoCambio', blank=True, null=True)
    descripcion1 = models.CharField(db_column='Descripcion1', max_length=50, blank=True, null=True)
    descripcion2 = models.CharField(db_column='Descripcion2', max_length=50, blank=True, null=True)
    descripcion3 = models.CharField(db_column='Descripcion3', max_length=50, blank=True, null=True)
    descripcion4 = models.CharField(db_column='Descripcion4', max_length=50, blank=True, null=True)
    descripcion5 = models.CharField(db_column='Descripcion5', max_length=50, blank=True, null=True)
    descripcion6 = models.CharField(db_column='Descripcion6', max_length=50, blank=True, null=True)
    descripcion7 = models.CharField(db_column='Descripcion7', max_length=50, blank=True, null=True)
    descripcion8 = models.CharField(db_column='Descripcion8', max_length=50, blank=True, null=True)
    descripcion9 = models.CharField(db_column='Descripcion9', max_length=50, blank=True, null=True)
    descripcion10 = models.CharField(db_column='Descripcion10', max_length=50, blank=True, null=True)
    descripcion11 = models.CharField(db_column='Descripcion11', max_length=50, blank=True, null=True)
    descripcion12 = models.CharField(db_column='Descripcion12', max_length=50, blank=True, null=True)
    descripcion13 = models.CharField(db_column='Descripcion13', max_length=50, blank=True, null=True)
    descripcion14 = models.CharField(db_column='Descripcion14', max_length=50, blank=True, null=True)
    descripcion15 = models.CharField(db_column='Descripcion15', max_length=50, blank=True, null=True)
    descripcion16 = models.CharField(db_column='Descripcion16', max_length=50, blank=True, null=True)
    descripcion17 = models.CharField(db_column='Descripcion17', max_length=50, blank=True, null=True)
    descripcion18 = models.CharField(db_column='Descripcion18', max_length=50, blank=True, null=True)
    descripcion19 = models.CharField(db_column='Descripcion19', max_length=50, blank=True, null=True)
    descripcion20 = models.CharField(db_column='Descripcion20', max_length=50, blank=True, null=True)
    personal_nombres = models.CharField(db_column='PersonalNombres', max_length=50, blank=True, null=True)
    personal_apellido_paterno = models.CharField(db_column='PersonalApellidoPaterno', max_length=50, blank=True,
                                                 null=True)
    personal_apellido_materno = models.CharField(db_column='PersonalApellidoMaterno', max_length=50, blank=True,
                                                 null=True)
    personal_direccion = models.CharField(db_column='PersonalDireccion', max_length=100, blank=True, null=True)
    personal_entrecalles = models.CharField(db_column='PersonalEntreCalles', max_length=100, blank=True, null=True)
    personal_plano = models.CharField(db_column='PersonalPlano', max_length=15, blank=True, null=True)
    personal_delegacion = models.CharField(db_column='PersonalDelegacion', max_length=100, blank=True, null=True)
    personal_colonia = models.CharField(db_column='PersonalColonia', max_length=100, blank=True, null=True)
    personal_poblacion = models.CharField(db_column='PersonalPoblacion', max_length=100, blank=True, null=True)
    personal_estado = models.CharField(db_column='PersonalEstado', max_length=30, blank=True, null=True)
    personal_pais = models.CharField(db_column='PersonalPais', max_length=30, blank=True, null=True)
    personal_zona = models.CharField(db_column='PersonalZona', max_length=30, blank=True, null=True)
    personal_codigo_postal = models.CharField(db_column='PersonalCodigoPostal', max_length=15, blank=True, null=True)
    personal_telefonos = models.CharField(db_column='PersonalTelefonos', max_length=100, blank=True, null=True)
    personal_telefonos_lada = models.CharField(db_column='PersonalTelefonosLada', max_length=6, blank=True, null=True)
    personal_telefono_movil = models.CharField(db_column='PersonalTelefonoMovil', max_length=30, blank=True, null=True)
    personal_sms = models.BooleanField(db_column='PersonalSMS', blank=True, null=True)
    fecha_nacimiento = models.DateTimeField(db_column='FechaNacimiento', blank=True, null=True)
    sexo = models.CharField(db_column='Sexo', max_length=20, blank=True, null=True)
    fecha1 = models.DateTimeField(db_column='Fecha1', blank=True, null=True)
    fecha2 = models.DateTimeField(db_column='Fecha2', blank=True, null=True)
    fecha3 = models.DateTimeField(db_column='Fecha3', blank=True, null=True)
    fecha4 = models.DateTimeField(db_column='Fecha4', blank=True, null=True)
    fecha5 = models.DateTimeField(db_column='Fecha5', blank=True, null=True)
    usuario = models.CharField(db_column='Usuario', max_length=10, blank=True, null=True)
    fiscal_regimen = models.CharField(db_column='FiscalRegimen', max_length=30, blank=True, null=True)
    contactar = models.CharField(db_column='Contactar', max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'Cte'
        managed = False


class Empresa(BaseModel):
    empresa = models.CharField(db_column='Empresa', primary_key=True, max_length=5)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)
    grupo = models.CharField(db_column='Grupo', max_length=100, blank=True, null=True)
    direccion = models.CharField(db_column='Direccion', max_length=100, blank=True, null=True)
    direccion_numero = models.CharField(db_column='DireccionNumero', max_length=20, blank=True, null=True)
    direccion_numero_int = models.CharField(db_column='DireccionNumeroInt', max_length=20, blank=True, null=True)
    colonia = models.CharField(db_column='Colonia', max_length=100, blank=True, null=True)
    poblacion = models.CharField(db_column='Poblacion', max_length=30, blank=True, null=True)
    estado = models.CharField(db_column='Estado', max_length=30, blank=True, null=True)
    pais = models.CharField(db_column='Pais', max_length=30, blank=True, null=True)
    codigo_postal = models.CharField(db_column='CodigoPostal', max_length=15, blank=True, null=True)
    telefonos = models.CharField(db_column='Telefonos', max_length=100, blank=True, null=True)
    rfc = models.CharField(db_column='RFC', max_length=20, blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'Empresa'
        managed = False


class Agente(BaseModel):
    agente = models.CharField(db_column='Agente', primary_key=True, max_length=10)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=15, blank=True, null=True)
    categoria = models.CharField(db_column='Categoria', max_length=50, blank=True, null=True)
    familia = models.CharField(db_column='Familia', max_length=50, blank=True, null=True)
    zona = models.CharField(db_column='Zona', max_length=30, blank=True, null=True)
    grupo = models.CharField(db_column='Grupo', max_length=50, blank=True, null=True)
    estatus = models.CharField(db_column='Estatus', max_length=15)
    alta = models.DateTimeField(db_column='Alta', blank=True, null=True)
    baja = models.DateTimeField(db_column='Baja', blank=True, null=True)
    direccion = models.CharField(db_column='Direccion', max_length=100, blank=True, null=True)
    colonia = models.CharField(db_column='Colonia', max_length=255, blank=True, null=True)
    poblacion = models.CharField(db_column='Poblacion', max_length=30, blank=True, null=True)
    estado = models.CharField(db_column='Estado', max_length=30, blank=True, null=True)
    pais = models.CharField(db_column='Pais', max_length=30, blank=True, null=True)
    codigo_postal = models.CharField(db_column='CodigoPostal', max_length=15, blank=True, null=True)
    rfc = models.CharField(db_column='RFC', max_length=20, blank=True, null=True)
    curp = models.CharField(db_column='CURP', max_length=30, blank=True, null=True)
    email = models.CharField(db_column='eMail', max_length=50, blank=True, null=True)
    id_planta = models.CharField(db_column='IdPlanta', max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'Agente'
        managed = False


class Sucursal(BaseModel):
    sucursal = models.IntegerField(db_column='Sucursal', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100, blank=True, null=True)
    prefijo = models.CharField(db_column='Prefijo', max_length=5, blank=True, null=True)
    estatus = models.CharField(db_column='Estatus', max_length=15)
    rfc = models.CharField(db_column='RFC', max_length=20, blank=True, null=True)
    alta = models.DateTimeField(db_column='Alta', blank=True, null=True)
    almacen_principal = models.CharField(db_column='AlmacenPrincipal', max_length=10, blank=True, null=True)
    cliente = models.CharField(db_column='Cliente', max_length=10, blank=True, null=True)
    categoria = models.CharField(db_column='Categoria', max_length=50, blank=True, null=True)
    ip = models.CharField(db_column='IP', max_length=20, blank=True, null=True)
    fiscal_regimen = models.CharField(db_column='FiscalRegimen', max_length=30, blank=True, null=True)
    version = models.CharField(db_column='Version', max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'Sucursal'
        managed = False


class TipoOrdenOperacion(models.Model):
    interfaz = models.CharField(db_column='Interfaz', max_length=100)
    operacion_planta = models.CharField(db_column='OrdenOperacionPlanta', max_length=50)
    operacion_intelisis = models.CharField(db_column='OrdenOperacionIntelisis', max_length=50)

    class Meta:
        managed = False
        db_table = 'CA_MapeoTipoOrdenOperacion'
        unique_together = (('interfaz', 'operacion_intelisis'),)
