from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    discount_percentage = fields.Float(
        string="Discount Percentage",
        help="Set the discount percentage for the product."
    )

    discounted_price = fields.Float(
        string="Discounted Price",
        compute="_compute_discounted_price",
        store=True
    )

    @api.depends("list_price", "discount_percentage")
    def _compute_discounted_price(self):
        for product in self:
            if product.discount_percentage > 0:
                product.discounted_price = product.list_price * (1 - (product.discount_percentage / 100))
            else:
                product.discounted_price = product.list_price

    def _get_combination_info(self, combination=False, product_id=False, add_qty=1.0, parent_combination=False, only_template=False):
        combination_info = super(ProductTemplate, self)._get_combination_info(combination, product_id, add_qty, parent_combination, only_template)
        combination_info.update({
            'new_discounted_price': False,
            'discounted_price': 0
        })
        if self.discount_percentage > 0:
            combination_info.update({
                'new_discounted_price': True,
                'discounted_price': self.discounted_price
            })
        return combination_info

