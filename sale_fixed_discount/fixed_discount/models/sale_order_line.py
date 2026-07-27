# # # from odoo import api, fields, models
# # #
# # #
# # # class SaleOrderLine(models.Model):
# # #     _inherit = 'sale.order.line'
# # #
# # #     # Fixed Discount Field - ငွေသားနုတ်ခြင်း
# # #     fix_discount = fields.Monetary(
# # #         string='Fixed Discount',
# # #         currency_field='currency_id',
# # #         default=0.0,
# # #         help="Discount in fixed monetary amount (not percentage)"
# # #     )
# # #
# # #     @api.depends('product_uom_qty', 'discount','fix_discount', 'price_unit', 'tax_ids')
# # #     def _compute_amount(self):
# # #         """Override to apply fixed discount to subtotal and total"""
# # #         # မူလတွက်နည်းကို ခေါ်ပါ
# # #         super(SaleOrderLine, self)._compute_amount()
# # #
# # #         # Fixed Discount ကို ပြန်နုတ်ပါ
# # #         for line in self:
# # #             if line.fix_discount and line.product_uom_qty > 0:
# # #                 # Subtotal ကနေ Fixed Discount ကိုနုတ်ပါ
# # #                 new_subtotal = line.price_subtotal - line.fix_discount
# # #                 # အနုတ်မဖြစ်စေဖို့
# # #                 line.price_subtotal = max(new_subtotal, 0.0)
# # #                 # Total ကို ပြန်တွက်ပါ
# # #                 line.price_total = line.price_subtotal + line.price_tax
# # # from odoo import api, fields, models
# # # class SaleOrderLine(models.Model):
# # #     _inherit = 'sale.order.line'
# # #
# # #     fix_discount = fields.Monetary(
# # #         string='Fixed Discount',
# # #         currency_field='currency_id',
# # #         default=0.0
# # #     )
# #
# #     # @api.depends('product_uom_qty', 'discount', 'fix_discount', 'price_unit', 'tax_ids')
# #
# #     # def _compute_amount(self):
# #     #     super()._compute_amount()
# #     #
# #     #     for line in self:
# #     #         if line.fix_discount:
# #     #             line.price_subtotal = max(
# #     #                 line.price_subtotal - line.fix_discount,
# #     #                 0.0
# #     #             )
# #     #
# #     #             line.price_total = max(
# #     #                 line.price_total - line.fix_discount,
# #     #                 0.0
# #     #             )
# # from odoo import api, fields, models
# #
# # class SaleOrderLine(models.Model):
# #     _inherit = 'sale.order.line'
# #
# #     fixed_discount = fields.Monetary(
# #         string='Fixed Discount',
# #         currency_field='currency_id',
# #         default=0.0,
# #         help="Discount in fixed monetary amount (not percentage)"
# #     )
# #
# #     @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids', 'fixed_discount')
# #     def _compute_amount(self):
# #         """Override to apply fixed discount to subtotal and total"""
# #         # ၁. Fixed Discount မပါဘဲ မူလတွက်နည်းကို ခေါ်ပါ
# #         super(SaleOrderLine, self)._compute_amount()
# #
# #         for line in self:
# #             if line.fixed_discount and line.product_uom_qty > 0:
# #                 # ၂. Price Unit ကို လျှော့ပြီး Tax ကို ပြန်တွက်ပါ
# #                 price_unit_after_discount = line.price_unit - (line.fixed_discount / line.product_uom_qty)
# #
# #                 # ၃. Tax ကို ပြန်တွက်ပါ
# #                 if line.tax_ids:
# #                     tax_result = line.tax_ids.compute_all(
# #                         price_unit_after_discount,
# #                         currency=line.currency_id,
# #                         quantity=line.product_uom_qty,
# #                         product=line.product_id,
# #                         partner=line.order_id.partner_shipping_id,
# #                     )
# #                     line.price_subtotal = tax_result['total_excluded']
# #                     line.price_tax = sum(tax.get('amount', 0.0) for tax in tax_result['taxes'])
# #                     line.price_total = tax_result['total_included']
# #                 else:
# #                     # Tax မပါရင်
# #                     line.price_subtotal = price_unit_after_discount * line.product_uom_qty
# #                     line.price_tax = 0.0
# #                     line.price_total = line.price_subtotal
# from odoo import api, fields, models
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
#         """Override to apply fixed discount to subtotal and total"""
#         super(SaleOrderLine, self)._compute_amount()
#         for line in self:
#             if line.fixed_discount and line.product_uom_qty > 0:
#                 new_subtotal = line.price_subtotal - line.fixed_discount
#                 line.price_subtotal = max(new_subtotal, 0.0)
#                 line.price_total = line.price_subtotal + line.price_tax
#
#     def _prepare_invoice_line(self, **optional_values):
#         """Override to include fixed_discount when creating invoice line"""
#         # ၁. မူလတန်ဖိုးတွေကို ရယူပါ
#         res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
#
#         # ၂. fixed_discount ကို ထည့်ပါ
#         if self.fixed_discount:
#             res['fixed_discount'] = self.fixed_discount
#
#         return res
# from odoo import api, fields, models
#
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
#     # Odoo 19 မှာ 'tax_ids' (အများကိန်း) ကို သုံးရပါမယ်
#     @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids', 'fixed_discount')
#     def _compute_amount(self):
#         """Override to properly calculate tax, subtotal, and total with fixed discount for Odoo 19"""
#         # ၁။ ပထမဦးစွာ standard fields တွက်ချက်မှုအတွက် super ကို အရင်ခေါ်ပါ
#         super(SaleOrderLine, self)._compute_amount()
#
#         for line in self:
#             if line.fixed_discount and line.product_uom_qty > 0:
#                 # ၂။ ပစ္စည်းတစ်ခုချင်းစီအလိုက် ကျမည့် fixed discount ကို ရှာပါ
#                 discount_per_unit = line.fixed_discount / line.product_uom_qty
#
#                 # ၃။ မူလ ယူနစ်ဈေးနှုန်းထဲကနေ နှုတ်ပြီး အသားတင်ဈေးနှုန်း ထုတ်ပါ
#                 price_unit_net = line.price_unit - discount_per_unit
#
#                 # ၄။ အကယ်၍ % discount ပါ ရှိနေရင် ထပ်ဆင့်တွက်ချက်ပါ
#                 if line.discount:
#                     price_unit_net = price_unit_net * (1 - (line.discount or 0.0) / 100.0)
#
#                 # ၅။ အခွန် (Tax) ကို line.tax_ids သုံးပြီး ဈေးနှုန်းအသစ်ပေါ်မှာ ပြန်တွက်ခိုင်းပါ
#                 taxes = line.tax_ids.compute_all(
#                     price_unit_net,
#                     line.order_id.currency_id,
#                     line.product_uom_qty,
#                     product=line.product_id,
#                     partner=line.order_id.partner_shipping_id
#                 )
#
#                 # ၆။ တန်ဖိုးများကို Assign လုပ်ပါ (ဒါမှ အောက်ခြေက Untaxed Amount နဲ့ Total လိုက်ပြောင်းမှာပါ)
#                 line.price_subtotal = taxes['total_excluded']
#                 line.price_tax = sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
#                 line.price_total = taxes['total_included']
#
#     def _prepare_invoice_line(self, **optional_values):
#         """Override to include fixed_discount when creating invoice line"""
#         res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
#         if self.fixed_discount:
#             res['fixed_discount'] = self.fixed_discount
#         return res

# from odoo import api, fields, models
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
#
#     fixed_discount = fields.Monetary(
#         string='Fixed Discount',
#         currency_field='currency_id',
#         default=0.0,
#         help="Discount in fixed monetary amount (not percentage)"
#     )
#     def _prepare_invoice_line(self, **optional_values):
#         """Passes the custom fixed discount value cleanly when generating an invoice"""
#         res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
#         if self.fixed_discount:
#             res['fixed_discount'] = self.fixed_discount
#         return res
# from odoo import api, fields, models
#
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
#         """
#         Calculate both percentage discount and fixed discount together
#         """
#
#         for line in self:
#             # ၁။ Standard Odoo အတိုင်း အရင်တွက်ပါ
#             super(SaleOrderLine, line)._compute_amount()
#
#             # ၂။ Fixed Discount ရှိရင် ပြန်တွက်ပါ
#             if line.fixed_discount and line.product_uom_qty > 0:
#                 # Subtotal ကို ပြန်တွက်ပါ
#                 subtotal = line.product_uom_qty * line.price_unit
#
#                 # Percentage Discount
#                 discount_percent = line.discount or 0.0
#                 discount_amount = subtotal * (discount_percent / 100.0)
#
#                 # Fixed Discount
#                 fixed_discount_amount = line.fixed_discount or 0.0
#
#                 # စုစုပေါင်းလျှော့ဈေး
#                 total_discount = discount_amount + fixed_discount_amount
#
#                 # Net Subtotal
#                 line.price_subtotal = max(subtotal - total_discount, 0.0)
#
#                 # Tax ကို ပြန်တွက်ပါ (Net Subtotal ပေါ်မှာ)
#                 if line.tax_ids:
#                     net_unit_price = line.price_subtotal / line.product_uom_qty if line.product_uom_qty > 0 else 0.0
#                     taxes = line.tax_ids.compute_all(
#                         net_unit_price,
#                         currency=line.currency_id,
#                         quantity=line.product_uom_qty,
#                         product=line.product_id,
#                         partner=line.order_id.partner_shipping_id,
#                         record=line,  # Pass record for fixed discount
#                     )
#                     line.price_tax = sum(tax.get('amount', 0.0) for tax in taxes.get('taxes', []))
#                     line.price_total = taxes['total_included']
#                 else:
#                     line.price_tax = 0.0
#                     line.price_total = line.price_subtotal
#
#     @api.onchange('fixed_discount', 'discount', 'product_uom_qty', 'price_unit')
#     def _onchange_fixed_discount(self):
#         """Trigger recomputation when fields change"""
#         if self.fixed_discount or self.discount:
#             self._compute_amount()
#             # Update parent sale order footer
#             if self.order_id:
#                 self.order_id._compute_amounts()
#
#     def _prepare_invoice_line(self, **optional_values):
#         """Pass fixed discount when creating invoice line"""
#         res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
#         if self.fixed_discount:
#             res['fixed_discount'] = self.fixed_discount
#         return res
#
#     def write(self, vals):
#         """Override write to ensure recomputation after save"""
#         result = super(SaleOrderLine, self).write(vals)
#
#         # If discount or fixed_discount changed, recompute
#         if 'discount' in vals or 'fixed_discount' in vals or 'price_unit' in vals or 'product_uom_qty' in vals:
#             self._compute_amount()
#             # Also recompute parent sale order
#             for line in self:
#                 if line.order_id:
#                     line.order_id._compute_amounts()
#
#         return result
#
#
# from odoo import api, fields, models
#
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
#         """Calculate both percentage discount and fixed discount together"""
#
#         for line in self:
#             # Standard Odoo အတိုင်း အရင်တွက်ပါ
#             super(SaleOrderLine, line)._compute_amount()
#
#             # Fixed Discount ရှိရင် ပြန်တွက်ပါ
#             if line.fixed_discount and line.product_uom_qty > 0:
#                 subtotal = line.product_uom_qty * line.price_unit
#                 discount_percent = line.discount or 0.0
#                 discount_amount = subtotal * (discount_percent / 100.0)
#                 fixed_discount_amount = line.fixed_discount or 0.0
#                 total_discount = discount_amount + fixed_discount_amount
#
#                 line.price_subtotal = max(subtotal - total_discount, 0.0)
#
#                 if line.tax_ids:
#                     net_unit_price = line.price_subtotal / line.product_uom_qty if line.product_uom_qty > 0 else 0.0
#                     taxes = line.tax_ids.compute_all(
#                         net_unit_price,
#                         currency=line.currency_id,
#                         quantity=line.product_uom_qty,
#                         product=line.product_id,
#                         partner=line.order_id.partner_shipping_id,
#                     )
#                     line.price_tax = sum(tax.get('amount', 0.0) for tax in taxes.get('taxes', []))
#                     line.price_total = taxes['total_included']
#                 else:
#                     line.price_tax = 0.0
#                     line.price_total = line.price_subtotal
#
#     @api.onchange('fixed_discount', 'discount', 'product_uom_qty', 'price_unit')
#     def _onchange_fixed_discount(self):
#         """Trigger recomputation when fields change"""
#         if self.fixed_discount or self.discount:
#             self._compute_amount()
#             if self.order_id:
#                 self.order_id._compute_amounts()
#
#     def write(self, vals):
#         """Override write to ensure recomputation after save"""
#         result = super(SaleOrderLine, self).write(vals)
#         if 'discount' in vals or 'fixed_discount' in vals or 'price_unit' in vals or 'product_uom_qty' in vals:
#             self._compute_amount()
#             for line in self:
#                 if line.order_id:
#                     line.order_id._compute_amounts()
#         return result
# from odoo import api, fields, models
#
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
#         """Calculate both percentage discount and fixed discount together"""
#
#         for line in self:
#             # ၁။ Standard Odoo အတိုင်း အရင်တွက်ပါ
#             super(SaleOrderLine, line)._compute_amount()
#
#             # ၂။ Fixed Discount ရှိရင် ပြန်တွက်ပါ
#             if line.fixed_discount and line.product_uom_qty > 0:
#                 subtotal = line.product_uom_qty * line.price_unit
#                 discount_percent = line.discount or 0.0
#                 discount_amount = subtotal * (discount_percent / 100.0)
#                 fixed_discount_amount = line.fixed_discount or 0.0
#                 total_discount = discount_amount + fixed_discount_amount
#
#                 line.price_subtotal = max(subtotal - total_discount, 0.0)
#
#                 if line.tax_ids:
#                     net_unit_price = line.price_subtotal / line.product_uom_qty if line.product_uom_qty > 0 else 0.0
#                     taxes = line.tax_ids.compute_all(
#                         net_unit_price,
#                         currency=line.currency_id,
#                         quantity=line.product_uom_qty,
#                         product=line.product_id,
#                         partner=line.order_id.partner_shipping_id,
#                     )
#                     line.price_tax = sum(tax.get('amount', 0.0) for tax in taxes.get('taxes', []))
#                     line.price_total = taxes['total_included']
#                 else:
#                     line.price_tax = 0.0
#                     line.price_total = line.price_subtotal
#
#     @api.onchange('fixed_discount', 'discount', 'product_uom_qty', 'price_unit')
#     def _onchange_fixed_discount(self):
#         """Trigger recomputation when fields change"""
#         if self.fixed_discount or self.discount:
#             self._compute_amount()
#             if self.order_id:
#                 self.order_id._compute_amounts()
#
#     def write(self, vals):
#         """Override write to ensure recomputation after save"""
#         result = super(SaleOrderLine, self).write(vals)
#         if 'discount' in vals or 'fixed_discount' in vals or 'price_unit' in vals or 'product_uom_qty' in vals:
#             self._compute_amount()
#             for line in self:
#                 if line.order_id:
#                     line.order_id._compute_amounts()
#         return result
# from odoo import api, fields, models
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'
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

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    fixed_discount = fields.Float(string='Disc.Amount')

    @api.depends('product_uom_qty', 'discount', 'fixed_discount', 'price_unit', 'tax_ids', 'price_total')
    def _compute_amount(self):
        super()._compute_amount()

    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res.update({
            'fixed_discount': self.fixed_discount,
        })
        return res