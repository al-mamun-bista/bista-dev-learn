{
    'name' : 'Inventory Transfer',
    'version' : '1.1',
    'summary': 'Inventory Transfer',
    'sequence': 1,
    'description': """
       Transfer product from sourch location to destination location
    """,
    'category': 'Inventory',
    'website': 'https://www.odoo.com/page/billing',
    'images' : [],
    'depends' : ['base','stock','mail','report_xlsx'],
    'data': [
            
            # security
            'security/security.xml',
            'security/ir.model.access.csv',
            # view
            'views/internal_transfer_view_form.xml',
            # data
            'data/data.xml',
            
            #report
            'reports/report.xml',
            'reports/internal_transfer_order_view.xml',
            'reports/consolidated_report_view.xml',
            'data/internal_transfer_mail.xml',
            # wizard view
            'wizard/inventory_consolidated_report_view.xml',
            
        ],
    'demo': [
       
    ],
    'qweb': [
        
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
