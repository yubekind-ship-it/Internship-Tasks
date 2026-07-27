from odoo import api, fields, models
from odoo.fields import Command
class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.model
    def _prepare_base_line_for_taxes_computation(self, record, **kwargs):
        """
        Override to inject fixed discount into tax computation base line
        """
        base_line = super(AccountTax, self)._prepare_base_line_for_taxes_computation(record, **kwargs)

        # Check if record has fixed_discount field
        if record and hasattr(record, 'fixed_discount'):
            fixed_discount = record.fixed_discount
            if fixed_discount and base_line.get('quantity', 0.0) > 0:
                price_unit = base_line.get('price_unit', 0.0)
                quantity = base_line.get('quantity', 1.0)

                if quantity > 0:
                    # Get percentage discount from record if available
                    discount_percent = 0.0
                    if hasattr(record, 'discount'):
                        discount_percent = record.discount or 0.0

                    # Calculate price after percentage discount
                    price_after_percent = price_unit * (1 - (discount_percent / 100.0))

                    # Then subtract fixed discount per unit
                    net_price_unit = price_after_percent - (fixed_discount / quantity)
                    base_line['price_unit'] = max(net_price_unit, 0.0)

                    # Update manual total excluded (for tax calculation)
                    base_line['manual_total_excluded_currency'] = max((price_unit * quantity) - fixed_discount, 0.0)
                    base_line['manual_total_excluded'] = base_line['manual_total_excluded_currency']

        return base_line

    @api.model
    def _prepare_base_line_grouping_key(self, base_line):
        """
        Override to include fixed discount in grouping key for tax lines
        """
        result = super(AccountTax, self)._prepare_base_line_grouping_key(base_line)

        if base_line.get('record') and hasattr(base_line['record'], 'fixed_discount'):
            result['fixed_discount'] = base_line['record'].fixed_discount

        return result

    def compute_all(self, price_unit, currency=None, quantity=1.0, product=None, partner=None,
                    is_refund=False, handle_price_include=True, include_caba_tags=False,
                    rounding_method=None):
        """
        Override compute_all to ensure both percentage discount and fixed discount are applied
        """
        # Get fixed discount from context if available
        fixed_discount = self.env.context.get('fixed_discount', 0.0)

        # Check if record is passed in kwargs
        record = kwargs.get('record')
        if record and hasattr(record, 'fixed_discount'):
            fixed_discount = record.fixed_discount or 0.0

            # Get percentage discount from record
            discount_percent = 0.0
            if hasattr(record, 'discount'):
                discount_percent = record.discount or 0.0

            # Calculate net price after both discounts
            price_after_percent = price_unit * (1 - (discount_percent / 100.0))
            adjusted_price = price_after_percent - (fixed_discount / quantity) if quantity > 0 else 0.0
            price_unit = max(adjusted_price, 0.0)

        # Call parent with adjusted price_unit
        result = super(AccountTax, self).compute_all(
            price_unit=price_unit,
            currency=currency,
            quantity=quantity,
            product=product,
            partner=partner,
            is_refund=is_refund,
            handle_price_include=handle_price_include,
            include_caba_tags=include_caba_tags,
            rounding_method=rounding_method
        )

        # Apply fixed discount to final totals if not already applied via record
        if fixed_discount and quantity > 0 and not (record and hasattr(record, 'fixed_discount')):
            result['total_excluded'] = max(result['total_excluded'] - fixed_discount, 0.0)
            result['total_included'] = max(result['total_included'] - fixed_discount, 0.0)

            # Adjust individual tax amounts proportionally
            if result.get('taxes'):
                total_tax = sum(tax.get('amount', 0.0) for tax in result['taxes'])
                if total_tax > 0:
                    for tax in result['taxes']:
                        tax['amount'] = (tax['amount'] / total_tax) * result['total_included']

        return result
# from odoo import api, fields, models
#
#
# class AccountTax(models.Model):
#     _inherit = 'account.tax'
#
#     def compute_all(self, price_unit, currency=None, quantity=1.0, product=None, partner=None, is_refund=False,
#                     handle_price_include=True, include_caba_tags=False, rounding_method=None):
#         """Override to handle fixed discount from sale.order.line"""
#         # Call parent to get standard tax computation
#         result = super(AccountTax, self).compute_all(
#             price_unit=price_unit,
#             currency=currency,
#             quantity=quantity,
#             product=product,
#             partner=partner,
#             is_refund=is_refund,
#             handle_price_include=handle_price_include,
#             include_caba_tags=include_caba_tags,
#             rounding_method=rounding_method
#         )
#
#         # Check if we have a fixed discount from the context
#         fixed_discount = self.env.context.get('fixed_discount', 0.0)
#         if fixed_discount and quantity > 0:
#             # Reduce total_excluded and total_included by fixed discount
#             result['total_excluded'] = max(result['total_excluded'] - fixed_discount, 0.0)
#             result['total_included'] = max(result['total_included'] - fixed_discount, 0.0)
#
#             # Also adjust individual tax amounts proportionally
#             if result.get('taxes'):
#                 total_tax = sum(tax.get('amount', 0.0) for tax in result['taxes'])
#                 if total_tax > 0:
#                     for tax in result['taxes']:
#                         tax['amount'] = (tax['amount'] / total_tax) * result['total_included']
#
#         return result
