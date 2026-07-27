# from odoo import api, fields, models
#
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     @api.depends(
#         'order_line.price_subtotal',
#         'order_line.price_total',
#         'order_line.fixed_discount',
#         'order_line.discount',
#         'order_line.product_uom_qty',
#         'order_line.price_unit'
#     )
#     def _compute_amounts(self):
#         """Ensure Sale Order footer totals (Untaxed Amount, Tax, Total) are correct"""
#
#         for order in self:
#             # ၁။ ပထမ Standard Odoo အတိုင်း တွက်ပါ
#             super(SaleOrder, order)._compute_amounts()
#
#             # ၂။ စုစုပေါင်းလျှော့ဈေးကို ပြန်တွက်ပါ
#             total_discount = 0.0
#             for line in order.order_line:
#                 subtotal = line.product_uom_qty * line.price_unit
#                 discount_amount = subtotal * (line.discount / 100.0) if line.discount else 0.0
#                 fixed_discount_amount = line.fixed_discount or 0.0
#                 total_discount += discount_amount + fixed_discount_amount
#
#             # ၃။ လျှော့ဈေးရှိရင် Untaxed Amount နဲ့ Total ကို ပြန်တွက်ပါ
#             if total_discount:
#                 order.amount_untaxed = max(order.amount_untaxed - total_discount, 0.0)
#                 order.amount_total = max(order.amount_total - total_discount, 0.0)
#                 order.amount_tax = max(order.amount_total - order.amount_untaxed, 0.0)
#
#                 # 🔑 Debug: print ထုတ်ကြည့်ပါ
#                 print(f"Total Discount: {total_discount}")
#                 print(f"Untaxed: {order.amount_untaxed}")
#                 print(f"Total: {order.amount_total}")