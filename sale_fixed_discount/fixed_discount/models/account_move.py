from odoo import api, models
class AccountMove(models.Model):
    _inherit = 'account.move'
    @api.depends(
        'line_ids.price_subtotal',
        'line_ids.price_total',
        'line_ids.fixed_discount',
        'line_ids.discount',
        'line_ids.tax_ids',
        'line_ids.quantity',
    )
    def _compute_amount(self):
        """Override to ensure both discount and fixed discount are reflected in totals"""
        super(AccountMove, self)._compute_amount()

    # ၂. Fixed Discount ကိုပြန်တွက်ပါ
        for move in self:
            total_fixed_discount = sum(move.line_ids.mapped('fixed_discount'))
            if total_fixed_discount:
                # Untaxed Amount ကနေ Discount ကိုနုတ်ပါ
                move.amount_untaxed = max(move.amount_untaxed - total_fixed_discount, 0.0)
                # Total Amount ကနေ Discount ကိုနုတ်ပါ
                move.amount_total = max(move.amount_total - total_fixed_discount, 0.0)
                # Tax Amount ကို ပြန်တွက်ပါ
                move.amount_tax = move.amount_total - move.amount_untaxed

            # ၂. Percentage Discount စုစုပေါင်း
            total_percent_discount = 0.0
            for line in move.line_ids:
                if line.discount and line.quantity > 0:
                    discount_amount = (line.price_unit * line.quantity * line.discount) / 100.0
                    total_percent_discount += discount_amount

            # ၃. စုစုပေါင်း Discount
            total_discount = total_fixed_discount + total_percent_discount

            # ၄. Invoice Totals ကိုပြောင်းပါ
            if total_discount:
                move.amount_untaxed = max(move.amount_untaxed - total_discount, 0.0)
                move.amount_total = max(move.amount_total - total_discount, 0.0)
                move.amount_tax = move.amount_total - move.amount_untaxed

