from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    @staticmethod
    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max([offer.price for offer in record.offer_ids] or [0])

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'North'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError('The selling price shouldn\'t be less than 90% of the expected price.')

    def sell_property(self):
        if self.state != 'Canceled':
            self.state = 'Sold'
        else:
            raise UserError('Canceled properties cannot be sold.')
    
    def cancel_selling(self):
        if self.state != 'Sold':
            self.state = 'Canceled'
        else:
            raise UserError('Sold properties cannot be canceled.')


#Relational fields
    property_type_id = fields.Many2one(comodel_name = 'estate.property.type',
                                    string = 'Property Type')
    buyer = fields.Many2one(comodel_name = 'res.users',
                            string = 'Buyer', copy = False)
    salesperson = fields.Many2one(comodel_name = 'res.partner',
                                  string = 'Salesman', default = lambda self: self.env.user)
    tag_ids = fields.Many2many(comodel_name = 'estate.property.tag',
                               string = 'Tags')
    offer_ids = fields.One2many('estate.property.offer', inverse_name = 'property_id')

#Computed fields
    total_area = fields.Integer(string = 'Total Area (sqm)',
                                compute = '_compute_total_area')
    best_price = fields.Float(string = 'Best Offer',
                              compute = '_compute_best_price')
    

#Normal fields
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
                             string = 'status',
                             copy = False,
                             default = 'New',
                             selection = [('New', 'new'), 
                                          ('Offer Received', 'Offer Received'),
                                          ('Offer Accepted', 'Offer Accepted'), 
                                          ('Sold', 'sold'),
                                          ('Canceled', 'Canceled')])

#Constraints
    _sql_constraints =[
        ('positive_expected_price', 'CHECK(expected_price >= 0)', 
        'The expected price shouldn\'t be negative.'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 
        'The selling price shouldn\'t be negative.'),
    ]