{
    'name': 'Product Cost Visibility',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Show/hide product cost based on user setting',
    'description': """
        This module adds a field in user access rights to show/hide product cost.
        If enabled, product cost will be visible in product forms and lists.
    """,
    'author': 'Your Name',
    'depends': ['base', 'product', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_users_views.xml',
        'views/product_template_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}