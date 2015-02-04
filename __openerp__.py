# -*- coding: utf-8 -*-
{
    'name': 'Wechat Enterprise Module',
    'version': '0.2',
    'category': 'wechat',
    'complexity': "easy",
    'description': """
Wechat Enterprise""",
    'author': 'Matt Cai',
    'website': 'http://odoosoft.com',
    'depends': ['base', 'web'],
    'data': [
        'views/message_view.xml',
        'views/user_view.xml',
        'views/filter_view.xml',
        'views/menu.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'demo': [],
    'application': True
}
