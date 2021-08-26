# -*- coding: utf-8 -*-
{
    'name': "Sugar Laboratory",
    'summary': """  Custom Application To enhance Sugar Laboratories """,
    'description': """ Sugar Laboratories  """,
    'author': "SIIC",
    'category': 'Other',
    'depends': ['base', 'portal', 'contacts', 'multi_branch'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/malfunction_views.xml',
        'views/malfunction_branch_view.xml',
        'views/lab_season.xml',
        'views/lab_sugar_analysis.xml',
        'views/lab_menu_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
