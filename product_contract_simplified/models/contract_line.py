from odoo import fields, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    manual_renew_needed = fields.Boolean(
        string="Manual Renew Needed",
        default=False,
        help="If checked, contract renewals require manual approval.",
    )
