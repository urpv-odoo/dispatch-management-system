from odoo import api, models, fields


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("stock.transport.dock", "Dock")
    vehicle_id = fields.Many2one(
        "fleet.vehicle", "Vehicle", placeholder="Opel GJ45XC1234"
    )
    vehicle_category_id = fields.Many2one(
        "fleet.vehicle.model.category",
        "Vehicle Category",
        placeholder="e.g. Semi-Truck",
    )

    category_weight = fields.Float(related="vehicle_category_id.max_weight", store=True)
    category_volume = fields.Float(related="vehicle_category_id.max_volume", store=True)

    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)
    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)

    @api.depends("picking_ids.weight")
    def _compute_weight(self):
        for record in self:
            total_weight = 0
            for picking in record.picking_ids:
                total_weight += picking.weight
            if(record.category_volume != 0.0):
                record.weight = (total_weight / record.category_weight) * 100
            else:
                record.weight = 0.0

    @api.depends("picking_ids.volume")
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for picking in record.picking_ids:
                total_volume += picking.volume
            if(record.category_volume != 0.0):
                record.volume = (total_volume / record.category_volume) * 100
            else:
                record.volume = 0.0
