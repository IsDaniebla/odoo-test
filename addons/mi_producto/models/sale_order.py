from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    sale_type = fields.Selection([
        ('direct', 'Venta Directa'),
        ('shipping', 'Envíos')
    ], string='Tipo de Venta', default='direct', required=True,
       help="Especifica si es una venta directa o un envío")
    
    productos_nuevos_con_medidas = fields.Boolean(
        string="Productos nuevos con tomas de medidas necesarias"
    )
    
    plataforma = fields.Selection([
        ('mercado_libre', 'Mercado Libre'),
        ('amazon', 'Amazon'),
        ('coppel', 'Coppel')
    ], string="Plataforma")
    
    cuenta = fields.Selection([
        ('dehom', 'Dehom'),
        ('lean', 'Lean'),
        ('mebix', 'Mebix')
    ], string="Cuenta")

    fecha_pedido = fields.Datetime(string="Fecha de pedido", compute='_compute_fecha_pedido', store=True)
    
    @api.depends('date_order')
    def _compute_fecha_pedido(self):
        for order in self:
            order.fecha_pedido = order.date_order
    fecha_validacion = fields.Datetime(string="Fecha de Validacion (Delivery)", compute='_compute_fecha_validacion', store=True)
    picking_hrs = fields.Char(string="Picking (Hrs)", compute='_compute_tiempos', store=True)
    delivery_dias = fields.Float(string="Delivery (Días)", compute='_compute_tiempos', store=True)

    @api.depends('date_order')
    def _compute_fecha_validacion(self):
        for order in self:
            if hasattr(order, 'picking_ids'):
                pickings = order.picking_ids.filtered(lambda p: p.state == 'done' and p.date_done)
                order.fecha_validacion = pickings[:1].date_done if pickings else order.date_order
            else:
                order.fecha_validacion = order.date_order

    @api.depends('fecha_pedido', 'fecha_validacion')
    def _compute_tiempos(self):
        for order in self:
            if order.fecha_pedido and order.fecha_validacion:
                delta = order.fecha_validacion - order.fecha_pedido
                horas = delta.total_seconds() // 3600
                minutos = (delta.total_seconds() % 3600) // 60
                order.picking_hrs = f"{int(horas):02}:{int(minutos):02}"
                order.delivery_dias = round(delta.total_seconds() / 86400, 2)
            else:
                order.picking_hrs = False
                order.delivery_dias = 0.0

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    copy_sku_button = fields.Html(string='Copiar SKU', compute='_compute_copy_sku_button', sanitize=False)

    def _compute_copy_sku_button(self):
        for line in self:
            sku = line.product_id.default_code or ''
            line.copy_sku_button = f"""
                <span>{sku}</span>
                <button type='button' class='btn btn-primary btn-copy-sku' data-sku='{sku}'>
                    <i class='fa fa-copy'></i> Copiar
                </button>
            """