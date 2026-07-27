# from odoo import api, models
# class AccountTax(models.Model):
#     _inherit = 'account.tax'
#     @api.model
#     def _prepare_base_line_for_taxes_computation(self, record, **kwargs):
#         """Override to handle both percentage discount and fixed discount in tax computation"""
#         base_line = super()._prepare_base_line_for_taxes_computation(record, **kwargs)
#         if record and hasattr(record, 'fixed_discount'):
#             fixed_discount = record.fixed_discount
#             if fixed_discount and base_line.get('quantity', 0.0) > 0:
#                 price_unit = base_line.get('price_unit', 0.0)
#                 quantity = base_line.get('quantity', 1.0)
#                 if quantity > 0:
#                     # Percentage Discount ကိုပါ ထည့်တွက်ပါ
#                     discount_percent = 0.0
#                     if hasattr(record, 'discount'):
#                         discount_percent = record.discount or 0.0
#
#                     # ပထမ percentage discount ကိုနုတ်ပါ
#                     price_after_percent = price_unit * (1 - (discount_percent / 100.0))
#                     # ပြီးရင် fixed discount ကိုနုတ်ပါ
#                     net_price_unit = price_after_percent - (fixed_discount / quantity)
#                     base_line['price_unit'] = max(net_price_unit, 0.0)
#
#                     base_line['manual_total_excluded_currency'] = max((price_unit * quantity) - fixed_discount, 0.0)
#                     base_line['manual_total_excluded'] = base_line['manual_total_excluded_currency']
#
#         return base_line
#     @api.model
#     def _prepare_base_line_grouping_key(self, base_line):
#         """Override to include fixed discount in grouping key"""
#         result = super()._prepare_base_line_grouping_key(base_line)
#         if base_line.get('record') and hasattr(base_line['record'], 'fixed_discount'):
#             result['fixed_discount'] = base_line['record'].fixed_discount
#
#         return result

from odoo import models, api


class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.model
    def _prepare_base_line_for_taxes_computation(self, record, **kwargs):
        base_line = super()._prepare_base_line_for_taxes_computation(record, **kwargs)

        if record and hasattr(record, 'fixed_discount'):
            price_unit = base_line['price_unit'] * (
                    1 - (base_line.get('discount', 0.0) or 0.0) / 100.0
            )
            price_unit -= (record.fixed_discount or 0.0)
            base_line.update({
                'price_unit': price_unit,
                'discount': 0.0,
            })

        return base_line

    @api.model
    def _prepare_base_line_grouping_key(self, base_line):
        result = super()._prepare_base_line_grouping_key(base_line)
        result['fixed_discount'] = base_line.get('fixed_discount', 0.0)
        return result