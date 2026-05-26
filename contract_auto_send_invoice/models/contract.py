import logging

from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class ContractContract(models.Model):
    _inherit = "contract.contract"

    auto_send_recurring_invoice = fields.Boolean(
        string="Auto Post and Email Invoices",
        default=True,
        help=(
            "If enabled, recurring invoices generated from this contract "
            "are posted and emailed automatically."
        ),
    )

    @api.model
    def _get_recurring_create_func(self, create_type="invoice"):
        recurring_create_func = super()._get_recurring_create_func(create_type=create_type)
        if create_type == "invoice":
            return self.__class__._recurring_create_invoice_from_cron
        return recurring_create_func

    def _recurring_create_invoice_from_cron(self, date_ref=False):
        moves = super()._recurring_create_invoice(date_ref=date_ref)
        self._auto_post_and_send_recurring_invoices(moves)
        return moves

    def _auto_post_and_send_recurring_invoices(self, moves):
        contracts = self.filtered("auto_send_recurring_invoice")
        if not contracts:
            return

        all_contract_moves = self.env["account.move"]
        for contract in contracts:
            all_contract_moves |= moves & contract._get_related_invoices()

        draft_moves = all_contract_moves.filtered(lambda m: m.state == "draft")
        if draft_moves:
            draft_moves.action_post()

        to_send = all_contract_moves.filtered(
            lambda m: m.state == "posted" and m.move_type == "out_invoice"
        )
        if not to_send:
            return

        no_email = to_send.filtered(lambda m: not m.partner_id.email)
        for move in no_email:
            _logger.info(
                "Skipping auto-send for invoice %s: partner has no email address",
                move.name,
            )
        to_send -= no_email

        if not to_send:
            return

        # Use Odoo's canonical send path so the invoice PDF is generated and
        # attached to the email – replicating what account.move._generate_and_send does.
        # from_cron must be False: our moves never go through the Send & Print wizard,
        # so sending_data is False and reading it would crash. We supply all settings
        # explicitly via custom_settings instead.
        self.env["account.move.send"]._generate_and_send_invoices(
            to_send,
            from_cron=False,
            allow_raising=False,
            allow_fallback_pdf=True,
            sending_methods={"email"},
        )
