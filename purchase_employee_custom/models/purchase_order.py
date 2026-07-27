from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        help="Employee responsible for this purchase order",
        tracking=True,
        index=True,
    )

    def _prepare_invoice(self):
        """Pass employee to invoice when creating bill"""
        invoice_vals = super()._prepare_invoice()
        if self.employee_id:
            invoice_vals["employee_id"] = self.employee_id.id
        return invoice_vals
