from odoo import fields, models, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sell_property(self):
        super().sell_property()

        for property in self:
            self.env['account.move'].create({
                'partner_id': property.buyer.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        'name': property.name,
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    Command.create({
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    })
                ]
            })
