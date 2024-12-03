# -*- coding: utf-8 -*-
{
    'name': "Website Product Discount Feature",
    'summary': "Add a discount feature to products in Odoo eCommerce",
    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Website',
    'version': '1.0',
    'depends': ['base', 'website_sale', 'product'],
    'data': [
        'views/product_template_view.xml',
        'views/product_template.xml',
    ],
    'installable': True,
    'application': False,
}

