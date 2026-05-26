from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    contract_line_name_template = fields.Text(
        string="Description",
        help=(
            "Description used for the contract line when this product is sold. "
            "Use #START# and #END# placeholders for invoicing period dates."
        ),
    )
    skip_contract_configurator = fields.Boolean(
        string="Skip Contract Configurator",
        default=False,
        help=(
            "If checked, the contract configuration wizard will not pop up "
            "when adding this product to a sale order. Product defaults will be used instead."
        ),
    )
    manual_renew_needed = fields.Boolean(
        string="Manual Renew Needed",
        default=False,
        help="If checked, contract renewals require manual approval.",
    )
