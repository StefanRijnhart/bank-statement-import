# coding: utf-8
from openerp import api, models


class BankStatement(models.Model):
    _inherit = 'account.bank.statement'

    @api.multi
    def get_reconcile_clearing_account_lines(self):
        if (self.journal_id.default_debit_account_id !=
                self.journal_id.default_credit_account_id or
                not self.journal_id.default_debit_account_id.reconcile):
            return False
        move_lines = self.env['account.move.line'].search([
            ('statement_id', '=', self.id),
            ('account_id', '=', self.journal_id.default_debit_account_id.id),
        ])
        balance = sum(line.debit - line.credit for line in move_lines)
        currency = self.journal_id.currency or self.company_id.currency_id
        if not currency.is_zero(balance):
            return False
        return move_lines

    @api.multi
    def reconcile_clearing_account(self):
        self.ensure_one()
        lines = self.get_reconcile_clearing_account_lines()
        if not lines:
            return False
        if any(line.reconcile_id or line.reconcile_partial_id
               for line in lines):
            return False
        lines.reconcile_partial()

    @api.multi
    def button_cancel(self):
        res = super(BankStatement, self).button_cancel()
        for statement in self:
            statement.unreconcile_clearing_account()
        return res

    @api.multi
    def button_confirm_bank(self):
        res = super(BankStatement, self).button_confirm_bank()
        for statement in self:
            statement.reconcile_clearing_account()
        return res
