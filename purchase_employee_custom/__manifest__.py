{
    "name": "Purchase Employee Custom",
    "version": "19.0.1.0.0",
    "category": "Purchases",
    "summary": "Add employee to purchase orders",
    "description": """
        Add employee field to:
        - Purchase Order Form
        - Vendor Bill/Invoice
        - List View
        - Search/Group By
        -  Purchase Order Report
    """,
    "author": "Your Company",
    "license": "LGPL-3",
    "depends": [
        "purchase",
        "account",
        "hr",
    ],
    "data": [
        "views/purchase_views.xml",
        "views/account_move_views.xml",
        "report/purchase_order_templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
