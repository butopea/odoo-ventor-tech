# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

# Odoo:
from odoo import _, api, fields, models


class PalletTransfer(models.Model):
    _name = "pallet.transfer"
    _description = "All Pallet Transfers"

    name = fields.Char(
        string="Transfer Name",
        default="New",
    )
    pallet_name = fields.Char(string="Pallet Name")
    pallet_id = fields.Many2one("stock.location", string="Pallet")
    destination_location_id = fields.Many2one("stock.location", string="Destination Location")

    def update_value(self):
        self.write(
            {
                "name": self.env["ir.sequence"].next_by_code("pallet.transfer"),
                "pallet_name": self.pallet_id.name,
            }
        )
        self.pallet_id.location_id = self.destination_location_id

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res:
            res.update_value()
        return res
