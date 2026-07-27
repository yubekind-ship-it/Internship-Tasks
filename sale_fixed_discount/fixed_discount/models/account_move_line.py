# from odoo import api, fields, models
#
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     fixed_discount = fields.Monetary(
#         string='Fixed Discount',
#         currency_field='currency_id',
#         default=0.0,
#         help="Discount in fixed monetary amount (not percentage)"
#     )
#
#     @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids', 'fixed_discount')
#     def _compute_amount(self):
#         """Override to apply both percentage discount and fixed discount"""
#         super(SaleOrderLine, self)._compute_amount()
#         for line in self:
#             if line.fixed_discount and line.product_uom_qty > 0:
#                 line.price_subtotal = max(line.price_subtotal - line.fixed_discount, 0.0)
#                 line.price_total = line.price_subtotal + line.price_tax
#
#     def _prepare_invoice_line(self, **optional_values):
#         """Override to include fixed_discount when creating invoice line"""
#         res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
#         if self.fixed_discount:
#             res['fixed_discount'] = self.fixed_discount
#         return res
# from odoo import api, fields, models
# from odoo.tools import frozendict
# from collections import defaultdict
# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'
#     fixed_discount = fields.Monetary(
#                 string='Fixed Discount',
#                 currency_field='currency_id',
#                 default=0.0,
#         help="Discount in fixed monetary amount (not percentage)"
#             )
#     discount_amount = fields.Float(string='Disc.Amount')
#     discount_allocation_needed = fields.Boolean(
#         compute='_compute_discount_allocation_needed',
#         store=False
#     )
#     discount_allocation_dirty = fields.Boolean(
#         default=False
#     )
#     @api.depends('account_id', 'company_id', 'discount', 'discount_amount', 'price_unit', 'quantity', 'currency_rate',
#                  'analytic_distribution')
#     def _compute_discount_allocation_needed(self):
#         """Compute discount allocation for lines"""
#         for move in self.mapped('move_id'):
#             # Get discount allocation account
#             discount_allocation_account = move._get_discount_allocation_account() if hasattr(move,'_get_discount_allocation_account')\
#             else False
#             if not discount_allocation_account:
#                 for line in move.line_ids:
#                     line.discount_allocation_needed = False
#                 continue
#
#             # Calculate discounted amounts per line
#             line2discounted_amount = {}
#             for line in move.line_ids:
#                 if line.display_type == 'product' and line.account_id != discount_allocation_account:
#                     amount = line.currency_id.round(
#                         line.move_id.direction_sign
#                         * line.quantity
#                         * (
#                                 (line.price_unit * (line.discount or 0.0) / 100.0)
#                                 + (line.discount_amount or 0.0)
#                         )
#                     )
#                     if amount:
#                         line2discounted_amount[line] = [
#                             (line.account_id, amount),
#                             (discount_allocation_account, -amount),
#                         ]
#             # Aggregate distribution totals
#             distribution_totals = defaultdict(lambda: defaultdict(float))
#             for line, discounted_amounts in line2discounted_amount.items():
#                 for account, amount in discounted_amounts:
#                     for analytic_account_id in (line.analytic_distribution or {}):
#                         distribution_totals[frozendict({
#                             'move_id': line.move_id.id,
#                             'account_id': account.id,
#                             'currency_rate': line.currency_rate,
#                         })][analytic_account_id] += amount
#             # Set discount allocation needed
#             for line in move.line_ids:
#                 line.discount_allocation_dirty = True
#                 if line not in line2discounted_amount:
#                     line.discount_allocation_needed = False
#                     continue
#                 discount_allocation_needed = {}
#                 for account, amount in line2discounted_amount[line]:
#                     key = frozendict({
#                         'move_id': line.move_id.id,
#                         'account_id': account.id,
#                         'currency_rate': line.currency_rate,
#                     })
#                     dist = distribution_totals.get(key, {})
#                     total = sum(dist.values())
# from odoo import models, fields, api, _
# from odoo.tools import frozendict
# from collections import defaultdict
# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'
#     fixed_discount = fields.Monetary(
#                         string='Fixed Discount',
#                         currency_field='currency_id',
#                         default=0.0,
#                 help="Discount in fixed monetary amount (not percentage)"
#                     )
#     discount_amount = fields.Float(string='Disc.Amount')
#     discount_allocation_needed = fields.Boolean(
#         compute='_compute_discount_allocation_needed',
#         store=False
#     )
#     discount_allocation_dirty = fields.Boolean(
#         default=False
#     )
#
#     @api.depends('account_id', 'company_id', 'discount', 'discount_amount', 'price_unit', 'quantity', 'currency_rate',
#                  'analytic_distribution')
#     def _compute_discount_allocation_needed(self):
#         """Compute discount allocation for lines"""
#         for move in self.mapped('move_id'):
#             # Get discount allocation account
#             discount_allocation_account = move._get_discount_allocation_account() if hasattr(move,
#                                                                                              '_get_discount_allocation_account') else False
#
#             if not discount_allocation_account:
#                 for line in move.line_ids:
#                     line.discount_allocation_needed = False
#                 continue
#
#             # Calculate discounted amounts per line
#             line2discounted_amount = {}
#             for line in move.line_ids:
#                 if line.display_type == 'product' and line.account_id != discount_allocation_account:
#                     amount = line.currency_id.round(
#                         line.move_id.direction_sign
#                         * line.quantity
#                         * (
#                                 (line.price_unit * (line.discount or 0.0) / 100.0)
#                                 + (line.discount_amount or 0.0)
#                         )
#                     )
#                     if amount:
#                         line2discounted_amount[line] = [
#                             (line.account_id, amount),
#                             (discount_allocation_account, -amount),
#                         ]
#
#             # Aggregate distribution totals
#             distribution_totals = defaultdict(lambda: defaultdict(float))
#             for line, discounted_amounts in line2discounted_amount.items():
#                 for account, amount in discounted_amounts:
#                     for analytic_account_id in (line.analytic_distribution or {}):
#                         distribution_totals[frozendict({
#                             'move_id': line.move_id.id,
#                             'account_id': account.id,
#                             'currency_rate': line.currency_rate,
#                         })][analytic_account_id] += amount
#
#             # Set discount allocation needed
#             for line in move.line_ids:
#                 line.discount_allocation_dirty = True
#                 if line not in line2discounted_amount:
#                     line.discount_allocation_needed = False
#                     continue
#
#                 discount_allocation_needed = {}
#                 for account, amount in line2discounted_amount[line]:
#                     key = frozendict({
#                         'move_id': line.move_id.id,
#                         'account_id': account.id,
#                         'currency_rate': line.currency_rate,
#                     })
#                     dist = distribution_totals.get(key, {})
#                     total = sum(dist.values()) or 1.0
#
#                     discount_allocation_needed[key] = frozendict({
#                         'display_type': 'discount',
#                         'name': _("Discount"),
#                         'amount_currency': amount,
#                         'analytic_distribution': {
#                             str(account_id): 100.0 * value / total
#                             for account_id, value in dist.items()
#                         }
#                     })
#                 line.discount_allocation_needed = discount_allocation_needed
#
#     @api.depends('quantity', 'discount', 'discount_amount', 'price_unit', 'tax_ids', 'currency_id')
#     def _compute_totals(self):
#         """Override to handle discount amounts in totals"""
#         super()._compute_totals()
# from odoo import api, fields, models
#
#
# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'
#
#     # Fixed Discount Field
#     fixed_discount = fields.Monetary(
#         string='Fixed Discount',
#         currency_field='currency_id',
#         default=0.0,
#         help="Discount in fixed monetary amount (not percentage)"
#     )
#
#     @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', 'fixed_discount')
#     def _compute_amount(self):
#         """Apply both percentage discount and fixed discount to invoice lines"""
#         for line in self:
#             if line.quantity > 0:
#                 # 1. မူလ price_unit ကိုယူပါ
#                 price_unit = line.price_unit
#
#                 # 2. Percentage Discount (%) ကို ဦးစွာ တွက်ပါ
#                 price_after_percent = price_unit * (1 - (line.discount / 100.0))
#
#                 # 3. Fixed Discount ကို ထည့်တွက်ပါ
#                 if line.fixed_discount:
#                     price_after_fixed = price_after_percent - (line.fixed_discount / line.quantity)
#                 else:
#                     price_after_fixed = price_after_percent
#
#                 # 4. Subtotal ကို တွက်ပါ (Tax မပါ)
#                 line.price_subtotal = max(price_after_fixed, 0.0) * line.quantity
#
#                 # 5. Tax တွက်ပါ
#                 if line.tax_ids:
#                     tax_result = line.tax_ids.compute_all(
#                         max(price_after_fixed, 0.0),
#                         currency=line.currency_id,
#                         quantity=line.quantity,
#                         product=line.product_id,
#                         partner=line.partner_id,
#                     )
#                     line.price_tax = sum(tax.get('amount', 0.0) for tax in tax_result['taxes'])
#                 else:
#                     line.price_tax = 0.0
#
#                 # 6. Total ကို တွက်ပါ (Tax ပါ)
#                 line.price_total = line.price_subtotal + line.price_tax
#
#                 # 7. Line Amount ကို ပြောင်းပါ
#                 line.amount_currency = line.price_subtotal
#                 line.balance = line.price_subtotal
#             else:
#                 # Quantity 0 ဆိုရင် မူလတွက်နည်းကိုသုံးပါ
#                 super(AccountMoveLine, line)._compute_amount()

from odoo import models, fields, api, _
from odoo.tools import frozendict
from collections import defaultdict


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    fixed_discount = fields.Float(string='Disc.Amount')

    @api.depends('account_id', 'company_id', 'discount', 'fixed_discount', 'price_unit', 'quantity', 'currency_rate',
                 'analytic_distribution')
    def _compute_discount_allocation_needed(self):

        line2discounted_amount = {
            line: [
                (line.account_id, amount),
                (discount_allocation_account, -amount),
            ]
            for line in self.move_id.line_ids
            if line.display_type == 'product'
               and (discount_allocation_account := line.move_id._get_discount_allocation_account())
               and line.account_id != discount_allocation_account
               and (amount := line.currency_id.round(
                line.move_id.direction_sign
                * line.quantity
                * (
                        (line.price_unit * (line.discount or 0.0) / 100)
                        + (line.fixed_discount or 0.0)
                )
            ))
        }

        distribution_totals = defaultdict(lambda: defaultdict(float))
        for line, discounted_amounts in line2discounted_amount.items():
            for account, amount in discounted_amounts:
                for analytic_account_id in line.analytic_distribution or {}:
                    distribution_totals[frozendict({
                        'move_id': line.move_id.id,
                        'account_id': account.id,
                        'currency_rate': line.currency_rate,
                    })][analytic_account_id] += amount

        for line in self:
            line.discount_allocation_dirty = True
            if line not in line2discounted_amount:
                line.discount_allocation_needed = False
                continue

            discount_allocation_needed = {}
            for account, amount in line2discounted_amount[line]:
                key = frozendict({
                    'move_id': line.move_id.id,
                    'account_id': account.id,
                    'currency_rate': line.currency_rate,
                })
                dist = distribution_totals[key]
                total = sum(dist.values()) or 1

                discount_allocation_needed[key] = frozendict({
                    'display_type': 'discount',
                    'name': _("Discount"),
                    'amount_currency': amount,
                    'analytic_distribution': {
                        account_id: 100 * value / total
                        for account_id, value in dist.items()
                    }
                })

            line.discount_allocation_needed = discount_allocation_needed

    @api.depends('quantity', 'discount', 'fixed_discount', 'price_unit', 'tax_ids', 'currency_id')
    def _compute_totals(self):
        super()._compute_totals()