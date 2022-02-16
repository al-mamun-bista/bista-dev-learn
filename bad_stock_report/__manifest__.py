# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bad Stock Report',
    'author': 'Mokhlesur Rahman Mahin2',
    'category': '',
    'version': '1.0',
    'description': """Bad Stock Report""",
    'summary': 'Bad Stock Report',
    'sequence': 10,
    'website': 'https://www.google.com',
    'depends': ['mail'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/bad_stock_report_config_view.xml',
        'views/menu.xml',
        'reports/report.xml',
        'reports/bad_stock_report_view.xml'
    ],
    "images": [],
    'demo': [],
    'installable': True,

}
