from odoo import api, fields, models


class ContractLine(models.Model):
    _inherit = ["contract.line", "commission.mixin"]
    _name = "contract.line"

    agent_ids = fields.One2many(
        comodel_name="contract.line.agent",
        inverse_name="object_id",
        string="Agents & commissions",
        copy=True,
    )

    @api.depends("contract_id.partner_id")
    def _compute_agent_ids(self):
        self.agent_ids = False
        for record in self:
            if record.contract_id.partner_id and not record.commission_free:
                record.agent_ids = record._prepare_agents_vals_partner(
                    record.contract_id.partner_id,
                    settlement_type="sale_invoice",
                )

    def _prepare_invoice_line(self):
        vals = super()._prepare_invoice_line()
        vals["agent_ids"] = [
            (0, 0, {"agent_id": x.agent_id.id, "commission_id": x.commission_id.id})
            for x in self.agent_ids
        ]
        return vals


class ContractLineAgent(models.Model):
    _inherit = "commission.line.mixin"
    _name = "contract.line.agent"
    _description = "Agent detail of commission line in contract lines"

    object_id = fields.Many2one(
        comodel_name="contract.line",
        ondelete="cascade",
        required=True,
    )
    currency_id = fields.Many2one(
        related="object_id.currency_id",
    )

    def _compute_amount(self):
        # Amount is intentionally not calculated on the contract line.
        # The agent + commission rate are carried through to the invoice line
        # via _prepare_invoice_line(); account.invoice.line.agent computes
        # the real commission amount from the actual invoiced subtotal.
        for line in self:
            line.amount = 0.0

