﻿# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import json

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_warehouse_ids = fields.Many2many(
        comodel_name='stock.warehouse',
        string='Allowed Warehouses',
        help='List of all warehouses user has access to',
    )

    default_inventory_location = fields.Many2one(
        comodel_name='stock.location',
        string='Default Inventory Location',
    )

    default_warehouse = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Default Warehouse For Ventor App'
    )

    stock_location_id = fields.Many2one(
        'stock.location',
        string='Force Source Location for Instant Move',
        required=False,
    )

    allow_to_change_force_source_location = fields.Boolean(
        string='Allow to change Force Source Location',
    )

    custom_package_name = fields.Char(
        string='Custom package name'
    )

    ventor_global_settings = fields.Text(
        string='Global Settings',
        readonly=True,
        compute='_compute_global_settings'
    )

    ventor_user_settings = fields.Text(
        string='User Settings'
    )

    @property
    def SELF_READABLE_FIELDS(self):
        readable_fields = [
            'ventor_global_settings',
            'ventor_user_settings',
            'custom_package_name',
        ]
        return super().SELF_READABLE_FIELDS + readable_fields

    @property
    def SELF_WRITEABLE_FIELDS(self):
        writable_fields = ['ventor_user_settings']
        return super().SELF_WRITEABLE_FIELDS + writable_fields

    def _compute_global_settings(self):
        settings = []

        for stock_picking_type in self.env['stock.picking.type'].search([]):
            settings.append(stock_picking_type.get_ventor_settings())

        self.ventor_global_settings = json.dumps(
            obj={'operation_types': settings},
            indent='    ',
            sort_keys=True
        )

    def write(self, vals):
        result = super().write(vals)
        if result and 'allowed_warehouse_ids' in vals:
            self.env['ir.rule'].clear_cache()
        return result