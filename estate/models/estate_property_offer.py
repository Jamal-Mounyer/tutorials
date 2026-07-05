from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

#Relational fields
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required = True)

#Normal fields
    price = fields.Float(string = 'Price')
    status = fields.Selection(string = 'Status',
                              selection = [('no copy', 'no copy'),
                                           ('Accepted', 'Accepted'),
                                           ('Refused', 'Refused')])
    