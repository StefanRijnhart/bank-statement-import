# coding: utf-8
from openerp.addons.account_bank_statement_import.tests import (
    TestStatementFile)


class TestImportAdyen(TestStatementFile):
    def setUp(self):
        super(TestImportAdyen, self).setUp()
        self.journal = self.env['account.journal'].search(
            [('type', '=', 'bank')], limit=1)
        self.journal.write({'adyen_merchant_account': 'YOURCOMPANY_ACCOUNT'})

    def test_import_adyen(self):
        self._test_statement_import(
            'account_bank_statement_import_adyen', 'adyen_test.xlsx',
            'YOURCOMPANY_ACCOUNT 2016/48')
        statement = self.env['account.bank.statement'].search(
            [], order='create_date desc', limit=1)
        self.assertEqual(len(statement.line_ids), 21)
