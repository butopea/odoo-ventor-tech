from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})

    validate_wave_picking = env.ref("ventor_base.validate_wave_picking", False)
    validate_picking_batch = env.ref("ventor_base.validate_picking_batch", False)
    validate_cluster_picking = env.ref("ventor_base.validate_cluster_picking", False)

    value = {
        "description": "Validate Stock Picking automatically if it completely processed. "
                       "Note: When ON transfers with all skipped items will be validated with initial quantity"
    }

    if validate_wave_picking:
        validate_wave_picking.write(value)
    if validate_picking_batch:
        validate_picking_batch.write(value)
    if validate_cluster_picking:
        validate_cluster_picking.write(value)
