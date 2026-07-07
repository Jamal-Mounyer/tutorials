{
    'name': 'estate',
    'depends': ['base'],
    'application': True,
    'license': 'LGPL-3', 
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_actions.xml',
        'views/estate_property_views.xml',
        'views/estate_property_tag.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_type.xml',
        'views/estate_menus.xml',
        'views/base_view_users_form.xml',
    ]
}