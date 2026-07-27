{
    'name': 'Fixed Discount',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Fixed amount discount on sale order and invoice lines',
    'description': """
        This module adds a fixed monetary discount field to:
        - Sale Order Lines
        - Invoice Lines

        Features:
        - Fixed discount in monetary amount (not percentage)
        - Works together with percentage discount
        - Automatically updates subtotal and total amounts
        - Works on both Sale Orders and Invoices
        - Appears in Sale Order and Invoice PDF reports
    """,
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'depends': ['product','sale','account','base'],
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'report/sale_order_report.xml',
        'report/invoice_report.xml',


    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}