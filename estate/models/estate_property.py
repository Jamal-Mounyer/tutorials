from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    @staticmethod
    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)


    name = fields.Char(required = True, string = 'Title')
    description = fields.Text(string = 'Description')
    postcode = fields.Char(string = 'Postcode')
    date_availability = fields.Date(string = 'Available From', copy = False, default = _default_date_availability)
    expected_price = fields.Float(string = 'Expected Price', required = True)
    selling_price = fields.Float(string = 'Selling Price', readonly = True, copy = False)
    bedrooms = fields.Integer(string = 'Bedrooms', default = 2)
    living_area = fields.Integer(string = 'Living Area (sqm)')
    facades = fields.Integer(string = 'Facades')
    garage = fields.Boolean(string = 'Garage')
    garden = fields.Boolean(string = 'Garden')
    garden_area = fields.Integer(string = 'Garden Area (sqm)')
    garden_orientation = fields.Selection(string = 'Garden Orientation', 
                                          selection=[('North', 'north'),
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
