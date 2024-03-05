from odoo import api, models, fields


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("stock.transport.dock", "Dock")
    vehicle_id = fields.Many2one(
        "fleet.vehicle", "Vehicle", placeholder="Opel GJ45XC1234"
    )
    vehicle_category_id = fields.Many2one(
        "fleet.vehicle.model.category", "Vehicle Category"
    )

    category_weight = fields.Float(related="vehicle_category_id.max_weight", store=True)
    category_volume = fields.Float(related="vehicle_category_id.max_volume", store=True)

    weight = fields.Float(string="Weight", compute="_compute_weight")
    volume = fields.Float(string="Volume", compute="_compute_volume")

    @api.depends(
        "picking_ids.move_ids.product_id.weight",
        "picking_ids.move_ids.quantity",
    )
    def _compute_weight(self):
        for batch in self:
            total_weight = sum(
                move.product_id.weight * move.quantity
                for move in batch.mapped("picking_ids.move_ids")
            )
            batch.weight = total_weight
        print(self.weight)

    @api.depends(
        "picking_ids.move_ids.product_id.volume", "picking_ids.move_ids.quantity"
    )
    def _compute_volume(self):
        for batch in self:
            total_volume = sum(
                move.product_id.volume * move.quantity
                for move in batch.mapped("picking_ids.move_ids")
            )
            batch.volume = total_volume
        print(self.volume)
