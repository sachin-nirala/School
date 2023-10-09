# -*- coding: utf-8 -*-
{
    'name': "PST School",

    'summary': """
        For Customization in sale module""",

    'description': """
        For School management system 
    """,

    'author': "PST devs",
    'website': "https://pennsummitgroup.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'sequence': -100,

    # any module necessary for this one to work correctly
    'depends': ['mail', 'base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'wizard/wizard_customized_view.xml',
        'report/pst_quotation.xml',
        'report/cus_report.xml',
        'report/cus_report_template.xml',
        'report/pst_school.xml',
        'views/customized_view.xml',
        'views/sale.xml',
        'views/excel_view.xml',

        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
