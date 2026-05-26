from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    skip_contract_configurator = fields.Boolean(
        related="product_id.skip_contract_configurator",
        readonly=True,
    )

    def _prepare_contract_line_values(
        self, contract, predecessor_contract_line_id=False
    ):
        vals = super()._prepare_contract_line_values(
            contract, predecessor_contract_line_id=predecessor_contract_line_id
        )
        template = self.product_id.contract_line_name_template
        if template:
            vals["name"] = template
        vals["manual_renew_needed"] = self.product_id.manual_renew_needed
        return vals
