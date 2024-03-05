from odoo import api, models, fields


class Dock(models.Model):
    _name = "stock.transport.dock"
    _description = "Real Estate property model."

    name = fields.Char("Dock")
