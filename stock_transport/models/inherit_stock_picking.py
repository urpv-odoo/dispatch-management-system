from odoo import api, models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    weight = fields.Float(compute="_cal_weight", string="Weight", store=True)
    volume = fields.Float(compute="_cal_volume", string="Volume", store=True)

    @api.depends("weight")
    def _cal_weight(self):
        self.weight = 1112.0
        print(self)

    @api.depends("volume")
    def _cal_volume(self):
        self.volume = 1111.0
        print(self)
