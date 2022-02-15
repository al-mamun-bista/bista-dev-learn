# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bad Due Report',
    'author': 'Mokhlesur Rahman Mahin',
    'category': '',
    'version': '1.0',
    'description': """Bad Due Report""",
    'summary': 'Bad Due Report',
    'sequence': 10,
    'website': 'https://www.google.com',
    'depends': [],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/due_days_mail_config.xml',
    ],
    "images": [],
    'demo': [],
    'installable': True,

}