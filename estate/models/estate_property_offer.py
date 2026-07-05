from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

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


    def reject_offer(self):
        if self.stat != 'Accepted':
            self.status = 'Refused'
        else:
            raise UserError('You cannot cancel your payment.')


#Relational fields
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.property', required = True)

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
    