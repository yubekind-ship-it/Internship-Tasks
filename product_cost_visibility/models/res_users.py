from odoo import fields, models
class ResUsers(models.Model):
    _inherit = 'res.users'

    show_product_cost = fields.Boolean(
        string='Show Product Cost',
        default=False,
        help="If enabled, product cost will be visible in product forms and lists"
    )