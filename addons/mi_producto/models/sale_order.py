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

    sku_text = fields.Char(string="SKU", compute='_compute_sku_text', store=False)
    amazon_tag_ids = fields.Many2many(
        'amazon.product.tag',
        compute='_compute_amazon_tag_ids',
        string='Etiquetas Amazon',
        store=False
    )
    product_image_128 = fields.Image(string="Imagen", compute='_compute_product_image_128', store=False)

    @api.depends('product_id')
    def _compute_sku_text(self):
        for line in self:
            line.sku_text = line.product_id.default_code or ''

    @api.depends('product_id.amazon_tag_ids')
    def _compute_amazon_tag_ids(self):
        for line in self:
            if line.product_id and hasattr(line.product_id, 'amazon_tag_ids'):
                line.amazon_tag_ids = line.product_id.amazon_tag_ids
            else:
                line.amazon_tag_ids = [(5, 0, 0)]

    @api.depends('product_id.image_128')
    def _compute_product_image_128(self):
        for line in self:
            line.product_image_128 = line.product_id.image_128

    def action_copy_sku(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'SKU',
                'message': f'SKU: {self.product_id.default_code or ""}',
                'sticky': False,
            }
        }

class AmazonTag(models.Model):
    _name = 'amazon.product.tag'
    _description = 'Etiqueta Amazon para Producto'

    name = fields.Char('Nombre', required=True, translate=True)
    product_id = fields.Many2one('product.template', string='Producto', ondelete='cascade', required=True)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_studio_vendido_en_coppel = fields.Selection([
        ('AG', 'AG'),
    ], string='Vendido en Coppel',
       help="Especifica desde donde proviene el producto para Coppel")
    x_studio_vendido_en_fba = fields.Selection([
        ('AG', 'AG'),
        ('FBA', 'FBA'),
    ], string='Vendido en FBA',
       help="Especifica desde donde proviene el producto para FBA")
    x_studio_vendido_en_full = fields.Selection([
        ('AG', 'AG'),
        ('FULL', 'FULL'),
    ], string='Vendido en FULL',
       help="Especifica desde donde proviene el producto para FULL")

    amazon_tag_ids = fields.One2many('amazon.product.tag', 'product_id', string='Tags Amazon')

