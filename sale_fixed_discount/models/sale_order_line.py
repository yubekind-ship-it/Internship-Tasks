from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    fixed_discount = fields.Monetary(
        string='Fixed Discount',
        currency_field='currency_id',
        default=0.0,
        help="Discount in fixed monetary amount (not percentage)"
    )

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids', 'fixed_discount')
    def _compute_amount(self):
        super(SaleOrderLine, self)._compute_amount()
        for line in self:
            if line.fixed_discount and line.product_uom_qty > 0:
                new_subtotal = line.price_subtotal - line.fixed_discount
                if new_subtotal < 0:
                    new_subtotal = 0.0
                line.price_subtotal = new_subtotal
                line.price_total = line.price_subtotal + line.price_tax