from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(required = True)

#Constraints
    _sql_constraints =[
        ('unique_type_name', 'UNIQUE(name)', 
        'The type name should be unique.'),
    ]