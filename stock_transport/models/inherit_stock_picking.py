from odoo import api, models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    weight = fields.Float(compute="_cal_weight", string="Weight", store=True)
    volume = fields.Float(compute="_cal_volume", string="Volume", store=True)

    @api.depends("product_id", "product_id.weight", "move_line_ids.quantity")
    def _cal_weight(self):
        for record in self:
            cal_weight = 0
            for move in record.move_line_ids:
                cal_weight += move.product_id.weight * move.quantity
            record.weight = cal_weight

    @api.depends("product_id", "product_id.volume", "move_line_ids.quantity")
    def _cal_volume(self):
        for record in self:
            cal_volume = 0
            for move in record.move_line_ids:
                cal_volume += move.product_id.volume * move.quantity
            record.volume = cal_volume
