from odoo import fields, models, api

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'name'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


            
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', 
                                string = 'Offers')
    name = fields.Char(required = True)
    sequence = fields.Integer(default = 1)
    offer_count = fields.Integer(compute = '_compute_offer_count')

#Constraints
    _sql_constraints =[
        ('unique_type_name', 'UNIQUE(name)', 
        'The type name should be unique.'),
    ]