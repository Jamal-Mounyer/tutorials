from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    @staticmethod
    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)


    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy = False, default = _default_date_availability)
    expected_price = fields.Float(required = True)
    selling_price = fields.Float(readonly = True, copy = False)
    bedrooms = fields.Integer(default = 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[('North', 'north'),
                                                     ('South', 'south'),
                                                     ('East', 'east'),
                                                     ('West', 'west')])
    
    active = fields.Boolean(default = True)
    state = fields.Selection(required = True,
                             copy = False,
                             default = 'New',
                             selection = [('New', 'new'), 
                                          ('Offer Received', 'Offer Received'),
                                          ('Offer Accepted', 'Offer Accepted'), 
                                          ('Sold', 'sold'),
                                          ('Cancelled', 'Cancelled')])
