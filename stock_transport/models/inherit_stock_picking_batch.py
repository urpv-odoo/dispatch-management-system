from odoo import api, models, fields


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("stock.transport.dock", "Dock")
    vehicle_id = fields.Many2one("fleet.vehicle", "Vehicle")
    vehicle_category_id = fields.Many2one(
        "fleet.vehicle.model.category", "Vehicle Category"
    )

    weight = fields.Float(
        string="Weight", compute="_compute_weight", store=True, digits=(12, 2)
    )
    volume = fields.Float(
        string="Volume", compute="_compute_volume", store=True, digits=(12, 2)
    )

    tot_weight = fields.Float("Total Weight", readonly=1)
    tot_volume = fields.Float("Total Volume", readonly=1)

    transfer_lines = fields.Integer("Transfer Lines", compute="_compute_transfer_lines")

    @api.depends("picking_ids.weight", "vehicle_category_id")
    def _compute_weight(self):
        for record in self:
            total_weight = 0
            for picking in record.picking_ids:
                total_weight += picking.weight
            if record.vehicle_category_id.max_weight != 0.0:
                record.weight = (
                    total_weight / record.vehicle_category_id.max_weight
                ) * 100
                record.tot_weight = total_weight
            else:
                record.weight = 0.0
                record.tot_weight = 0.0

    @api.depends("picking_ids.volume", "vehicle_category_id")
    def _compute_volume(self):
        for record in self:
            total_volume = 0
            for picking in record.picking_ids:
                total_volume += picking.volume
            if record.vehicle_category_id.max_volume != 0.0:
                record.volume = (
                    total_volume / record.vehicle_category_id.max_volume
                ) * 100
                record.tot_volume = total_volume
            else:
                record.volume = 0.0
                record.tot_volume = 0.0

    @api.depends("picking_ids")
    def _compute_transfer_lines(self):
        for record in self:
            record.transfer_lines = len(record.picking_ids)

    @api.depends("weight", "volume")
    def _compute_display_name(self):
        for record in self:
            precision = 2

            formatted_weight = f"{record.tot_weight:.{precision}f}"
            formatted_volume = f"{record.tot_volume:.{precision}f}"

            record.display_name = (
                record.name
                + " ("
                + formatted_weight
                + "kg, "
                + formatted_volume
                + "m\u00b3)"
            )
