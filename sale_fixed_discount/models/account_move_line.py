from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # Fixed Discount Field - Invoice မှာပါဖို့
    fixed_discount = fields.Monetary(
        string='Fixed Discount',
        currency_field='currency_id',
        default=0.0,
        help="Discount in fixed monetary amount (not percentage)"
    )

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids')
    def _compute_amount(self):
        """Override to apply fixed discount to invoice lines"""
        super(AccountMoveLine, self)._compute_amount()
        for line in self:
            if line.fixed_discount and line.quantity > 0:
                new_subtotal = line.price_subtotal - line.fixed_discount
                line.price_subtotal = max(new_subtotal, 0.0)
                line.price_total = line.price_subtotal + line.price_tax