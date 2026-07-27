from odoo import api, fields, models, exceptions


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # Add a custom field for demonstration
    approval_code = fields.Char(string='Approval Code', help='Unique approval code for this purchase order')
    is_priority = fields.Boolean(string='Priority Order', default=False)

    # ==================== CREATE METHOD ====================
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create method for Purchase Order
        Called when creating new purchase orders or RFQs

        Note: Use @api.model_create_multi for batch creation in Odoo 19
        """
        # --- PRE-CREATE LOGIC: Modify values before saving ---
        for vals in vals_list:
            # Auto-generate approval code if not provided
            if not vals.get('approval_code') and vals.get('partner_id'):
                partner = self.env['res.partner'].browse(vals['partner_id'])
                vals['approval_code'] = f"PO-{partner.name[:5].upper()}-{vals.get('name', 'NEW')}"

            # Prevent creating purchase order without vendor
            if not vals.get('partner_id'):
                raise exceptions.ValidationError("Vendor is required for purchase order!")

            # Auto-set priority for high-value orders (example logic)
            if vals.get('amount_total', 0) > 10000:
                vals['is_priority'] = True

        # --- CALL THE ORIGINAL METHOD ---
        # CRITICAL: Always call super() to preserve Odoo's default behavior
        purchase_orders = super().create(vals_list)

        # --- POST-CREATE LOGIC: Actions after creation ---
        for po in purchase_orders:
            # Log message in chatter
            po.message_post(
                body=f"Purchase Order created with Approval Code: {po.approval_code}",
                message_type='notification'
            )

            # Send notification for priority orders
            if po.is_priority:
                po.message_post(
                    body="⚠️ This is a HIGH PRIORITY order requiring immediate attention!",
                    message_type='notification'
                )

        return purchase_orders

    # ==================== WRITE METHOD ====================
    def write(self, vals):
        """
        Override write method for Purchase Order
        Called when updating existing purchase orders
        """
        # --- PRE-WRITE LOGIC: Validate before updating ---

        # Restriction 1: Prevent modifying confirmed/done purchase orders
        if 'partner_id' in vals or 'order_line' in vals:
            for po in self:
                if po.state in ['purchase', 'done']:
                    raise exceptions.UserError(
                        f"Cannot modify vendor or order lines on confirmed purchase order: {po.name}"
                    )

        # Restriction 2: Validate approval code changes
        if 'approval_code' in vals:
            for po in self:
                if po.state == 'done' and po.approval_code != vals['approval_code']:
                    raise exceptions.UserError(
                        f"Cannot change approval code for completed PO: {po.name}"
                    )

        # Restriction 3: Track priority changes
        if 'is_priority' in vals:
            for po in self:
                old_priority = po.is_priority
                new_priority = vals['is_priority']
                if old_priority != new_priority:
                    po.message_post(
                        body=f"Priority status changed from {old_priority} to {new_priority}",
                        message_type='notification'
                    )

        # --- CALL THE ORIGINAL METHOD ---
        result = super().write(vals)

        # --- POST-WRITE LOGIC: Actions after update ---
        if vals.get('state') == 'purchase':
            # When order is confirmed
            self.message_post(
                body="✅ Purchase Order has been confirmed!",
                message_type='notification'
            )

        return result

    # ==================== UNLINK METHOD ====================
    def unlink(self):
        """
        Override unlink method for Purchase Order
        Called when deleting purchase orders

        Note: For simple deletion restrictions, consider using @api.ondelete decorator instead
        """
        # --- PRE-UNLINK LOGIC: Prevent deletion under certain conditions ---
        for po in self:
            # Prevent deletion of confirmed or done purchase orders
            if po.state in ['purchase', 'done']:
                raise exceptions.UserError(
                    f"Cannot delete confirmed/completed purchase order: {po.name}\n"
                    "Please cancel the order first before deletion."
                )

            # Prevent deletion of priority orders without special approval
            if po.is_priority and po.state != 'cancel':
                raise exceptions.UserError(
                    f"Cannot delete priority purchase order: {po.name}\n"
                    "Please remove priority flag or cancel the order first."
                )

        # Log deletion for audit trail
        po_names = self.mapped('name')

        # --- CALL THE ORIGINAL METHOD ---
        result = super().unlink()

        return result

    # ==================== ADD THE MISSING METHOD FOR BUTTON ====================
    def action_test_custom_method(self):
        """
        Test method to demonstrate custom CRUD overrides
        This is called by the button in the view
        """
        # Just show a success message
        message = f"""
        ✅ Custom CRUD Override Test Successful!

        Order: {self.name}
        Approval Code: {self.approval_code}
        Priority: {self.is_priority}
        State: {self.state}

        The create, write, and unlink methods have been overridden successfully.
        """

        # Show notification to user
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'CRUD Override Test',
                'message': message,
                'type': 'success',
                'sticky': False,
            }
        }

    # ==================== ALTERNATIVE: Using @api.ondelete (Recommended) ====================
    @api.ondelete(at_uninstall=False)
    def _check_unlink_constraints(self):
        """
        This is the recommended Odoo way to add deletion restrictions
        Avoids issues during module uninstallation
        """
        for po in self:
            if po.state in ['purchase', 'done']:
                raise exceptions.UserError(
                    f"Cannot delete purchase order in {po.state} state: {po.name}"
                )