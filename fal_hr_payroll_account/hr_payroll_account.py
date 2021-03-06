#-*- coding:utf-8 -*-
import time
from openerp import netsvc
from datetime import date, datetime, timedelta

from openerp.osv import fields, orm
from openerp.tools import config, float_compare
from openerp.tools.translate import _

class hr_payslip(orm.Model):
    
    _name = "hr.payslip"    
    _inherit = "hr.payslip"
    
    #override real method
    def process_sheet(self, cr, uid, ids, context=None):
        move_pool = self.pool.get('account.move')
        period_pool = self.pool.get('account.period')
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Payroll')
        timenow = time.strftime('%Y-%m-%d')

        for slip in self.browse(cr, uid, ids, context=context):
            line_ids = []
            debit_sum = 0.0
            credit_sum = 0.0
            if not slip.period_id:
                ctx = dict(context or {}, account_period_prefer_normal=True)
                search_periods = period_pool.find(cr, uid, slip.date_to, context=ctx)
                period_id = search_periods[0]
            else:
                period_id = slip.period_id.id

            default_partner_id = slip.employee_id.address_home_id.id
            name = _('Payslip of %s') % (slip.employee_id.name)
            move = {
                'narration': name,
                'date': timenow,
                'ref': slip.number,
                'journal_id': slip.journal_id.id,
                'period_id': period_id,
            }
            for line in slip.details_by_salary_rule_category:
                amt = slip.credit_note and -line.total or line.total
                partner_id = line.salary_rule_id.register_id.partner_id and line.salary_rule_id.register_id.partner_id.id or default_partner_id
                debit_account_id = line.salary_rule_id.account_debit.id
                credit_account_id = line.salary_rule_id.account_credit.id                
                #modif start here
                anal_account = (line.salary_rule_id.analytic_account_id and line.salary_rule_id.analytic_account_id.id) or (slip.contract_id.analytic_account_id and slip.contract_id.analytic_account_id.id) or False                
                if debit_account_id and amt != 0.00 :
                #end here
                    debit_line = (0, 0, {
                    'name': line.name,
                    'date': timenow,
                    'partner_id': partner_id or False,
                    'account_id': debit_account_id,
                    'journal_id': slip.journal_id.id,
                    'period_id': period_id,
                    'debit': amt > 0.0 and amt or 0.0,
                    'credit': amt < 0.0 and -amt or 0.0,
                    #modif start here
                    'analytic_account_id': anal_account,
                    #end here
                    'tax_code_id': line.salary_rule_id.account_tax_id and line.salary_rule_id.account_tax_id.id or False,
                    'tax_amount': line.salary_rule_id.account_tax_id and amt or 0.0,
                })
                    line_ids.append(debit_line)
                    debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']
                #modif start here
                if credit_account_id and amt != 0.00:
                #end here
                    credit_line = (0, 0, {
                    'name': line.name,
                    'date': timenow,
                    'partner_id': partner_id or False,
                    'account_id': credit_account_id,
                    'journal_id': slip.journal_id.id,
                    'period_id': period_id,
                    'debit': amt < 0.0 and -amt or 0.0,
                    'credit': amt > 0.0 and amt or 0.0,
                    #modif start here
                    'analytic_account_id': anal_account,
                    #end here
                    'tax_code_id': line.salary_rule_id.account_tax_id and line.salary_rule_id.account_tax_id.id or False,
                    'tax_amount': line.salary_rule_id.account_tax_id and amt or 0.0,
                })
                    line_ids.append(credit_line)
                    credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

            if float_compare(credit_sum, debit_sum, precision_digits=precision) == -1:
                acc_id = slip.journal_id.default_credit_account_id.id
                if not acc_id:
                    raise orm.except_orm(_('Configuration Error!'),_('The Expense Journal "%s" has not properly configured the Credit Account!')%(slip.journal_id.name))
                adjust_credit = (0, 0, {
                    'name': _('Adjustment Entry'),
                    'date': timenow,
                    'partner_id': False,
                    'account_id': acc_id,
                    'journal_id': slip.journal_id.id,
                    'period_id': period_id,
                    'debit': 0.0,
                    'credit': debit_sum - credit_sum,
                    'analytic_account_id': slip.contract_id.analytic_account_id and slip.contract_id.analytic_account_id.id or False,
                })
                line_ids.append(adjust_credit)

            elif float_compare(debit_sum, credit_sum, precision_digits=precision) == -1:
                acc_id = slip.journal_id.default_debit_account_id.id
                if not acc_id:
                    raise orm.except_orm(_('Configuration Error!'),_('The Expense Journal "%s" has not properly configured the Debit Account!')%(slip.journal_id.name))
                adjust_debit = (0, 0, {
                    'name': _('Adjustment Entry'),
                    'date': timenow,
                    'partner_id': False,
                    'account_id': acc_id,
                    'journal_id': slip.journal_id.id,
                    'period_id': period_id,
                    'debit': credit_sum - debit_sum,
                    'credit': 0.0,
                    'analytic_account_id': slip.contract_id.analytic_account_id and slip.contract_id.analytic_account_id.id or False,
                })
                line_ids.append(adjust_debit)
            move.update({'line_id': line_ids})
            move_id = move_pool.create(cr, uid, move, context=context)
            self.write(cr, uid, [slip.id], {'move_id': move_id, 'period_id' : period_id}, context=context)
            if slip.journal_id.entry_posted:
                move_pool.post(cr, uid, [move_id], context=context)
        return self.write(cr, uid, ids, {'paid': True, 'state': 'done'}, context=context)

#end of hr_payslip()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
