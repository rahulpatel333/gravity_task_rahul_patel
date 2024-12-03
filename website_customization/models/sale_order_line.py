from odoo import models, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('product_id')
    def _onchange_product_id_set_price(self):
        if self.product_id.discount_percentage > 0:
            self.price_unit = self.product_id.discounted_price

    @api.depends('product_id', 'product_uom', 'product_uom_qty')
    def _compute_price_unit(self):
        for line in self:
            if line.qty_invoiced > 0 or (line.product_id.expense_policy == 'cost' and line.is_expense):
                continue
            if not line.product_uom or not line.product_id:
                line.price_unit = 0.0
            else:
                if line.product_id.discount_percentage > 0:
                    line.price_unit = line.product_id.discounted_price
                else:
                    line = line.with_company(line.company_id)
                    price = line._get_display_price()
                    line.price_unit = line.product_id._get_tax_included_unit_price_from_price(
                        price,
                        line.currency_id or line.order_id.currency_id,
                        product_taxes=line.product_id.taxes_id.filtered(
                            lambda tax: tax.company_id == line.env.company
                        ),
                        fiscal_position=line.order_id.fiscal_position_id,
                    )


