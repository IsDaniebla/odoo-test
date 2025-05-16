{
    'name': 'Producto Personalizado',
    'version': '1.0',
    'summary': 'Un módulo que agrega un producto personalizado',
    'description': 'Este módulo agrega un modelo de Producto Personalizado en Odoo.',
    'author': 'Tu Nombre',
    'depends': ['sale'],
    'data': [
        'views/sale_order_views.xml',
        'views/product_kanban_views.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'mi_producto/static/src/js/copy_sku.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,

}