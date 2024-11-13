from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})

    is_qc_installed = env.user.is_module_installed('quality_control')

    if is_qc_installed:
        # BP, CP, WP menus
        ventor_quality_control_settings = env['ventor.option.setting'].search(
            [
                ('technical_name', '=', 'quality_check_per_product_line'),
            ]
        )
        ventor_quality_control_settings.value = env.ref('ventor_base.bool_true')

        # WO operation types:
        stock_picking_type_ids = env['stock.picking.type'].with_context(active_test=False).search([])
        stock_picking_type_ids.quality_check_per_product_line = True
