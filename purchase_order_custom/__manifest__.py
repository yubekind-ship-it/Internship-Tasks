{
    'name': 'Purchase Order Custom',
    'version': '19.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Override create, write, and unlink methods on purchase.order',
    'description': """
        This module demonstrates how to override CRUD methods on the Purchase Order model in Odoo 19.
    """,
    'author': 'Your Name',
    'depends': ['base', 'purchase'],
    'data': [
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}