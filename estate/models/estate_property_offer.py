from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        for offer in property.offer_ids:
            if vals['price'] < offer.price:
                raise UserError('You cannot create an offer with a lower amount than an existing offer.')

        records = super().create(vals)

        for record in records:
            record.property_id.state = 'Offer Received'

        return records

    @api.constrains('price')
    def _check_offer_price(self):
        for record in self:
            if record.price < 0.9 * record.property_id.expected_price:
                raise ValidationError('The offered price shouldn\'t be less than 90% of the property expected price.')


    @api.depends('validity', 'create_date')
    def _compute_deadline_date(self):
        for record in self:
            record.date_deadline = record.create_date + timedelta(days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def accept_offer(self):
        '''
            I have searched for ways to accept only one offer
            but didn't implement it because I thought that it's
            out of the tutorial
            EX: accepted_offer = self.env['estate.property.offer'].search([
                    ('property_id', '=', self.property_id.id),
                    ('status', '=', 'accepted'),
                    ('id', '!=', self.id),
                ], limit=1)
        '''
        self.status = 'Accepted'
        self.property_id.buyer = self.env.user
        self.property_id.selling_price = self.price
        self.property_id.state = 'Offer Accepted'


    def reject_offer(self):
        if self.status != 'Accepted':
            self.status = 'Refused'
        else:
            raise UserError('You cannot cancel your payment.')


#Relational fields
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required = True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    

#Computed fields
    validity = fields.Integer(string = 'Validity (days)', default = 7)
    date_deadline = fields.Date(string = 'Deadline',
                                compute = '_compute_deadline_date',
                                inverse = '_inverse_deadline_date')
    create_date = fields.Date(default = fields.Date.today)

#Normal fields
    price = fields.Float(string = 'Price')
    status = fields.Selection(string = 'Status',
                              selection = [('no copy', 'no copy'),
                                           ('Accepted', 'Accepted'),
                                           ('Refused', 'Refused')])
    
#Constraints
    _sql_constraints =[
        ('positive_offer_price', 'CHECK(price >= 0)', 
        'The offer price shouldn\'t be negative.'),
    ]