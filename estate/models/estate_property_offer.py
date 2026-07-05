from odoo import fields, models, api
from datetime import timedelta

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
    