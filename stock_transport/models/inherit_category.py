from odoo import api, models, fields


class FleetVehicleCategory(models.Model):
    _inherit = "fleet.vehicle.model.category"

    max_weight = fields.Float("Max Weight (Kg)")
    max_volume = fields.Float("Max Volume (m^3)")

    @api.depends('name', 'max_weight', 'max_volume')
    def _compute_display_name(self):
        for category in self:
            category.display_name = "%s (%s kg, %s m\u00b3)" % (
                category.name,
                category.max_weight,
                category.max_volume
            )
